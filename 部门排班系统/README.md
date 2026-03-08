# 部门排班系统

自动生成周末和法定节假日的值班排班表，适合 Python 初学者学习工程目录和代码结构。本 README 会详细介绍项目用到的所有 Python 基础知识。

---

## 一、快速开始

1. **安装依赖**：`pip install -r requirements.txt`
2. **运行**：双击 `启动排班界面.bat` 或执行 `python run_gui.py`（命令行用 `python run_cli.py`）
3. **生成结果**：`排班表_2024年1-12月.xlsx`

---

## 二、项目结构

### 目录树

```
部门排班系统/
├── run_gui.py         ← 图形界面入口
├── run_cli.py         ← 命令行入口
├── 启动排班界面.bat    ← 双击 = 运行 run_gui.py
├── 安装依赖.bat
├── requirements.txt   ← 依赖列表
└── src/
    └── paiban/        ← 核心代码包
        ├── __init__.py
        ├── core.py    ← 排班逻辑
        ├── cli.py     ← 命令行
        └── gui.py     ← 图形界面
```

### 调用关系

```
run_gui.py  →  from paiban.gui import main  →  main()  →  用户点按钮  →  调用 core 的函数
run_cli.py  →  from paiban.cli import main  →  main()  →  调用 core 的函数
```

### 为什么分 core、cli、gui？

- **core**：纯计算，不依赖窗口或命令行。cli 和 gui 都用它，避免重复写逻辑。
- **cli**：用 `input()` / `print()` 交互。
- **gui**：用 Tkinter 做窗口。

---

## 三、Python 基础用法（本项目涉及的）

下面按「语法 → 本项目里的例子」来说明，方便对照代码学习。

### 3.1 变量与数据类型

| 概念 | 说明 | 项目中的例子 |
|------|------|--------------|
| **变量** | 名字 = 值，用来存东西 | `group_count = 3`、`schedule_dates = []` |
| **整数 int** | 1, 2, 2024 | `year = 2024`、`start_month = 1` |
| **字符串 str** | 用引号包起来 | `"周末"`、`"第1组"` |
| **列表 list** | `[]`，可放多个元素，用逗号隔开 | `groups = []`、`['周一','周二',...]` |
| **元组 tuple** | `()`，不可改的序列 | `(d, date_type)` 表示「日期 + 类型」 |
| **字典 dict** | `{键: 值}`，按键取值 | `{'日期': date, '值班组': '第1组'}` |
| **布尔 bool** | `True` / `False` | `is_weekend`、`can_assign` |

### 3.2 运算符

| 运算符 | 含义 | 例子 |
|--------|------|------|
| `=` | 赋值 | `x = 1` |
| `==` | 相等 | `if x == 1` |
| `!=` | 不相等 | `if x != 0` |
| `>`, `<`, `>=`, `<=` | 大小比较 | `if 1 <= x <= 10` |
| `%` | 取余数 | `(assigned_group + 1) % len(groups)` 实现循环 |
| `and` | 并且 | `is_weekend and is_workday` |
| `or` | 或者 | `is_weekend or is_holiday` |
| `not` | 取反 | `not is_weekend` |
| `in` | 是否在里面 | `d.weekday() in [5, 6]`、`date in period_dates` |

### 3.3 字符串

| 用法 | 说明 | 例子 |
|------|------|------|
| `"..." * 数字` | 重复 | `"=" * 50` → 50 个等号 |
| `f"..."` | 在字符串里插入变量 | `f"第{i+1}组"`、`f"共 {len(x)} 个"` |
| `.strip()` | 去掉首尾空格 | `input().strip()` |
| `.lower()` | 转小写 | `"Y".lower()` → `"y"` |
| `.split(',')` | 按逗号拆成列表 | `"张三,李四".split(',')` → `['张三','李四']` |
| `.join()` | 用某字符连接列表 | `'、'.join(['张三','李四'])` → `"张三、李四"` |

### 3.4 列表

