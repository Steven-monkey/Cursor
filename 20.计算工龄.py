"""
计算工龄 + 生成随机抽奖码
1. 根据入职日期与当前日期，计算工龄（支持 floor/ceil/round 三种取整方式）
2. 生成指定长度的随机抽奖码（大写字母 + 数字）
"""

from datetime import datetime
from math import ceil, floor
import random
import string

# ----------------- 计算工龄 -----------------
# 入职日期（年, 月, 日）
company_in = datetime(2019, 1, 1)
# 当前日期时间
current_now = datetime.now()

# 计算入职到今天的时间差（timedelta 对象），.days 可获取天数
delta = current_now - company_in
print(delta)

# 工龄（年）= 天数 ÷ 365（浮点数）
work_years = delta.days / 365

# floor：向下取整（不足整年不计，如 5.8 年 → 5 年）
print(f"工龄: {floor(work_years)} 年")
# ceil：向上取整（不足整年按 1 年计，如 5.2 年 → 6 年）
print(f"工龄: {ceil(work_years)} 年")
# round：四舍五入（5.4 → 5，5.6 → 6）
print(f"工龄: {round(work_years)} 年")

# ----------------- 生成随机抽奖码 -----------------


def generate_lottery_code(length=12):
    """
    生成指定长度的随机抽奖码（大写字母 + 数字）
    :param length: 抽奖码长度，默认 12 位
    :return: 随机字符串
    """
    chars = string.ascii_uppercase + string.digits  # A-Z 和 0-9
    return ''.join(random.choices(chars, k=length))  # 随机选 length 个字符并拼接


lottery_code = generate_lottery_code()
print(f"12位随机抽奖码：{lottery_code}")