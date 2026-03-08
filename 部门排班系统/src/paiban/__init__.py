"""
__init__.py - 让 paiban 成为一个"包"
有 __init__.py 的文件夹，Python 才认为它是一个包。
"""
# from .core 表示从同包的 core 模块导入；. 代表当前包
from .core import (
    get_all_schedule_dates,  # 获取要排班的所有日期
    create_schedule,         # 生成排班表
    export_to_excel,         # 导出到 Excel
)

# __all__ 定义"用 from paiban import * 时导出哪些名字"
__all__ = [
    "get_all_schedule_dates",
    "create_schedule",
    "export_to_excel",
]
