"""
__init__.py - 包初始化文件
作用：让 paiban 文件夹成为 Python 的"包"（package）
有 __init__.py 的文件夹，Python 才会把它当作包，才能用 from paiban import xxx
"""

# 从同包的 core 模块导入三个函数
# 这里的 . 表示"当前包"（即 paiban）
# 这样别人可以写：from paiban import get_all_schedule_dates
from .core import (
    get_all_schedule_dates,  # 根据年月获取需要排班的所有日期（周末+节假日）
    create_schedule,         # 根据组和日期生成完整的排班表
    export_to_excel,         # 把排班表导出为 Excel 文件
)

# __all__ 定义"用 from paiban import * 时导出哪些名字"
# 星号导入会只导入这里列出的三个函数，不会导入其他内部名字
# 这样可以让包的对外接口更清晰
__all__ = [
    "get_all_schedule_dates",
    "create_schedule",
    "export_to_excel",
]
