"""
gui.py - 图形界面模块（Graphical User Interface）
作用：创建窗口、输入框、按钮等控件，用户点击"生成排班表"后调用 core 模块
适合不习惯命令行的用户
"""
import datetime
# 用于获取当前年份，作为默认值

import os
# 用于路径操作：拼接路径、判断文件是否存在、打开文件

import tkinter as tk
# tkinter 是 Python 自带的图形界面库，tk 是常用缩写

from tkinter import ttk, messagebox, scrolledtext, filedialog
# ttk：更美观的控件（主题样式）
# messagebox：弹窗提示（如警告、错误、信息）
# scrolledtext：带滚动条的多行文本框
# filedialog：文件选择对话框（选保存位置）

# 从同包的 core 导入三个核心函数
from .core import get_all_schedule_dates, create_schedule, export_to_excel


def get_holiday_year_range():
    """
    获取 chinesecalendar 节假日库支持的年份范围
    返回值：(最小年份, 最大年份)
    """
    try:
        from chinese_calendar.constants import holidays
        # 集合推导：{d.year for d in holidays} 取出所有年份
        years = {d.year for d in holidays}
        return min(years), max(years)
    except Exception:
        # 出错时给一个默认范围
        return 2004, 2026


def get_holiday_lib_version():
    """
    获取 chinesecalendar 库的版本号
    getattr(对象, 属性名, 默认值)：取对象的属性，没有则返回默认值
    """
    try:
        import chinese_calendar
        return getattr(chinese_calendar, '__version__', '?')
    except Exception:
        return '?'


