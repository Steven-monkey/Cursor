"""
演示 Python 模块的导入与使用。
从 data 模块导入员工列表，从 add_employees_id 模块导入函数，给每位员工添加工号并打印。
"""

# 从 data 模块导入员工列表 employees（定义在 data.py 中）
from data import employees

# 从 add_employees_id 模块导入 add_employees_id 函数（用于给每位员工添加工号，格式如 QSJT-0001）
from add_employees_id import add_employees_id

# 调用 add_employees_id 函数，为员工列表中的每位员工添加工号，并将返回结果赋回 employees
employees = add_employees_id(employees)

# 打印添加工号后的员工列表
for i in employees:
    print(i["工号"])
print(employees[0]['工号'])
