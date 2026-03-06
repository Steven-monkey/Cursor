# 帮我周一到周日吃什么的内容写一个if 多分支判断功能

def what_to_eat(day):
    """根据星期几返回当天吃什么"""
    if day == 1:
        print("周一：吃点清淡的，粥配小菜")
    elif day == 2:
        print("周二：来碗牛肉面，补充能量")
    elif day == 3:
        print("周三：周三吃点饺子，百吃不厌")
    elif day == 4:
        print("周四：炒菜配米饭，家的味道")
    elif day == 5:
        print("周五：周末前夜，火锅走起！")
    elif day == 6:
        print("周六：休息日，烧烤啤酒安排")
    elif day == 7:
        print("周日：养生汤，迎接新的一周")
    else:
        print("请输入 1-7 之间的数字")


def what_to_eat_match(day):
    """根据星期几返回当天吃什么（match-case 写法，Python 3.10+）"""
    match day:
        case 1:
            print("周一：吃点清淡的，粥配小菜")
        case 2:
            print("周二：来碗牛肉面，补充能量")
        case 3:
            print("周三：周三吃点饺子，百吃不厌")
        case 4:
            print("周四：炒菜配米饭，家的味道")
        case 5:
            print("周五：周末前夜，火锅走起！")
        case 6:
            print("周六：休息日，烧烤啤酒安排")
        case 7:
            print("周日：养生汤，迎接新的一周")
        case _:
            print("请输入 1-7 之间的数字")


# 测试
what_to_eat_match(10)   # 周一
