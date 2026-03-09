# Python基本运算符和表达式
"""我是一个多行注释，我可以注释多行代码"""
# ============================================
# 1. 算术运算符 (用于数学计算)
# ============================================
# print("=== 算术运算符 ===")  # 打印标题
a = 10  # 定义变量a，赋值为10
b = 3   # 定义变量b，赋值为3

print(f"加法: {a} + {b} = {a + b}")  # 加法运算: 10 + 3 = 13
print(f"减法: {a} - {b} = {a - b}")  # 减法运算: 10 - 3 = 7
print(f"乘法: {a} * {b} = {a * b}")  # 乘法运算: 10 * 3 = 30
print(f"除法: {a} / {b} = {a / b}")  # 除法运算: 10 / 3 = 3.333...（结果是小数）
print(f"整除: {a} // {b} = {a // b}")  # 整除运算: 10 // 3 = 3（只保留整数部分）
print(f"取余: {a} % {b} = {a % b}")  # 取余运算: 10 % 3 = 1（10除以3余1）
print(f"幂运算: {a} ** {b} = {a ** b}")  # 幂运算: 10 ** 3 = 1000（10的3次方）

# ============================================
# 2. 比较运算符 (用于比较两个值，结果是True或False)
# ============================================
print("\n=== 比较运算符 ===")  # \n表示换行，打印标题
x = 5  # 定义变量x，赋值为5
y = 8  # 定义变量y，赋值为8

print(f"{x} == {y} 结果: {x == y}")  # 判断x是否等于y，结果是False
print(f"{x} != {y} 结果: {x != y}")  # 判断x是否不等于y，结果是True
print(f"{x} > {y} 结果: {x > y}")   # 判断x是否大于y，结果是False
print(f"{x} < {y} 结果: {x < y}")   # 判断x是否小于y，结果是True
print(f"{x} >= {y} 结果: {x >= y}")  # 判断x是否大于等于y，结果是False
print(f"{x} <= {y} 结果: {x <= y}")  # 判断x是否小于等于y，结果是True

# ============================================
# 3. 赋值运算符 (用于给变量赋值或修改变量的值)
# ============================================
print("\n=== 赋值运算符 ===")  # 打印标题
num = 10  # 定义变量num，赋值为10
print(f"初始值: num = {num}")  # 打印num的初始值

num += 5  # 相当于 num = num + 5，现在num = 15
print(f"num += 5 后: {num}")  # 打印num加5后的值

num -= 3  # 相当于 num = num - 3，现在num = 12
print(f"num -= 3 后: {num}")  # 打印num减3后的值

num *= 2  # 相当于 num = num * 2，现在num = 24
print(f"num *= 2 后: {num}")  # 打印num乘以2后的值

num //= 4  # 相当于 num = num // 4，现在num = 6
print(f"num //= 4 后: {num}")  # 打印num整除4后的值

# ============================================
# 4. 逻辑运算符 (用于组合多个条件判断)
# ============================================
print("\n=== 逻辑运算符 ===")  # 打印标题
age = 20  # 定义年龄变量，赋值为20
has_id = True  # 定义是否有身份证变量，赋值为True（真）

print(f"年龄是 {age}, 有身份证: {has_id}")  # 打印当前的年龄和身份证状态
# and表示"并且"，两个条件都为True时结果才是True
print(f"年龄>=18 and 有身份证: {age >= 18 and has_id}")
print(f"年龄<18 or 有身份证: {age < 18 or has_id}")  # or表示"或者"，只要有一个条件为True结果就是True
print(f"not 有身份证: {not has_id}")  # not表示"取反"，True变False，False变True

# ============================================
# 5. 简单实用案例
# ============================================
print("\n=== 实用案例 ===")  # 打印标题

# 案例1: 计算购物总价
apple_price = 5.5  # 定义苹果单价，每个5.5元
apple_count = 3    # 定义苹果数量，买3个
banana_price = 3.2  # 定义香蕉单价，每个3.2元
banana_count = 5    # 定义香蕉数量，买5个

total = apple_price * apple_count + \
    banana_price * banana_count  # 计算总价：苹果总价 + 香蕉总价
# 打印苹果的小计
print(f"苹果 {apple_count}个 x {apple_price}元 = {apple_price * apple_count}元")
# 打印香蕉的小计
print(f"香蕉 {banana_count}个 x {banana_price}元 = {banana_price * banana_count}元")
print(f"总价: {total}元")  # 打印购物总价

# 案例2: 判断是否及格
score = 75  # 定义考试分数变量，赋值为75分
is_pass = score >= 60  # 判断分数是否大于等于60，结果赋值给is_pass（True表示及格）
print(f"\n考试分数: {score}")  # 打印考试分数
print(f"是否及格: {is_pass}")  # 打印是否及格的判断结果

# 案例3: 计算平均分
math = 85     # 定义数学成绩，85分
chinese = 90  # 定义语文成绩，90分
english = 78  # 定义英语成绩，78分
average = (math + chinese + english) / 3  # 计算平均分：三科总分除以3
print(f"\n数学: {math}, 语文: {chinese}, 英语: {english}")  # 打印三科成绩
print(f"平均分: {average:.2f}")  # 打印平均分，.2f表示保留2位小数

# 案例4: 判断奇偶数
number = 17  # 定义一个数字变量，赋值为17
is_even = number % 2 == 0  # 用取余运算判断：如果除以2余数是0，就是偶数
print(f"\n数字 {number} 是偶数吗? {is_even}")  # 打印判断结果（False表示不是偶数，是奇数）

# 案例5: 温度转换 (摄氏度转华氏度)
celsius = 25  # 定义摄氏温度，25度
fahrenheit = celsius * 9 / 5 + 32  # 摄氏度转华氏度的公式：C * 9 / 5 + 32
print(f"\n{celsius}°C = {fahrenheit}°F")  # 打印转换结果


# 案例6: 我可以找对象吗？
age = 18
money = 10000
print(age and money)
