"""
个人 Class 封装 - 简洁版（用于对比学习）
特点： fewer 方法、更少的代码行，功能相同
"""


# =============================================================================
# Person 人物类 - 简洁版
# =============================================================================
class Person:
    # __init__ 简写：多变量一行赋值，格式为 a,b,c = x,y,z
    def __init__(self, name, age, high, weight):
        self.name, self.age, self.high, self.weight = name, age, high, weight

    # __str__：魔法方法，定义 print(对象) 时自动调用的内容
    # 无需额外写 show_info()，print 对象就能直接输出
    def __str__(self):
        return f"我叫{self.name},今年{self.age}岁,身高{self.high}cm,体重{self.weight}kg"

    # 返回关联的"女朋友"对象
    def get_girlfriend(self, age, high, weight):
        return Person(self.name + "的女朋友", age, high, weight)


# 创建对象并调用：直接用 print(girlfriend)，会自动触发 __str__
person = Person("侯金双", 18, 180, 80)
girlfriend = person.get_girlfriend(18, 170, 60)
print(girlfriend)


# =============================================================================
# Calculator 计算器类 - 简洁版
# =============================================================================
# 思路：用字典把运算符映射到运算，一个方法代替 add/sub/mul/div 四个
class Calculator:
    def __init__(self):
        self.result = 0

    # 用字典 {key: value} 选择运算，[op] 根据传入的 "+" "-" 等取对应结果
    # a // b 是整除，等同于 int(a/b)
    def calc(self, op, a, b):
        self.result = {"+": a + b, "-": a - b, "*": a * b, "/": a // b}[op]
        return self.result


# 调用：统一用 calc("运算符", 数1, 数2)
calc = Calculator()
print("加法结果：", calc.calc("+", 100, 20))
print("减法结果：", calc.calc("-", 100, 20))
print("乘法结果：", calc.calc("*", 100, 20))
print("除法结果：", calc.calc("/", 100, 20))


# =============================================================================
# 对比总结
# =============================================================================
# | 原版                     | 简洁版                     |
# |--------------------------|----------------------------|
# | 属性分行写               | 一行赋值 self.a,self.b=... |
# | show_info() 单独方法     | __str__ 直接用 print()     |
# | add/sub/mul/div 四个方法 | 一个 calc(op,a,b) 搞定     |
# | 代码行数更多             | 代码行数更少               |
