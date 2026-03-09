"""
================================================================================
个人 Class 封装 - 带详细注释版
================================================================================
本文件包含 Person 人物类 和 Calculator 计算器类
每一行代码都有详细解释，帮助理解封装的完整流程
"""


# =============================================================================
# 一、Person 人物类
# =============================================================================

# class 是关键字，用来定义一个「类」（可以理解为对象的模板）
# Persion 是类名（注意：英文正确拼写是 Person，这里是沿用原名）
class Persion:

    # def 定义函数，__init__ 是特殊方法名，创建对象时 Python 会自动调用
    # self：代表「当前对象本身」，必须是第一个参数
    # name, age, high, weight：创建对象时需要传入的 4 个参数
    def __init__(self, name, age, high, weight):

        # self.name：给当前对象添加一个属性叫 name
        # = name：把传入的 name 参数的值赋给这个属性
        self.name = name

        # self.age：对象的年龄属性，保存传入的 age 值
        self.age = age

        # self.high：对象的身高属性，单位 cm
        self.high = high

        # self.weight：对象的体重属性，单位 kg
        self.weight = weight

    # show_info 是普通方法，用来打印这个人的基本信息
    # self 必须写，这样方法才能访问 self.name、self.age 等属性
    def show_info(self):

        # print：内置函数，在控制台输出内容
        # f"..."：f-string 格式化字符串，{} 里的变量会被替换成实际值
        # 例如 self.name 是 "侯金双"，则 {self.name} 显示为 侯金双
        print(
            f"我叫{self.name},今年{self.age}岁,身高{self.high}cm,体重{self.weight}kg"
        )

    # get_girlfriend：创建一个「女朋友」对象并返回
    # age, high, weight：女朋友的年龄、身高、体重（姓名会来自 self.name）
    def get_girlfriend(self, age, high, weight):

        # return：结束方法并返回一个值
        # Persion(...)：调用 Persion 的构造函数，创建一个新的 Persion 对象
        # self.name + "的女朋友"：字符串拼接，例如 "侯金双" + "的女朋友" = "侯金双的女朋友"
        return Persion(self.name + "的女朋友", age, high, weight)


# -----------------------------------------------------------------------------
# 调用 Person 类
# -----------------------------------------------------------------------------

# Persion("侯金双", 18, 180, 80)：根据类创建对象，会执行 __init__
# 把创建的对象赋值给变量 persion，之后用 persion 来操作这个对象
persion = Persion("侯金双", 18, 180, 80)

# persion.get_girlfriend(18, 170, 60)：调用对象的 get_girlfriend 方法
# 传入 18, 170, 60 作为女朋友的年龄、身高、体重
# 返回值是一个新的 Persion 对象，存入变量 girlfriend
girlfriend = persion.get_girlfriend(18, 170, 60)

# girlfriend.show_info()：对女朋友对象调用 show_info，在控制台打印她的信息
girlfriend.show_info()


# =============================================================================
# 二、Calculator 计算器类 - 写法一：每次运算传入参数
# =============================================================================

# 定义计算器类
class Calculator:

    # __init__ 没有额外参数，只初始化 result
    def __init__(self):
        # self.result：用来存储每次计算的结果，初始为 0
        self.result = 0

    # add 方法：计算 a + b
    # self：对象本身；a, b：要相加的两个数
    def add(self, a, b):
        # 把 a+b 的结果存到 self.result，同时返回
        self.result = a + b
        return self.result

    # sub 方法：计算 a - b
    def sub(self, a, b):
        self.result = a - b
        return self.result

    # mul 方法：计算 a * b
    def mul(self, a, b):
        self.result = a * b
        return self.result

    # div 方法：计算 a / b，返回整数部分
    def div(self, a, b):
        # a / b 得到浮点数，int() 转为整数（会截断小数）
        self.result = a / b
        return int(self.result)

    # show_result：打印当前存储在 self.result 中的值
    def show_result(self):
        print(f"计算结果是:{self.result}")


# 注意：下面第二个 Calculator 类会覆盖上面的定义
# 所以实际运行的是下面的 Calculator（写法二）


# =============================================================================
# 三、Calculator 计算器类 - 写法二：创建时传入两个数，方法不再传参
# =============================================================================
# 这种写法：先把 a、b 存到对象里，运算时直接用 self.a 和 self.b

class Calculator:

    # __init__ 接收 a、b 两个参数，在创建对象时就保存
    def __init__(self, a, b):
        # 初始化结果为 0
        self.result = 0
        # self.a：把传入的第一个数存到对象里
        self.a = a
        # self.b：把传入的第二个数存到对象里
        self.b = b

    # add：用对象里的 self.a 和 self.b 做加法，不需要再传参数
    def add(self):
        self.result = self.a + self.b
        return self.result

    # sub：用 self.a - self.b
    def sub(self):
        self.result = self.a - self.b
        return self.result

    # mul：用 self.a * self.b
    def mul(self):
        self.result = self.a * self.b
        return self.result

    # div：用 self.a // self.b，// 是整除运算符，直接得到整数
    def div(self):
        self.result = self.a // self.b
        return self.result

    # show_result：打印 self.result
    def show_result(self):
        print(f"计算结果是:{self.result}")


# -----------------------------------------------------------------------------
# 调用 Calculator 类（写法二）
# -----------------------------------------------------------------------------

# Calculator(100, 20)：创建对象，执行 __init__(self, 100, 20)
# 即 self.a=100, self.b=20
cla = Calculator(100, 20)

# cla.add()：调用 add 方法，内部用 self.a + self.b，即 100 + 20 = 120
print("加法结果：", cla.add())

# cla.sub()：100 - 20 = 80
print("减法结果：", cla.sub())

# cla.mul()：100 * 20 = 2000
print("乘法结果：", cla.mul())

# cla.div()：100 // 20 = 5（整除）
print("除法结果：", cla.div())
