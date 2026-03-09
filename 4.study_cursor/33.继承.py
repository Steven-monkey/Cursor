"""
================================================================================
Python 继承 - 学习示例（带详细注释）
================================================================================
继承：子类可以继承父类的属性和方法，不用重复写，还能添加自己的东西
"""


# =============================================================================
# 示例一： Father 父类 + Son 子类（在原有基础上扩展）
# =============================================================================

# 父类：Father，定义「父亲」的通用属性
class Father:
    def __init__(self, name, money, car, house):
        self.name = name
        self.money = money
        self.car = car
        self.house = house


# Son 继承 Father：括号里写 Father 表示继承
# Son 自动拥有 name、money、car、house，还能加自己的 game
class Son(Father):
    def __init__(self, name, money, car, house, game):
        # super().__init__()：先调用父类的 __init__，初始化 name/money/car/house
        super().__init__(name, money, car, house)
        # 子类自己的属性
        self.game = game


# 创建父类对象
f1 = Father("老王", "一个亿", "劳斯莱斯", "house")
# 创建子类对象，多传一个 game
s1 = Son("小王", "一个亿", "劳斯莱斯", "house", "英雄联盟")
# 子类对象可以访问父类的属性
print(s1.money)   # 输出：一个亿
print(s1.game)    # 输出：英雄联盟


# =============================================================================
# 示例二：方法继承 + 方法重写
# =============================================================================

class Animal:
    def __init__(self, name):
        self.name = name

    # 父类方法：默认「在叫」
    def speak(self):
        print(f"{self.name} 在叫")


# Dog 继承 Animal，重写 speak 方法
class Dog(Animal):
    def speak(self):
        # 子类覆盖父类：狗叫「汪汪汪」
        print("汪汪汪！")


# Cat 继承 Animal，也重写 speak
class Cat(Animal):
    def speak(self):
        print("喵喵喵！")


dog = Dog("小黑")
cat = Cat("小白")
dog.speak()  # 汪汪汪！（用子类重写后的方法）
cat.speak()  # 喵喵喵！
print(dog.name)  # 小黑（继承自父类的属性）


# =============================================================================
# 示例三：子类添加父类没有的新方法
# =============================================================================

class Person:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print(f"{self.name} 说：你好")


# Student 继承 Person，添加 study 方法
class Student(Person):
    def study(self):
        print(f"{self.name} 在学习")


stu = Student("小明")
stu.say_hi()   # 继承自父类
stu.study()    # 子类自己的方法
