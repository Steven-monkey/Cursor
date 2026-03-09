"""
演示字典的增、删、改、查等常见操作
"""

# 定义一个员工信息字典，包含若干键值对
employee = {
    "name": "高启强",          # 员工姓名
    "age": 18,                # 年龄
    "salary": 5000,           # 月薪
    "gender": "男",           # 性别
    "job": "程序员",          # 职位
    "hobby": ["足球", "游泳"]  # 爱好（列表）
}

# ----------------- 增 / 改 -----------------
# update：一次性更新（或新增）多个键值对
# 如果 key 存在则“修改”，如果 key 不存在则“新增”
# employee.update({"brother": "高启盛", "sister": "高启兰"})
# print(employee)

# pop：根据 key 删除对应的键值对，并返回被删除的 value
# employee.pop("job")
# print(employee)

# clear：清空字典中所有键值对
# employee.clear()
# print(employee)

# del：删除指定 key 的键值对（如果 key 不存在会抛出异常）
# del employee["age"]
# print(employee)

# ----------------- 查 / 设默认值 -----------------
# setdefault：如果 key 不存在，添加该 key，并设置默认值；如果存在，则什么都不做
employee.setdefault("brother")

# 打印 employee 字典，查看所有键值对
print(employee)