def get_project_root():
    """
    获取项目根目录路径（Excel 默认保存在这里）
    __file__ 是当前文件 gui.py 的路径
    dirname 取父目录；三次 dirname 从 gui.py -> paiban -> src -> 项目根
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ScheduleApp:
    """
    排班系统的主窗口类
    封装了所有界面元素和交互逻辑
    """

    def __init__(self):
        """
        初始化：创建主窗口和所有控件
        """
        # tk.Tk() 创建主窗口对象
        self.root = tk.Tk()
        self.root.title("部门排班系统")
        self.root.geometry("620x800")
        # 格式：宽x高，单位像素
        self.root.minsize(500, 600)
        self.root.resizable(True, True)
        # 允许用户拖拽改变窗口大小

        # ttk.Style() 创建样式对象，用于统一控件外观
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 16, "bold"))
        style.configure("Header.TLabel", font=("Microsoft YaHei UI", 11, "bold"))
        style.configure("TLabel", font=("Microsoft YaHei UI", 10))
        style.configure("TButton", font=("Microsoft YaHei UI", 10))

        self.create_widgets()

    def create_widgets(self):
        """
        创建界面上所有的控件（输入框、按钮、标签等）
        """
        main_frame = ttk.Frame(self.root, padding="15 15 15 15")
        # Frame：容器，用来组织其他控件；padding 四周留白 15 像素
        main_frame.pack(fill=tk.BOTH, expand=True)
        # pack 布局：fill 填满方向，expand 可扩展

        ttk.Label(main_frame, text="部门值班排班系统", style="Title.TLabel").pack(pady=(0, 20))
        ttk.Label(main_frame, text="输入组员姓名，一键生成排班表", foreground="gray").pack(pady=(0, 15))

        group_frame = ttk.LabelFrame(main_frame, text="第一步：设置组数和成员", padding="10")
        # LabelFrame：带标题的框
        group_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(group_frame, text="组数：").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        # grid 网格布局：row 行、column 列；sticky 对齐方式；padx 左右留白

        self.group_count_var = tk.StringVar(value="3")
        # StringVar：绑定到控件的变量，改它控件显示就变

        group_spin = ttk.Spinbox(group_frame, from_=1, to=10, width=5,
                                 textvariable=self.group_count_var, command=self.on_group_count_change)
        # Spinbox：数字选择框；from_/to 范围；command 值改变时调用的函数
        group_spin.grid(row=0, column=1, sticky=tk.W)
        ttk.Button(group_frame, text="确认组数", command=self.on_group_count_change).grid(row=0, column=2, padx=(10, 0))

        self.member_entries_frame = ttk.Frame(group_frame)
        self.member_entries_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=(15, 0))
        # columnspan 跨 3 列；sticky=tk.EW 横向拉伸
        self.member_entries = []
        # 存每组的输入框，后面用 .get() 读取用户输入

        ttk.Label(self.member_entries_frame, text="每组组员用逗号分隔，例如：张三,李四,王五", foreground="gray").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.create_member_entries(3)
        # 默认创建 3 组的输入框

        time_frame = ttk.LabelFrame(main_frame, text="第二步：选择排班时间范围", padding="10")
        time_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(time_frame, text="年份：").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.year_var = tk.StringVar(value=str(datetime.datetime.now().year))
        # datetime.now() 当前时间；.year 取年份；str() 转成字符串
        ttk.Spinbox(time_frame, from_=2004, to=2035, width=8, textvariable=self.year_var).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(time_frame, text="起始月份：").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(8, 0))
        self.start_month_var = tk.StringVar(value="1")
        ttk.Spinbox(time_frame, from_=1, to=12, width=5, textvariable=self.start_month_var).grid(row=1, column=1, sticky=tk.W, pady=(8, 0))

        ttk.Label(time_frame, text="结束月份：").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(8, 0))
        self.end_month_var = tk.StringVar(value="12")
        ttk.Spinbox(time_frame, from_=1, to=12, width=5, textvariable=self.end_month_var).grid(row=2, column=1, sticky=tk.W, pady=(8, 0))
        ttk.Label(time_frame, text="支持 2004-2035 年，法定节假日数据随 chinesecalendar 库更新", foreground="gray").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(4, 0))

        continue_frame = ttk.LabelFrame(main_frame, text="第三步：是否接续上一年的排班顺序（可选）", padding="10")
        continue_frame.pack(fill=tk.X, pady=(0, 10))

        self.continue_var = tk.BooleanVar(value=False)
        # BooleanVar：布尔类型，用于复选框
        ttk.Checkbutton(continue_frame, text="接续上一年排班（新年度排班时可选）", variable=self.continue_var,
                       command=self.toggle_continue_input).pack(anchor=tk.W)

        self.last_group_frame = ttk.Frame(continue_frame)
        self.last_group_frame.pack(anchor=tk.W, pady=(8, 0))
        ttk.Label(self.last_group_frame, text="上一年最后值班的组号：").pack(side=tk.LEFT, padx=(20, 5))
        self.last_group_var = tk.StringVar(value="1")
        self.last_group_spin = ttk.Spinbox(self.last_group_frame, from_=1, to=10, width=5, textvariable=self.last_group_var)
        self.last_group_spin.pack(side=tk.LEFT)
        self.last_group_frame.pack_forget()
        # pack_forget 隐藏控件，勾选"接续"后才显示

        save_frame = ttk.LabelFrame(main_frame, text="第四步：选择保存位置（可选）", padding="10")
        save_frame.pack(fill=tk.X, pady=(0, 10))
        self.save_path_var = tk.StringVar(value="")
        ttk.Label(save_frame, text="留空则保存在项目根目录").pack(anchor=tk.W)
        path_row = ttk.Frame(save_frame)
        path_row.pack(fill=tk.X, pady=(5, 0))
        self.save_entry = ttk.Entry(path_row, textvariable=self.save_path_var, width=50)
        # Entry：单行输入框
        self.save_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(path_row, text="浏览...", command=self.choose_save_path, width=8).pack(side=tk.LEFT)

        h_min, h_max = get_holiday_year_range()
        holiday_frame = ttk.LabelFrame(main_frame, text="节假日数据说明", padding="8")
        holiday_frame.pack(fill=tk.X, pady=(0, 10))
        info_text = (
            f"• 当前节假日库版本：chinesecalendar {get_holiday_lib_version()}\n"
            f"• 法定节假日数据支持：{h_min} 年 — {h_max} 年\n"
            "• 国务院一般在每年 11 月发布次年安排，建议届时执行：\n"
            "  pip install -U chinesecalendar  （获取最新节假日数据）"
        )
        self.holiday_info = tk.Text(holiday_frame, height=5, wrap=tk.WORD, font=("Microsoft YaHei UI", 9),
                                    relief=tk.FLAT, borderwidth=0, cursor="arrow")
        # Text：多行文本框；height 行数；wrap 自动换行；relief 边框样式
        self.holiday_info.insert(tk.END, info_text)
        self.holiday_info.config(state=tk.DISABLED)
        # 设为只读，用户不能编辑
        self.holiday_info.pack(fill=tk.X)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 10))

        self.generate_btn = ttk.Button(btn_frame, text="生成排班表", command=self.generate_schedule)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.open_btn = ttk.Button(btn_frame, text="打开生成的Excel", command=self.open_excel, state=tk.DISABLED)
        # state=tk.DISABLED 禁用，生成成功后才启用
        self.open_btn.pack(side=tk.LEFT)

        log_frame = ttk.LabelFrame(main_frame, text="运行信息", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.insert(tk.END, "请在上方填写组员信息，点击「生成排班表」即可。\n")
        self.log_text.config(state=tk.DISABLED)

        self.last_filename = None
        # 保存最近生成的 Excel 文件路径
        self.on_group_count_change()

    def create_member_entries(self, count):
        """
        根据组数创建对应数量的组员输入框
        count：组数
        """
        for widget in self.member_entries_frame.winfo_children():
            # winfo_children() 返回该容器的所有子控件
            if widget.winfo_class() == "TFrame":
                widget.destroy()
        self.member_entries.clear()

        for i in range(count):
            frame = ttk.Frame(self.member_entries_frame)
            frame.grid(row=i + 1, column=0, sticky=tk.EW, pady=3)
            ttk.Label(frame, text=f"第{i + 1}组：", width=8, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 5))
            entry = ttk.Entry(frame, width=50)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.member_entries.append(entry)

        self.member_entries_frame.columnconfigure(0, weight=1)
        # columnconfigure：设置列扩展权重

    def on_group_count_change(self):
        """
        组数改变时：刷新组员输入框数量，并更新"上一年最后组号"的范围
        """
        try:
            count = int(self.group_count_var.get())
            if 1 <= count <= 10:
                self.create_member_entries(count)
                self.last_group_spin.config(from_=1, to=max(1, count))
                if int(self.last_group_var.get() or 1) > count:
                    self.last_group_var.set(str(count))
                self.log("已更新为 {} 个组".format(count))
            else:
                messagebox.showwarning("提示", "组数请在 1-10 之间")
        except ValueError:
            messagebox.showwarning("提示", "请输入有效的数字")

    def choose_save_path(self):
        """
        弹出文件选择对话框，让用户选择 Excel 保存位置
        """
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择排班表保存位置"
        )
        if filename:
            self.save_path_var.set(filename)

    def toggle_continue_input(self):
        """
        勾选/取消"接续上一年"时，显示或隐藏"上一年最后组号"输入框
        """
        if self.continue_var.get():
            self.last_group_frame.pack(anchor=tk.W, pady=(8, 0))
        else:
            self.last_group_frame.pack_forget()

    def log(self, msg):
        """
        在运行信息区域追加一行日志
        """
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        # 滚动到底部，让用户看到最新内容
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        # 强制刷新界面，使日志立即显示

    def get_groups_from_input(self):
        """
        从输入框读取组员信息，返回 [['张三','李四'], ['王五','赵六'], ...]
        """
        groups = []
        for i, entry in enumerate(self.member_entries):
            text = entry.get().strip()
            if not text:
                raise ValueError(f"第{i + 1}组未填写组员姓名")
            members = [name.strip() for name in text.split(",") if name.strip()]
            if not members:
                raise ValueError(f"第{i + 1}组组员姓名不能为空")
            groups.append(members)
        return groups

    def generate_schedule(self):
        """
        用户点击"生成排班表"时执行：读取输入 -> 调用 core -> 导出 Excel -> 显示统计
        """
        try:
            self.log("\n-------- 开始生成 --------")

            groups = self.get_groups_from_input()
            self.log(f"共 {len(groups)} 组，组员已录入")

            year = int(self.year_var.get())
            start_month = int(self.start_month_var.get())
            end_month = int(self.end_month_var.get())
            if start_month > end_month:
                raise ValueError("起始月份不能大于结束月份")
            self.log(f"排班时间：{year}年{start_month}月 - {end_month}月")

            h_min, h_max = get_holiday_year_range()
            if year < h_min or year > h_max:
                raise ValueError(
                    f"当前节假日库仅支持 {h_min}-{h_max} 年。"
                    f"{year} 年需等待 chinesecalendar 更新，建议每年11月执行：pip install -U chinesecalendar"
                )

            start_group_index = 0
            if self.continue_var.get():
                last_group = int(self.last_group_var.get())
                if 1 <= last_group <= len(groups):
                    start_group_index = last_group % len(groups)
                    self.log(f"接续上一年，从第{start_group_index + 1}组开始")
                else:
                    self.log("接续组号无效，从第1组开始")

            self.log("正在分析周末和节假日...")
            try:
                schedule_dates = get_all_schedule_dates(year, start_month, end_month)
            except NotImplementedError:
                hmn, hmx = get_holiday_year_range()
                raise ValueError(
                    f"节假日库暂不支持 {year} 年。"
                    f"当前支持 {hmn}-{hmx} 年，建议每年11月执行 pip install -U chinesecalendar 获取最新数据。"
                )
            self.log(f"共找到 {len(schedule_dates)} 个需要排班的日期")

            self.log("正在生成排班表...")
            schedule = create_schedule(groups, schedule_dates, start_group_index)

            default_filename = f"排班表_{year}年{start_month}-{end_month}月.xlsx"
            custom_path = self.save_path_var.get().strip()
            if custom_path:
                # 确保扩展名为 .xlsx
                save_path = custom_path if custom_path.endswith('.xlsx') else custom_path.rstrip('.') + '.xlsx'
            else:
                save_path = os.path.join(get_project_root(), default_filename)

            export_to_excel(schedule, groups, year, start_month, end_month, save_path)

            self.last_filename = save_path
            self.open_btn.config(state=tk.NORMAL)

            self.log("\n排班统计：")
            for i in range(len(groups)):
                total = sum(1 for item in schedule if item["值班组"] == f"第{i + 1}组")
                self.log(f"  第{i + 1}组：共值班 {total} 天")
            if schedule:
                last_item = schedule[-1]
                self.log(f"\n最后值班：{last_item['值班组']}（{last_item['日期'].strftime('%Y年%m月%d日')}）")
                self.log("提示：下次排班时可选择接续此次排班顺序")

            self.log("\n✓ 排班表已成功生成！")
            messagebox.showinfo("完成", f"排班表已保存至：\n{save_path}\n\n点击「打开生成的Excel」可查看。")

        except ValueError as e:
            messagebox.showerror("输入错误", str(e))
            self.log(f"错误：{e}")
        except Exception as e:
            messagebox.showerror("运行错误", str(e))
            self.log(f"错误：{e}")
            import traceback
            traceback.print_exc()

    def open_excel(self):
        """
        用系统默认程序（如 Excel）打开刚才生成的排班表
        os.startfile 在 Windows 下会调用默认关联程序打开文件
        """
        if self.last_filename and os.path.exists(self.last_filename):
            os.startfile(self.last_filename)
        else:
            messagebox.showwarning("提示", "尚未生成排班表，或文件不存在")

    def run(self):
        """
        启动主事件循环，窗口一直显示直到用户关闭
        mainloop 会不断处理用户操作（点击、输入等）
        """
        self.root.mainloop()


def main():
    """
    入口函数：创建 ScheduleApp 实例并运行
    """
    app = ScheduleApp()
    app.run()


if __name__ == "__main__":
    main()
