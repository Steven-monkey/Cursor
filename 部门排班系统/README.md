# 部门排班系统

自动生成周末和法定节假日的值班排班表，适合 Python 初学者学习工程目录和代码结构。

## 快速开始

1. **安装依赖**：`pip install -r requirements.txt`
2. **运行**：双击 `启动排班界面.bat` 或执行 `python run_gui.py`（命令行用 `python run_cli.py`）
3. **生成结果**：`排班表_2024年1-12月.xlsx`

---

## 一、项目结构（初学必看）

### 目录长什么样

```
部门排班系统/
├── run_gui.py        ← 点窗口时，从这开始
├── run_cli.py        ← 打命令行时，从这开始
├── 启动排班界面.bat   ← 双击 = 运行 run_gui.py
├── 安装依赖.bat
├── requirements.txt
└── src/
    └── paiban/       ← 真正的代码在这
        ├── __init__.py  包要有这个文件
        ├── core.py      算排班、导出Excel（核心）
        ├── cli.py       命令行那一套
        └── gui.py       窗口那一套
```

### 谁调谁

```
双击 启动排班界面.bat
  → python run_gui.py
  → run_gui.py 把 src 加进路径，然后 from paiban.gui import main
  → main() 打开窗口
  → 用户点「生成排班表」
  → gui 调用 core 里的函数（get_all_schedule_dates、create_schedule、export_to_excel）
  → 生成 Excel
```

命令行同理：`run_cli` 调 `cli`，`cli` 调 `core`。

### 为什么分 core、cli、gui？

- **core**：只算排班，不管窗口还是打字。cli 和 gui 都用它，不用写两遍。
- **cli**：黑窗口，用 input/print。
- **gui**：有按钮有输入框。
- **__init__.py**：有这个文件，paiban 才算一个"包"，才能 from paiban import xxx。

### 关于 import

- `run_gui.py` 在根目录，`paiban` 在 `src/paiban/`，所以要先 `sys.path.insert(0, 'src')`，Python 才能找到。
- `cli`、`gui` 里写 `from .core import ...`，`.` 表示"同一个包里的 core"。

---

## 二、主要功能

- 识别周末、法定节假日，自动排除调休日
- 劳动节/国庆节分段安排，连休固定同一组
- 每组每月不超过 4 天，避免连续值班
- 可接续上一年的排班顺序

## 技术栈

- Python 3.6+
- pandas、xlsxwriter（Excel）
- chinese_calendar（节假日）

代码里已有详细注释，适合边看边学。
