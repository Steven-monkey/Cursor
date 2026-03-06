# 简单加减乘除计算器（函数版）
# 支持 + - * / 四种运算，可多次使用，输入 q 退出


def add(a, b):
    """加法：返回 a 与 b 的和"""
    return a + b


def subtract(a, b):
    """减法：返回 a 减 b 的差"""
    return a - b


def multiply(a, b):
    """乘法：返回 a 与 b 的积"""
    return a * b


def divide(a, b):
    """除法：返回 a 除以 b 的商，除数为 0 时返回 None"""
    if b == 0:
        return None  # 表示除数为0
    return a / b


def calculate(a, op, b):
    """根据运算符 op 计算 a 和 b，返回结果或 None（表示出错）"""
    if op == "+":
        return add(a, b)
    elif op == "-":
        return subtract(a, b)
    elif op == "*":
        return multiply(a, b)
    elif op == "/":
        return divide(a, b)
    else:
        return None  # 表示无效运算符


# 主循环：持续接收用户输入，直到输入 q 退出
while True:
    # 获取第一个数，若输入 q 则退出程序
    num1_input = input("请输入第一个数 (输入 q 退出): ")
    if num1_input.lower() == "q":
        print("再见！")
        break

    # 将输入转换为浮点数，获取运算符和第二个数
    num1 = float(num1_input)
    op = input("请输入运算符 (+ - * /): ")
    num2 = float(input("请输入第二个数: "))

    # 调用 calculate 函数计算结果
    result = calculate(num1, op, num2)

    # 根据结果输出：None 表示出错，否则打印计算结果
    if result is None:
        if op == "/" and num2 == 0:
            print("错误：除数不能为0")
        else:
            print("错误：无效的运算符")
    else:
        print(f"{num1} {op} {num2} = {result}")
