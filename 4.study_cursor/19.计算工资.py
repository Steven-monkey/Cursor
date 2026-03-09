employees = [
    {
        "name": "高启强",              # 姓名
        "age": 18,                     # 年龄
        "salary": 5000,                # 基础工资
        "gender": "男",                # 性别
        "job": "程序员",               # 职位
        "hobby": ["足球", "游泳"],     # 爱好（列表）
        "is_lader": True,
        "bonus": 200.2232432      # 是否是领导（True/False）
    },
    {
        "name": "高启兰",
        "age": 18,
        "salary": 5000,
        "gender": "男",
        "job": "程序员",
        "is_lader": False,
        "bonus": 2000.2243343      # 不是领导
    },
    {
        "name": "高启盛",
        "age": 20,
        "salary": 23000,
        "gender": "男",
        "job": "程序员",
        "hobby": ["羽毛球", "游泳"],
        "is_lader": True,
        "bonus": 600.223434
    }
]


def calc_total_salary(employee):
    """计算员工应发工资（salary + bonus），精确到两位小数"""
    total = employee['salary'] + employee['bonus']
    return round(total, 2)


for employee in employees:
    total = calc_total_salary(employee)
    print(f"{employee['name']}的工资是: {total:.2f}")
