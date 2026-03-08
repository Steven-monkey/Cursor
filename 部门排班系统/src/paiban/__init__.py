"""
__init__.py - 让 paiban 成为一个"包"

有 __init__.py 的文件夹，Python 才认它是一个包，才能写 from paiban import xxx。
当有人 import paiban 或 from paiban.gui import main 时，会先执行这个文件。

这里把 core 里的函数"导出去"，别人可以写 from paiban import create_schedule。
（run_gui 和 run_cli 是直接 from paiban.gui / paiban.cli，不一定会用到这个）
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
