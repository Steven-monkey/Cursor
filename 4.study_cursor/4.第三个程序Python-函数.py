# 4.第三个程序Python-函数.py - Python函数完整教程
# 从基础到高级，逐步学习

# ==================== 第一部分：函数基础 ====================

# 1. 什么是函数？
# 函数是一段可以重复使用的代码块，用来完成特定的任务
# 使用def关键字定义函数

# 你的原始例子：
def get_income(name, day, per_salary):
    """计算员工工资"""
    salary = day * per_salary
    print(f"{name}的工资是：{salary}")
    return salary


# 调用函数
result = get_income("侯金双", 22, 200)
print(f"返回值是：{result}\n")


# 2. 函数的基本结构
def function_name(参数1, 参数2):
    """这是文档字符串，用来说明函数的作用"""
    # 函数体：执行的代码
    result = 参数1 + 参数2
    return result  # 返回值


# 3. 无参数的函数
def greet():
    """简单的问候函数"""
    print("你好！欢迎学习Python函数")


greet()
print()


# 4. 有参数但无返回值的函数
def print_info(name, age):
    """打印用户信息"""
    print(f"姓名：{name}")
    print(f"年龄：{age}")


print_info("张三", 25)
print()


# 5. 有返回值的函数
def add(a, b):
    """返回两个数的和"""
    return a + b


sum_result = add(10, 20)
print(f"10 + 20 = {sum_result}\n")


# ==================== 第二部分：参数的不同类型 ====================

# 6. 位置参数（必须按顺序传递）
def introduce(name, age, city):
    """使用位置参数"""
    print(f"我叫{name}，今年{age}岁，来自{city}")


introduce("李四", 30, "北京")
print()


# 7. 关键字参数（可以不按顺序）
def introduce2(name, age, city):
    """使用关键字参数"""
    print(f"我叫{name}，今年{age}岁，来自{city}")


introduce2(city="上海", name="王五", age=28)
print()


# 8. 默认参数（有默认值的参数）
def make_coffee(size="中杯", sugar=True):
    """制作咖啡"""
    sugar_text = "加糖" if sugar else "不加糖"
    print(f"制作一杯{size}咖啡，{sugar_text}")


make_coffee()  # 使用默认值
make_coffee("大杯", False)  # 覆盖默认值
make_coffee(sugar=False)  # 只改变部分参数
print()


# 9. 可变参数 *args（接收任意数量的位置参数）
def calculate_sum(*numbers):
    """计算任意数量数字的和"""
    total = 0
    for num in numbers:
        total += num
    return total


print(f"求和：{calculate_sum(1, 2, 3)}")
print(f"求和：{calculate_sum(10, 20, 30, 40, 50)}")
print()


# 10. 关键字可变参数 **kwargs（接收任意数量的关键字参数）
def print_user_info(**info):
    """打印用户的所有信息"""
    print("用户信息：")
    for key, value in info.items():
        print(f"  {key}: {value}")


print_user_info(姓名="赵六", 年龄=35, 职位="工程师", 部门="技术部")
print()


# 11. 混合使用不同类型的参数
def complex_function(a, b, *args, default="默认值", **kwargs):
    """演示参数的组合使用"""
    print(f"位置参数 a: {a}, b: {b}")
    print(f"额外位置参数 args: {args}")
    print(f"默认参数 default: {default}")
    print(f"关键字参数 kwargs: {kwargs}")


complex_function(1, 2, 3, 4, 5, default="自定义", name="测试", value=100)
print()


# ==================== 第三部分：返回值 ====================

# 12. 返回单个值
def square(x):
    """返回平方值"""
    return x * x


print(f"5的平方是：{square(5)}\n")


# 13. 返回多个值（实际返回的是元组）
def get_min_max(numbers):
    """返回列表的最小值和最大值"""
    return min(numbers), max(numbers)


min_val, max_val = get_min_max([3, 7, 2, 9, 1, 5])
print(f"最小值：{min_val}，最大值：{max_val}\n")


# 14. 返回不同类型的值
def divide(a, b):
    """除法运算，返回结果或错误信息"""
    if b == 0:
        return None, "除数不能为0"
    return a / b, "成功"


result, message = divide(10, 2)
print(f"结果：{result}，消息：{message}")

result, message = divide(10, 0)
print(f"结果：{result}，消息：{message}\n")


# ==================== 第四部分：作用域 ====================

# 15. 局部变量和全局变量
global_var = "我是全局变量"


def scope_demo():
    """演示变量作用域"""
    local_var = "我是局部变量"
    print(f"函数内部：{global_var}")
    print(f"函数内部：{local_var}")


scope_demo()
print(f"函数外部：{global_var}")
# print(local_var)  # 这行会报错，因为局部变量在函数外不可访问
print()


# 16. 使用global关键字修改全局变量
counter = 0


def increment():
    """修改全局变量"""
    global counter
    counter += 1
    print(f"计数器：{counter}")


increment()
increment()
increment()
print()


