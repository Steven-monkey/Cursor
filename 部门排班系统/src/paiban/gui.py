"""
部门排班系统 - 图形界面

【本文件在项目中的位置】
  - 位于：src/paiban/gui.py
  - 作用：用 Tkinter 做窗口，用户填组员、选时间，点"生成排班表"后调用 core 完成排班
  - 被谁调用：只有 run_gui.py，通过 from paiban.gui import main
  - 调用谁：from .core import ... 调用 core.py 的三个函数

【与 cli 的区别】
  - cli：用 input() 读、print() 写，一次流程跑完就退出
  - gui：用窗口、输入框、按钮，用户点按钮才触发 generate_schedule，可多次生成
"""

import datetime
import os
import tkinter as tk  # Python 自带的图形界面库
from tkinter import ttk, messagebox, scrolledtext, filedialog

# 从同包的 core 导入排班相关函数，gui 只负责界面，计算全交给 core
from .core import get_all_schedule_dates, create_schedule, export_to_excel


def get_holiday_year_range():
    """获取 chinesecalendar 库支持的年份范围，用于在界面上提示用户"""
    try:
        from chinese_calendar.constants import holidays
        years = {d.year for d in holidays}  # 集合推导式，取出所有年份
        return min(years), max(years)
    except Exception:
        return 2004, 2026  # 失败时给一个默认范围


def get_holiday_lib_version():
    """获取 chinesecalendar 的版本号"""
    try:
        import chinese_calendar
        return getattr(chinese_calendar, '__version__', '?')  # 取 __version__ 属性，没有则返回 '?'
    except Exception:
        return '?'