| 用法 | 说明 | 例子 |
|------|------|------|
| `[]` | 空列表 | `schedule_dates = []` |
| `lst.append(x)` | 在末尾加一个元素 | `schedule_dates.append((d, date_type))` |
| `lst[-1]` | 最后一个元素 | `schedule[-1]` |
| `len(lst)` | 列表长度 | `len(groups)` |
| `lst.clear()` | 清空 | `self.member_entries.clear()` |
| `[x for x in ...]` | 列表推导式 | `[name.strip() for name in members.split(',')]` |
| `{x for x in ...}` | 集合推导式 | `{d.year for d in holidays}` |

### 3.5 字典

| 用法 | 说明 | 例子 |
|------|------|------|
| `{}` | 空字典 | `group_month_count = {}` |
| `d[key]` | 取值 | `schedule['值班组']` |
| `d.get(key, 默认值)` | 取值，没有就返回默认值 | `group_month_count.get(month_key, 0)` |
| `key in d` | 键是否存在 | `if period_id in period_assigned` |
| `d.items()` | 键值对 | `for month_key, days_needed in month_days.items()` |

### 3.6 控制流程

| 语法 | 说明 | 例子 |
|------|------|------|
| `if 条件:` | 条件成立时执行 | `if is_makeup_workday: continue` |
| `elif 条件:` | 否则如果 | `elif is_weekend and not is_holiday:` |
| `else:` | 否则 | `else: return None` |
| `for x in 序列:` | 遍历 | `for dt in pd.date_range(...)` |
| `for i, x in enumerate(序列):` | 遍历时同时得到下标 | `for i, (date, date_type) in enumerate(...)` |
| `continue` | 跳过本次循环 | `if ...: continue` |
| `break` | 跳出循环 | `if not can_assign: break` |

### 3.7 函数

| 语法 | 说明 | 例子 |
|------|------|------|
| `def 名(参数):` | 定义函数 | `def get_user_input():` |
| `return 值` | 返回值 | `return schedule_dates` |
| `return a, b, c` | 一次返回多个值 | `return groups, year, start_month, ...` |
| `参数=默认值` | 默认参数 | `def create_schedule(..., start_group_index=0)` |

### 3.8 异常处理

| 语法 | 说明 | 例子 |
|------|------|------|
| `try: ...` | 尝试执行 | `try: year = int(...)` |
| `except 异常类型 as e:` | 捕获某种错误 | `except ValueError as e:` |
| `except Exception as e:` | 捕获任意错误 | `except Exception as e:` |

### 3.9 模块与 import

| 用法 | 说明 | 例子 |
|------|------|------|
| `import 模块` | 导入整个模块 | `import datetime` |
| `from 模块 import 名` | 只导入某几个名字 | `from .core import create_schedule` |
| `from 模块 import 名 as 别名` | 导入并改名 | `import pandas as pd` |
| `.` 在 import 里 | 同一包下的模块 | `from .core import ...` 表示同包里的 core |
| `__name__ == "__main__"` | 只有「直接运行」本文件时为真 | `if __name__ == "__main__": main()` |

### 3.10 类（class）

| 概念 | 说明 | 项目中的例子 |
|------|------|--------------|
| `class 类名:` | 定义类 | `class ScheduleApp:` |
| `def __init__(self):` | 初始化，创建对象时自动执行 | `def __init__(self):` |
| `self.xxx` | 实例属性 | `self.root`、`self.group_count_var` |

### 3.11 常用内置函数

| 函数 | 说明 | 例子 |
|------|------|------|
| `int(x)` | 转成整数 | `int(input("..."))` |
| `str(x)` | 转成字符串 | `str(datetime.datetime.now().year)` |
| `len(x)` | 长度 | `len(groups)` |
| `range(n)` | 0 到 n-1 | `for i in range(5)` |
| `min(a,b)`, `max(a,b)` | 最小、最大 | `min(years), max(years)` |
| `any(序列)` | 任一为 True 则 True | `any(... for date in period_dates)` |
| `getattr(obj, 属性, 默认)` | 取对象属性 | `getattr(chinese_calendar, '__version__', '?')` |