# ==================== 第五部分：高级特性 ====================

# 17. 匿名函数（Lambda表达式）
# lambda 参数: 表达式
def multiply(x, y): return x * y


print(f"Lambda函数：5 * 3 = {multiply(5, 3)}")

# Lambda常用于排序、过滤等场景
students = [
    {"name": "小明", "score": 85},
    {"name": "小红", "score": 92},
    {"name": "小刚", "score": 78}
]
students.sort(key=lambda s: s["score"], reverse=True)
print(f"按分数排序：{students}\n")


# 18. 函数作为参数传递
def apply_operation(x, y, operation):
    """接收一个函数作为参数"""
    return operation(x, y)


def add_func(a, b):
    return a + b


def multiply_func(a, b):
    return a * b


print(f"传递加法函数：{apply_operation(5, 3, add_func)}")
print(f"传递乘法函数：{apply_operation(5, 3, multiply_func)}")
print(f"传递Lambda：{apply_operation(5, 3, lambda a, b: a - b)}\n")


# 19. 函数返回函数（闭包）
def create_multiplier(n):
    """创建一个乘法器函数"""
    def multiplier(x):
        return x * n
    return multiplier


times_2 = create_multiplier(2)
times_5 = create_multiplier(5)

print(f"2倍：{times_2(10)}")
print(f"5倍：{times_5(10)}\n")


# 20. 装饰器（高级特性）
def timer_decorator(func):
    """装饰器：测量函数执行时间"""
    import time

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"函数 {func.__name__} 执行时间：{end - start:.6f}秒")
        return result
    return wrapper


@timer_decorator
def slow_function():
    """一个慢速函数"""
    import time
    time.sleep(0.1)
    return "完成"


slow_function()
print()


# 21. 递归函数（函数调用自己）
def factorial(n):
    """计算阶乘：n! = n × (n-1) × ... × 1"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


print(f"5的阶乘：{factorial(5)}")


def fibonacci(n):
    """斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print(f"斐波那契数列前10项：{[fibonacci(i) for i in range(10)]}\n")


# 22. 类型提示（Python 3.5+）
def calculate_salary(name: str, days: int, daily_rate: float) -> float:
    """带类型提示的函数"""
    return days * daily_rate


salary = calculate_salary("员工A", 22, 200.5)
print(f"工资（带类型提示）：{salary}\n")


# ==================== 第六部分：实战练习 ====================

# 23. 综合练习：员工工资管理系统（基于你的原始例子扩展）
def calculate_salary(name, base_days, overtime_hours=0, base_rate=200, overtime_rate=300):
    """
    计算员工工资
    参数：
        name: 员工姓名
        base_days: 基本工作天数
        overtime_hours: 加班小时数（默认0）
        base_rate: 日薪（默认200）
        overtime_rate: 加班时薪（默认300）
    返回：
        总工资
    """
    base_salary = base_days * base_rate
    overtime_salary = overtime_hours * overtime_rate
    total = base_salary + overtime_salary

    print(f"\n{'='*40}")
    print(f"员工：{name}")
    print(f"基本工资：{base_days}天 × {base_rate}元 = {base_salary}元")
    print(f"加班工资：{overtime_hours}小时 × {overtime_rate}元 = {overtime_salary}元")
    print(f"总工资：{total}元")
    print(f"{'='*40}")

    return total


# 使用示例
calculate_salary("侯金双", 22)
calculate_salary("张三", 22, 10)
calculate_salary("李四", 20, 15, base_rate=250, overtime_rate=350)


# 24. 练习：创建一个简单的计算器
def calculator(operation, *numbers):
    """
    多功能计算器
    operation: 'sum', 'avg', 'max', 'min'
    numbers: 任意数量的数字
    """
    if not numbers:
        return "请输入至少一个数字"

    if operation == 'sum':
        return sum(numbers)
    elif operation == 'avg':
        return sum(numbers) / len(numbers)
    elif operation == 'max':
        return max(numbers)
    elif operation == 'min':
        return min(numbers)
    else:
        return "不支持的操作"


print(f"\n计算器演示：")
print(f"求和：{calculator('sum', 1, 2, 3, 4, 5)}")
print(f"平均值：{calculator('avg', 10, 20, 30, 40)}")
print(f"最大值：{calculator('max', 5, 12, 3, 18, 7)}")
print(f"最小值：{calculator('min', 5, 12, 3, 18, 7)}")


# ==================== 学习总结 ====================
"""
Python函数学习路径：

1. 基础概念：
   - 函数定义和调用
   - 参数和返回值
   
2. 参数类型：
   - 位置参数
   - 关键字参数
   - 默认参数
   - *args 和 **kwargs
   
3. 高级特性：
   - Lambda表达式
   - 函数作为参数
   - 闭包
   - 装饰器
   - 递归
   
4. 最佳实践：
   - 使用文档字符串
   - 类型提示
   - 单一职责原则
   - 函数命名规范

继续练习，多写代码，你会越来越熟练！
"""
