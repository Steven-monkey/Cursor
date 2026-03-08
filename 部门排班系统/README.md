# 部门排班系统

自动生成周末和法定节假日的值班排班表，适合 Python 初学者学习工程目录和代码结构。

## 快速开始

1. **安装依赖**：`pip install -r requirements.txt`
2. **运行**：双击 `启动排班界面.bat` 或执行 `python run_gui.py`（命令行用 `python run_cli.py`）
3. **生成结果**：`排班表_2024年1-12月.xlsx`

---

## 一、项目结构与目录穿插关系（初学必看）

### 1.1 目录树

```
部门排班系统/                    ← 项目根目录
├── run_gui.py                   ← 图形界面【入口】
├── run_cli.py                   ← 命令行【入口】
├── 启动排班界面.bat              ← 双击它 = 执行 run_gui.py
├── 安装依赖.bat
├── requirements.txt
├── README.md
└── src/                         ← 所有源代码放这里
    └── paiban/                  ← 包（package），Python 通过文件夹名 import
        ├── __init__.py          ← 包标识 + 导出函数
        ├── core.py              ← 核心逻辑（不依赖界面）
        ├── cli.py               ← 命令行逻辑
        └── gui.py               ← 图形界面逻辑
```

### 1.2 调用关系（谁调谁）

```
用户双击 启动排班界面.bat
        ↓
    python run_gui.py
        ↓
    run_gui.py 里：sys.path 加入 src，然后 from paiban.gui import main
        ↓
    paiban.gui 的 main() 被调用
        ↓
    gui.py 里：from .core import get_all_schedule_dates, create_schedule, export_to_excel
        ↓
    用户点「生成排班表」→ 调用 core 的三个函数 → 生成 Excel
```

**命令行同理**：`run_cli.py` → `from paiban.cli import main` → `cli.main()` → `cli` 里 `from .core import ...` → 调用 `core` 的函数。

### 1.3 为什么要这样分层？

| 文件 | 作用 | 被谁用 |
|------|------|--------|
| `core.py` | 纯排班计算，无界面 | `cli` 和 `gui` 都用它，避免重复写逻辑 |
| `cli.py` | 用 `input/print` 交互 | 只有 `run_cli.py` 用 |
| `gui.py` | 用 Tkinter 做窗口 | 只有 `run_gui.py` 用 |
| `__init__.py` | 让 `paiban` 成为包，可被 `from paiban import xxx` | `run_*.py` 不直接用它，但 import 时会执行 |

### 1.4 import 路径说明

- `run_gui.py` 在根目录，`paiban` 在 `src/paiban/`，所以要先 `sys.path.insert(0, 'src')`，Python 才能找到 `paiban`。
- `cli.py` 里写 `from .core import ...`，`.` 表示"同一包下的 core 模块"，即 `src/paiban/core.py`。
- `core.py` 不 import 本项目其他文件，只 import 第三方库，所以它是"最底层"。

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
