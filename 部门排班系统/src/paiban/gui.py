"""
gui.py - 图形界面
做窗口、输入框、按钮，用户点"生成排班表"后调用 core。
"""
import datetime  # 取当前年份
import os       # 路径操作
import tkinter as tk  # 图形界面库，tk 是别名
from tkinter import ttk, messagebox, scrolledtext, filedialog
# ttk 更好看的控件；messagebox 弹窗；scrolledtext 带滚动的文本框；filedialog 选文件

from .core import get_all_schedule_dates, create_schedule, export_to_excel


def get_holiday_year_range():
    """返回节假日库支持的年份范围 (最小年, 最大年)"""
    try:
        from chinese_calendar.constants import holidays  # 节假日数据
        years = {d.year for d in holidays}  # 集合推导，取所有年份
        return min(years), max(years)  # 返回最小和最大
    except Exception:
        return 2004, 2026  # 出错时给默认值


def get_holiday_lib_version():
    """返回 chinesecalendar 的版本号"""
    try:
        import chinese_calendar
        return getattr(chinese_calendar, '__version__', '?')
        # getattr(对象, 属性名, 默认值)：取属性，没有则返回 '?'
    except Exception:
        return '?'


def get_project_root():
    """返回项目根目录路径（Excel 默认存这里）"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # abspath(__file__) 当前文件绝对路径；dirname 取父目录；三次回到项目根


class ScheduleApp:
    """排班系统窗口类"""

    def __init__(self):
        """创建窗口和控件"""
        self.root = tk.Tk()  # 主窗口
        self.root.title("部门排班系统")  # 窗口标题
        self.root.geometry("620x800")   # 初始大小 宽x高
        self.root.minsize(500, 600)    # 最小尺寸
        self.root.resizable(True, True)  # 可否拖拽改变大小

        style = ttk.Style()  # 样式对象
        style.configure("Title.TLabel", font=("Microsoft YaHei UI", 16, "bold"))
        # 配置标题样式：字体、16 号、加粗
        style.configure("Header.TLabel", font=("Microsoft YaHei UI", 11, "bold"))
        style.configure("TLabel", font=("Microsoft YaHei UI", 10))
        style.configure("TButton", font=("Microsoft YaHei UI", 10))

        self.create_widgets()  # 创建所有界面控件

    def create_widgets(self):
        """创建界面上的各个控件"""
        main_frame = ttk.Frame(self.root, padding="15 15 15 15")
        # Frame 容器；padding 四周留空 15 像素
        main_frame.pack(fill=tk.BOTH, expand=True)
        # pack 布局；fill 填满；expand 可扩展

        ttk.Label(main_frame, text="部门值班排班系统", style="Title.TLabel").pack(pady=(0, 20))
        # Label 标签；pack 放入；pady 上下留空
        ttk.Label(main_frame, text="输入组员姓名，一键生成排班表", foreground="gray").pack(pady=(0, 15))
        # foreground 前景色

        group_frame = ttk.LabelFrame(main_frame, text="第一步：设置组数和成员", padding="10")
        # LabelFrame 带标题的框
        group_frame.pack(fill=tk.X, pady=(0, 10))
        # fill=tk.X 横向填满

        ttk.Label(group_frame, text="组数：").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        # grid 网格布局；row/column 行列；sticky 对齐；padx 左右留空
        self.group_count_var = tk.StringVar(value="3")
        # StringVar 绑定到控件，改它控件显示就变
        group_spin = ttk.Spinbox(group_frame, from_=1, to=10, width=5,
                                 textvariable=self.group_count_var, command=self.on_group_count_change)
        # Spinbox 数字选择框；from_/to 范围；command 值变时调用的函数
        group_spin.grid(row=0, column=1, sticky=tk.W)
        ttk.Button(group_frame, text="确认组数", command=self.on_group_count_change).grid(row=0, column=2, padx=(10, 0))
        # Button；command 点击时调用的函数

        self.member_entries_frame = ttk.Frame(group_frame)  # 放组员输入框的容器
        self.member_entries_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=(15, 0))
        # columnspan 跨 3 列；sticky=tk.EW 横向拉伸
        self.member_entries = []  # 存每组的 Entry 控件，后面要读值

        ttk.Label(self.member_entries_frame, text="每组组员用逗号分隔，例如：张三,李四,王五", foreground="gray").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.create_member_entries(3)  # 默认建 3 组的输入框

        time_frame = ttk.LabelFrame(main_frame, text="第二步：选择排班时间范围", padding="10")
        time_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(time_frame, text="年份：").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.year_var = tk.StringVar(value=str(datetime.datetime.now().year))
        # now() 当前时间；year 取年份；str 转字符串
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

        self.continue_var = tk.BooleanVar(value=False)  # 复选框绑定的变量
        ttk.Checkbutton(continue_frame, text="接续上一年排班（新年度排班时可选）", variable=self.continue_var,
                       command=self.toggle_continue_input).pack(anchor=tk.W)
        # Checkbutton 复选框；variable 绑定变量；anchor 对齐

        self.last_group_frame = ttk.Frame(continue_frame)
        self.last_group_frame.pack(anchor=tk.W, pady=(8, 0))
        ttk.Label(self.last_group_frame, text="上一年最后值班的组号：").pack(side=tk.LEFT, padx=(20, 5))
        # side=tk.LEFT 从左往右排
        self.last_group_var = tk.StringVar(value="1")
        self.last_group_spin = ttk.Spinbox(self.last_group_frame, from_=1, to=10, width=5, textvariable=self.last_group_var)
        self.last_group_spin.pack(side=tk.LEFT)
        self.last_group_frame.pack_forget()  # 隐藏这行，勾选接续后才显示

        save_frame = ttk.LabelFrame(main_frame, text="第四步：选择保存位置（可选）", padding="10")
        save_frame.pack(fill=tk.X, pady=(0, 10))
        self.save_path_var = tk.StringVar(value="")
        ttk.Label(save_frame, text="留空则保存在项目根目录").pack(anchor=tk.W)
        path_row = ttk.Frame(save_frame)
        path_row.pack(fill=tk.X, pady=(5, 0))
        self.save_entry = ttk.Entry(path_row, textvariable=self.save_path_var, width=50)
        # Entry 单行输入框
        self.save_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        # expand=True 占据剩余空间
        ttk.Button(path_row, text="浏览...", command=self.choose_save_path, width=8).pack(side=tk.LEFT)

        h_min, h_max = get_holiday_year_range()  # 获取年份范围
        holiday_frame = ttk.LabelFrame(main_frame, text="节假日数据说明", padding="8")
        holiday_frame.pack(fill=tk.X, pady=(0, 10))
        info_text = (
            f"• 当前节假日库版本：chinesecalendar {get_holiday_lib_version()}\n"
            f"• 法定节假日数据支持：{h_min} 年 — {h_max} 年\n"
            "• 国务院一般在每年 11 月发布次年安排，建议届时执行：\n"
            "  pip install -U chinesecalendar  （获取最新节假日数据）"
        )
        # 括号内多行字符串会自动拼接
        self.holiday_info = tk.Text(holiday_frame, height=5, wrap=tk.WORD, font=("Microsoft YaHei UI", 9),
                                    relief=tk.FLAT, borderwidth=0, cursor="arrow")
        # Text 多行文本框；height 行数；wrap 自动换行；relief 边框样式
        self.holiday_info.insert(tk.END, info_text)  # insert 插入文字；tk.END 插入到末尾
        self.holiday_info.config(state=tk.DISABLED)  # 设为只读
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
        # fill=tk.BOTH 填满；expand=True 占据剩余空间

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD, font=("Consolas", 9))
        # ScrolledText 带滚动条
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.insert(tk.END, "请在上方填写组员信息，点击「生成排班表」即可。\n")
        self.log_text.config(state=tk.DISABLED)

        self.last_filename = None  # 存刚生成的 Excel 路径
        self.on_group_count_change()  # 初始化组数相关

    def create_member_entries(self, count):
        """按 count 创建 count 个组员输入框"""
        for widget in self.member_entries_frame.winfo_children():
            # winfo_children() 返回所有子控件
            if widget.winfo_class() == "TFrame":
                # winfo_class() 返回控件类型
                widget.destroy()  # 删除旧控件
        self.member_entries.clear()  # 清空列表

        for i in range(count):
            frame = ttk.Frame(self.member_entries_frame)
            frame.grid(row=i + 1, column=0, sticky=tk.EW, pady=3)
            ttk.Label(frame, text=f"第{i + 1}组：", width=8, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 5))
            # anchor 文字对齐
            entry = ttk.Entry(frame, width=50)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.member_entries.append(entry)  # 存起来后面要 .get()

        self.member_entries_frame.columnconfigure(0, weight=1)
        # columnconfigure 列配置；weight 扩展权重

    def on_group_count_change(self):
        """组数变更时刷新输入框"""
        try:
            count = int(self.group_count_var.get())  # 从控件取字符串转 int
            if 1 <= count <= 10:
                self.create_member_entries(count)
                self.last_group_spin.config(from_=1, to=max(1, count))
                # config 修改控件属性
                if int(self.last_group_var.get() or 1) > count:
                    self.last_group_var.set(str(count))
                    # or 1：空字符串时用 1
                self.log("已更新为 {} 个组".format(count))  # format 格式化
            else:
                messagebox.showwarning("提示", "组数请在 1-10 之间")
        except ValueError:
            messagebox.showwarning("提示", "请输入有效的数字")

    def choose_save_path(self):
        """弹窗让用户选保存路径"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",  # 默认扩展名
            filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择排班表保存位置"
        )
        if filename:  # 用户选了才有值
            self.save_path_var.set(filename)

    def toggle_continue_input(self):
        """勾选/取消接续时，显示或隐藏"上一年最后组号"那行"""
        if self.continue_var.get():  # 勾选
            self.last_group_frame.pack(anchor=tk.W, pady=(8, 0))
        else:
            self.last_group_frame.pack_forget()  # 隐藏

    def log(self, msg):
        """在日志区追加一行"""
        self.log_text.config(state=tk.NORMAL)  # 先改成可编辑
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)  # 滚动到底部
        self.log_text.config(state=tk.DISABLED)  # 改回只读
        self.root.update()  # 强制刷新界面

    def get_groups_from_input(self):
        """从输入框读组员，返回 [['张三','李四'], ...]"""
        groups = []
        for i, entry in enumerate(self.member_entries):
            text = entry.get().strip()  # get() 取输入框内容
            if not text:
                raise ValueError(f"第{i + 1}组未填写组员姓名")
            members = [name.strip() for name in text.split(",") if name.strip()]
            # split 按逗号拆；if name.strip() 过滤空字符串
            if not members:
                raise ValueError(f"第{i + 1}组组员姓名不能为空")
            groups.append(members)
        return groups

    def generate_schedule(self):
        """点"生成排班表"时执行"""
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
                # endswith 判断是否以 .xlsx 结尾；rstrip 去掉右侧的 .
            else:
                save_path = os.path.join(get_project_root(), default_filename)
                # join 拼路径

            export_to_excel(schedule, groups, year, start_month, end_month, save_path)

            self.last_filename = save_path
            self.open_btn.config(state=tk.NORMAL)  # 启用"打开Excel"按钮

            self.log("\n排班统计：")
            for i in range(len(groups)):
                total = sum(1 for item in schedule if item["值班组"] == f"第{i + 1}组")
                # 生成器表达式：符合条件的 item 数
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
            traceback.print_exc()  # 在控制台打印完整错误栈

    def open_excel(self):
        """用系统默认程序打开 Excel"""
        if self.last_filename and os.path.exists(self.last_filename):
            os.startfile(self.last_filename)  # Windows 下打开文件
        else:
            messagebox.showwarning("提示", "尚未生成排班表，或文件不存在")

    def run(self):
        """启动主循环，窗口一直显示"""
        self.root.mainloop()  # mainloop 进入事件循环


def main():
    """入口：创建窗口并运行"""
    app = ScheduleApp()  # 创建 ScheduleApp 实例
    app.run()  # 调用 run 方法


if __name__ == "__main__":
    main()
