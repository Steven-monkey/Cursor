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
        self._semi = 2
        # self.__hide：私有属性，双下划线开头，会触发 Python 名称改写（存为 _Persion__hide）
        self.__hide = 3
        # 在 __init__ 里调用 change_hide，创建对象时就把 __hide 改为 6666666
        self.change_hide()

    # def change_hide：普通方法，用来修改 __hide 的值
    def change_hide(self):
        # 类内部可直接写 self.__hide，Python 会自动解析为 _Persion__hide
        self.__hide = 6666666


# per = Persion()：创建对象，执行 __init__ → 先设 public/_semi/__hide，再调用 change_hide
per = Persion()
# print(per.public)：访问公开属性，输出 1
print(per.public)
# print(per._semi)：访问半私有属性，输出 2
print(per._semi)
# print(per._Persion__hide)：访问私有属性必须用改写后的名字，输出 6666666
print(per._Persion__hide)