def get_project_root():
    """获取项目根目录（部门排班系统所在文件夹），用于默认保存路径"""
    # __file__ 是当前文件路径，abspath 转绝对路径，dirname 取所在目录
    # 三次 dirname：gui.py -> paiban -> src -> 部门排班系统
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ScheduleApp:
    """
    排班系统图形界面主类

    用 class 定义"应用"这个对象，里面包含窗口、按钮、输入框等，
    以及用户点击按钮时要做的事（方法）。
    """

    def __init__(self):
        """初始化：创建主窗口，设置大小、标题，创建所有控件"""
        self.root = tk.Tk()  # 主窗口
        self.root.title("部门排班系统")
        self.root.geometry("620x800")   # 窗口大小 宽x高
        self.root.minsize(500, 600)    # 最小尺寸
        self.root.resizable(True, True)  # 允许用户拖拽调整大小

        # ttk.Style 用来设置控件样式（字体、颜色等）
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 16, "bold"))  # 标题大号加粗
        style.configure("Header.TLabel", font=("Microsoft YaHei UI", 11, "bold"))
        style.configure("TLabel", font=("Microsoft YaHei UI", 10))
        style.configure("TButton", font=("Microsoft YaHei UI", 10))

        self.create_widgets()  # 创建界面上的各种控件

    def create_widgets(self):
        """创建界面上的所有控件：标题、输入框、按钮、日志区等"""
        main_frame = ttk.Frame(self.root, padding="15 15 15 15")  # 主容器，四周留白
        main_frame.pack(fill=tk.BOTH, expand=True)  # pack 布局，填满并扩展

        # ----- 标题 -----
        ttk.Label(main_frame, text="部门值班排班系统", style="Title.TLabel").pack(pady=(0, 20))
        ttk.Label(main_frame, text="输入组员姓名，一键生成排班表", foreground="gray").pack(pady=(0, 15))

        # ----- 第一步：组数和成员 -----
        group_frame = ttk.LabelFrame(main_frame, text="第一步：设置组数和成员", padding="10")
        group_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(group_frame, text="组数：").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.group_count_var = tk.StringVar(value="3")  # 绑定到控件的变量，改它就改显示
        group_spin = ttk.Spinbox(group_frame, from_=1, to=10, width=5,
                                 textvariable=self.group_count_var, command=self.on_group_count_change)
        group_spin.grid(row=0, column=1, sticky=tk.W)
        ttk.Button(group_frame, text="确认组数", command=self.on_group_count_change).grid(row=0, column=2, padx=(10, 0))

        self.member_entries_frame = ttk.Frame(group_frame)  # 组成员输入框的容器
        self.member_entries_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=(15, 0))
        self.member_entries = []  # 存储每组的输入框，后面好取用户输入

        ttk.Label(self.member_entries_frame, text="每组组员用逗号分隔，例如：张三,李四,王五", foreground="gray").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.create_member_entries(3)  # 默认创建 3 组的输入框

        # ----- 第二步：时间范围 -----
        time_frame = ttk.LabelFrame(main_frame, text="第二步：选择排班时间范围", padding="10")
        time_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(time_frame, text="年份：").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.year_var = tk.StringVar(value=str(datetime.datetime.now().year))  # 默认当年
        ttk.Spinbox(time_frame, from_=2004, to=2035, width=8, textvariable=self.year_var).grid(row=0, column=1, sticky=tk.W)

        ttk.Label(time_frame, text="起始月份：").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(8, 0))
        self.start_month_var = tk.StringVar(value="1")
        ttk.Spinbox(time_frame, from_=1, to=12, width=5, textvariable=self.start_month_var).grid(row=1, column=1, sticky=tk.W, pady=(8, 0))

        ttk.Label(time_frame, text="结束月份：").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=(8, 0))
        self.end_month_var = tk.StringVar(value="12")
        ttk.Spinbox(time_frame, from_=1, to=12, width=5, textvariable=self.end_month_var).grid(row=2, column=1, sticky=tk.W, pady=(8, 0))
        ttk.Label(time_frame, text="支持 2004-2035 年，法定节假日数据随 chinesecalendar 库更新", foreground="gray").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(4, 0))

        # ----- 第三步：接续设置 -----
        continue_frame = ttk.LabelFrame(main_frame, text="第三步：是否接续上一年的排班顺序（可选）", padding="10")
        continue_frame.pack(fill=tk.X, pady=(0, 10))

        self.continue_var = tk.BooleanVar(value=False)  # 复选框绑定的变量
        ttk.Checkbutton(continue_frame, text="接续上一年排班（新年度排班时可选）", variable=self.continue_var,
                       command=self.toggle_continue_input).pack(anchor=tk.W)

        self.last_group_frame = ttk.Frame(continue_frame)  # 接续时显示的"上一年最后组号"
        self.last_group_frame.pack(anchor=tk.W, pady=(8, 0))
        ttk.Label(self.last_group_frame, text="上一年最后值班的组号：").pack(side=tk.LEFT, padx=(20, 5))
        self.last_group_var = tk.StringVar(value="1")
        self.last_group_spin = ttk.Spinbox(self.last_group_frame, from_=1, to=10, width=5, textvariable=self.last_group_var)
        self.last_group_spin.pack(side=tk.LEFT)
        self.last_group_frame.pack_forget()  # 默认隐藏，勾选接续后才显示

        # ----- 第四步：保存路径 -----
        save_frame = ttk.LabelFrame(main_frame, text="第四步：选择保存位置（可选）", padding="10")
        save_frame.pack(fill=tk.X, pady=(0, 10))
        self.save_path_var = tk.StringVar(value="")
        ttk.Label(save_frame, text="留空则保存在项目根目录").pack(anchor=tk.W)
        path_row = ttk.Frame(save_frame)
        path_row.pack(fill=tk.X, pady=(5, 0))
        self.save_entry = ttk.Entry(path_row, textvariable=self.save_path_var, width=50)
        self.save_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(path_row, text="浏览...", command=self.choose_save_path, width=8).pack(side=tk.LEFT)

        # ----- 节假日说明 -----
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
        self.holiday_info.insert(tk.END, info_text)
        self.holiday_info.config(state=tk.DISABLED)  # 只读，用户不能改
        self.holiday_info.pack(fill=tk.X)

        # ----- 按钮 -----
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 10))

        self.generate_btn = ttk.Button(btn_frame, text="生成排班表", command=self.generate_schedule)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.open_btn = ttk.Button(btn_frame, text="打开生成的Excel", command=self.open_excel, state=tk.DISABLED)
        self.open_btn.pack(side=tk.LEFT)  # 生成成功后才启用

        # ----- 日志输出区 -----
        log_frame = ttk.LabelFrame(main_frame, text="运行信息", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.insert(tk.END, "请在上方填写组员信息，点击「生成排班表」即可。\n")
        self.log_text.config(state=tk.DISABLED)

        self.last_filename = None  # 记录本次生成的文件路径，方便"打开Excel"
        self.on_group_count_change()  # 初始化接续组号范围

    def create_member_entries(self, count):
        """根据组数创建/刷新组成员输入框"""
        for widget in self.member_entries_frame.winfo_children():  # 遍历容器里所有子控件
            if widget.winfo_class() == "TFrame":
                widget.destroy()  # 先删掉旧的
        self.member_entries.clear()

        for i in range(count):
            frame = ttk.Frame(self.member_entries_frame)
            frame.grid(row=i + 1, column=0, sticky=tk.EW, pady=3)
            ttk.Label(frame, text=f"第{i + 1}组：", width=8, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 5))
            entry = ttk.Entry(frame, width=50)  # 单行输入框
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.member_entries.append(entry)

        self.member_entries_frame.columnconfigure(0, weight=1)  # 让列可扩展

    def on_group_count_change(self):
        """用户修改组数或点击"确认组数"时调用，刷新输入框"""
        try:
            count = int(self.group_count_var.get())
            if 1 <= count <= 10:
                self.create_member_entries(count)
                self.last_group_spin.config(from_=1, to=max(1, count))  # 接续组号范围跟着变
                if int(self.last_group_var.get() or 1) > count:
                    self.last_group_var.set(str(count))
                self.log("已更新为 {} 个组".format(count))
            else:
                messagebox.showwarning("提示", "组数请在 1-10 之间")
        except ValueError:
            messagebox.showwarning("提示", "请输入有效的数字")

    def choose_save_path(self):
        """点击"浏览"时弹出文件选择框，让用户选保存位置"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择排班表保存位置"
        )
        if filename:
            self.save_path_var.set(filename)

    def toggle_continue_input(self):
        """勾选/取消"接续上一年"时，显示或隐藏"上一年最后组号"输入"""
        if self.continue_var.get():
            self.last_group_frame.pack(anchor=tk.W, pady=(8, 0))
        else:
            self.last_group_frame.pack_forget()  # 隐藏

    def log(self, msg):
        """在界面下方的日志区输出一行文字"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state=tk.DISABLED)
        self.root.update()  # 强制刷新界面，让用户看到进度

    def get_groups_from_input(self):
        """从界面上的输入框读取各组组员，转成 core 需要的 groups 格式"""
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
        点击"生成排班表"时执行

        【逻辑流程】
            1. get_groups_from_input：从界面输入框读组员
            2. 读年份、起止月份、是否接续
            3. get_all_schedule_dates（core）：得到需要排班的日期列表
            4. create_schedule（core）：生成排班结果
            5. export_to_excel（core）：写入 Excel
            6. log 统计信息，弹窗提示完成
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
                save_path = custom_path if custom_path.endswith('.xlsx') else custom_path.rstrip('.') + '.xlsx'
            else:
                save_path = os.path.join(get_project_root(), default_filename)

            export_to_excel(schedule, groups, year, start_month, end_month, save_path)

            self.last_filename = save_path
            self.open_btn.config(state=tk.NORMAL)  # 启用"打开Excel"按钮

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
            traceback.print_exc()  # 在终端打印完整错误栈，方便调试

    def open_excel(self):
        """点击"打开生成的Excel"时，用系统默认程序打开文件"""
        if self.last_filename and os.path.exists(self.last_filename):
            os.startfile(self.last_filename)  # Windows 下用默认程序打开
        else:
            messagebox.showwarning("提示", "尚未生成排班表，或文件不存在")

    def run(self):
        """启动主循环，窗口会一直显示直到用户关闭"""
        self.root.mainloop()


def main():
    """程序的入口：创建应用并运行"""
    app = ScheduleApp()
    app.run()


if __name__ == "__main__":
    main()
