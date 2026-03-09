class Persion:
    def __init__(self, name, age, high, weight):
        self.name = name
        self.set_name()

    def say_hello(self):
        print('你好,我的名字是：%s' % self.name)

    def set_name(self):
        self.name = "文人雅士李二狗"


p1 = Persion('张三', 18, 180, 80)
# p1.set_name('李四')
p1.say_hello()
