"""
演示“批量创建字典（字典列表）”以及批量更新字典中某个字段（工资）的操作。
核心知识点：
1. 列表中每个元素都是一个字典（批量存储多名员工的信息）；
2. 通过 for 循环遍历列表，对每个字典做条件判断并更新字段；
3. 使用 f 字符串（f"...{变量}..."）格式化输出结果。
"""

# 定义一个“员工列表”，列表中的每个元素都是一个员工信息字典
from os import name


employees = [
    {
        "name": "高启强",              # 姓名
        "age": 18,                     # 年龄
        "salary": 5000,                # 基础工资
        "gender": "男",                # 性别
        "job": "程序员",               # 职位
        "hobby": ["足球", "游泳"],     # 爱好（列表）
        "is_lader": True               # 是否是领导（True/False）
    },
    {
        "name": "高启兰",
        "age": 18,
        "salary": 5000,
        "gender": "男",
        "job": "程序员",
        "is_lader": False              # 不是领导
    },
    {
        "name": "高启盛",
        "age": 20,
        "salary": 23000,
        "gender": "男",
        "job": "程序员",
        "hobby": ["羽毛球", "游泳"],
        "is_lader": True
    }
]

# 第一轮：根据是否是领导，批量调整每位员工的工资
for employee in employees:
    # 如果是领导，涨 5000；否则涨 1000
    if employee["is_lader"]:
        employee["salary"] = employee["salary"] + 5000
    else:
        employee["salary"] = employee["salary"] + 1000

    # 使用 f 字符串格式化输出员工姓名和最终薪酬
    # f"...{变量}..."：{} 中放变量或表达式，最终会被替换成对应的值
    print(f"员工名字: {employee['name']} , 最终薪酬: {employee['salary']}")

print("-" * 40)

# 扩展：再遍历一次，筛选出“高薪员工”（例如工资大于 20000 的），并单独打印
# print("高薪员工列表（工资 > 20000）：")
for employee in employees:
    if employee["salary"] > 20000:
        # 再次使用 f 字符串，可以在 {} 中放简单表达式，比如 employee['salary'] * 12 计算年薪
        # print(f"{employee['name']} 的月薪为 {employee['salary']}，年薪约为 {employee['salary'] * 12}")
        print(f"{employee['name']}的月薪为{employee['salary']};他的爱好是{','.join(employee['hobby'])}.")
