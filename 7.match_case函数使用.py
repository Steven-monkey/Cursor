# 最简单的 match-case 示例（Python 3.10+）

fruit = "苹果"

match fruit:
    case "苹果":
        print("你选了苹果")
    case "香蕉":
        print("你选了香蕉")
    case "橙子":
        print("你选了橙子")
    case _:
        print("未知水果")
