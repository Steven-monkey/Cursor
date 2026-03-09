employee = {
    "name": "高启强",
    # "age": 18,
    "salary": 5000,
    "gender": "男",
    "job": "程序员",
    "hobby": ["足球", "游泳"]
}
# print(employee["name"])
# print(employee.get("emile","暂无"))
# print(employee.get("age", 19))
# employee 字典中有键值对，可以直接操作和演示
# 添加注释如下：

# 添加一个新键值对 "department"
# employee["department"] = "技术部"   # 新增"department"键，值为"技术部"

# # 修改 "salary" 的值（涨薪）
# employee["salary"] = 6000          # 将 "salary" 修改为6000

# # 删除 "job" 这个键值对
# del employee["job"]                # 删除"job"这一项

# # 打印完整 employee 字典
# print(employee)                    # 输出整个 employee 字典

# 遍历并打印所有键
# for key in employee:
#     print(key)                     # 输出每一个键

# # 遍历并打印所有值
# for value in employee.values():
#     print(value)                   # 输出每一个值

# # 遍历并打印所有的项（键值对）
# for k, v in employee.items():
#     print(k, v)                    # 输出键和值

# # 使用 in 关键字判断某个键是否存在
if "sary" in employee:
    print("有 salary 这个键")  
else: 
    print("无 salary 这个键")

       # 若存在输出对应信息

# # 清空字典内容
# employee.clear()                   # 清空 employee 字典

# # 打印清空后的结果
# print(employee)                    # 输出清空后的 employee
