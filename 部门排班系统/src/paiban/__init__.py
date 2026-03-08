"""
部门排班系统 - paiban 包

【本文件在项目中的位置】
  - 位于：src/paiban/__init__.py
  - 作用：让 paiban 成为 Python 包。有 __init__.py 的文件夹才能被 import
  - 执行时机：当有人写 from paiban import xxx 或 from paiban.gui import main 时，会先执行本文件

【目录穿插关系】
  - run_gui.py 写 from paiban.gui import main 时，Python 会：
    1. 找到 src/paiban/ 文件夹
    2. 执行本文件 __init__.py
    3. 再加载 gui.py
  - cli 和 gui 都从 .core 导入函数，所以本文件把 core 的函数"再导出"一次，
    这样外部也可以写 from paiban import create_schedule（可选，目前 run_*.py 没用）
"""
from .core import (
    get_all_schedule_dates,
    create_schedule,
    export_to_excel,
)

__all__ = [
    "get_all_schedule_dates",
    "create_schedule",
    "export_to_excel",
]