---

## 四、第三方库（本项目用到的）

### 4.1 datetime

处理日期。

```python
datetime.date(2024, 1, 1)           # 创建日期
date.weekday()                      # 0-6，5=周六 6=周日
date.strftime('%Y-%m-%d')           # 格式化为 "2024-01-06"
date - 另一个date                   # 得到天数差
timedelta(days=1)                   # 表示 1 天
```

### 4.2 pandas

处理表格、生成日期序列、写 Excel。

```python
pd.date_range(start=..., end=..., freq='D')  # 按天生成日期
pd.DataFrame(列表或字典)                      # 建表格
df["列名"]                                  # 取一列
df.to_excel(...)                            # 写入 Excel
pd.concat([a, b], ignore_index=True)        # 拼表格
```

### 4.3 chinese_calendar

判断中国节假日、调休。

```python
chinese_calendar.is_holiday(date)   # 是否法定节假日
chinese_calendar.is_workday(date)   # 是否工作日（含调休）
```

### 4.4 tkinter（Python 自带）

做图形界面。

```python
tk.Tk()                    # 主窗口
ttk.Label(父, text="...")  # 文字
ttk.Entry(父)              # 输入框
ttk.Button(父, text="...", command=函数)  # 按钮，command 是点击时调用的函数
ttk.Spinbox(父, from_=1, to=10)    # 数字选择框
tk.StringVar(value="3")    # 绑定到控件的变量
frame.pack() / frame.grid(row=0, column=0)  # 布局
messagebox.showinfo("标题", "内容")  # 弹窗
filedialog.asksaveasfilename(...)   # 选保存路径
```

---

## 五、常用 os、sys 用法

| 用法 | 说明 | 项目中的例子 |
|------|------|--------------|
| `sys.path.insert(0, 路径)` | 把路径加入模块搜索路径 | `sys.path.insert(0, 'src')` |
| `os.path.abspath(__file__)` | 当前文件的绝对路径 | 用于算项目根目录 |
| `os.path.dirname(路径)` | 取路径的父目录 | 多次 dirname 回到项目根 |
| `os.path.join(a, b)` | 拼路径 | `os.path.join(根目录, 文件名)` |
| `os.path.exists(路径)` | 文件是否存在 | `os.path.exists(self.last_filename)` |
| `os.startfile(路径)` | 用默认程序打开文件 | 打开 Excel |

---

## 六、requirements.txt 说明

```
chinesecalendar==1.9.1   # 中国节假日
pandas>=2.0.0            # 表格、Excel
xlsxwriter>=3.0.0        # pandas 写 xlsx 用的引擎
```

安装：`pip install -r requirements.txt`

---

## 七、学习路径建议

1. 先跑一遍：双击 `启动排班界面.bat`，填数据生成一次排班表。
2. 从 `run_gui.py` 看起：只有十几行，理解「入口」和 `import`。
3. 看 `core.py`：先看 `get_all_schedule_dates`、`create_schedule` 的流程。
4. 看 `cli.py`：理解 `input`、`print`、`try-except`。
5. 看 `gui.py`：理解 `class`、`tkinter` 控件、`command` 回调。
6. 对照本文「三、Python 基础用法」在代码里找对应写法。

---

## 八、排班规则简要

- 只排周末和法定节假日，自动排除调休日。
- 劳动节、国庆节拆成两段（前期/后期）。
- 连休假期同一组值，普通周末轮流。
- 每组每月不超过 4 天，不连续值班。
- 可接续上一年的排班顺序。

---

## 九、常见问题

**Q：双击 bat 没反应？**  
A：先执行 `安装依赖.bat`，确保 Python 和依赖都装好。

**Q：年份超出范围？**  
A：节假日库一般支持 2004–2026 年，每年 11 月可执行 `pip install -U chinesecalendar` 更新。

**Q：Excel 在哪？**  
A：默认在项目根目录，文件名如 `排班表_2024年1-12月.xlsx`。
