"""
================================================================================
Python 属性权限问题 - 详细注释版
================================================================================
Python 用命名约定区分「公开」「半私有」「私有」属性，但本质上都能被访问。
"""


# class：关键字，定义名为 Persion 的类
class Persion:

    # def __init__：构造函数，创建对象时自动执行
    # self：代表当前对象
    def __init__(self):
        # self.public：公开属性，无下划线，任何地方都可直接访问
        self.public = 1

        # self._semi：半私有属性，单下划线开头，约定表示「仅供内部使用」
        # 仍可直接访问，无强制限制，只是提醒开发者谨慎使用
        self._semi = 2

        # self.__hide：私有属性，双下划线开头，触发 Python 名称改写
        # 实际存为 _Persion__hide，外部访问需知道改写后的名字
        self.__hide = 3
        self.change_hide()
    # def change_hide：普通方法，用来修改 __hide 的值
    def change_hide(self):
        # 类内部可直接写 self.__hide，Python 会自动解析为 _Persion__hide
        self.__hide = 6666666


# per = Persion()：调用类创建对象，自动执行 __init__
per = Persion()
# per.change_hide()：调用方法，把 __hide 从 3 改为 4
# per.change_hide()
# print(per.public)：访问公开属性并打印
print(per.public)
# print(per._semi)：访问半私有属性并打印
print(per._semi)
# print(per._Persion__hide)：访问「私有」属性必须用改写后的名字 _类名__属性名
print(per._Persion__hide)


# public：无下划线，公开属性
# _semi：单下划线，约定为半私有
# __hide：双下划线，触发名称改写，实际为 _Persion__hide
# 同时修正了之前“public 是单下划线”的错误表述，并给 per.change_hide() 加上了注释说明。
