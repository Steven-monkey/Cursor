# 0.1 + 0.2 在二进制中无法精确表示，会产生 0.30000000000000004 这类误差
# 用 round(..., 1) 四舍五入到 1 位小数，即可得到 0.3
# print(round(0.1 + 0.2, 1))

from decimal import Decimal
a = Decimal("0.1212")
b= Decimal("0.2233")
print(a + b)