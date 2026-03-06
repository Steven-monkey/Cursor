"""
正则表达式示例：手机号、身份证号、邮箱的匹配与验证
"""
import re

# 手机号：11 位，1 开头，第二位 3-9
PHONE_PATTERN = r'^1[3-9]\d{9}$'

# 身份证号：18 位，前 17 位数字，最后一位数字或 X/x
ID_CARD_PATTERN = r'^\d{17}[\dXx]$'

# 邮箱：用户名@域名.后缀
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


def is_valid_phone(text):
    """验证是否为有效手机号"""
    return bool(re.match(PHONE_PATTERN, text))


def is_valid_id_card(text):
    """验证是否为有效 18 位身份证号（仅格式校验，不校验校验码）"""
    return bool(re.match(ID_CARD_PATTERN, text))


def is_valid_email(text):
    """验证是否为有效邮箱"""
    return bool(re.match(EMAIL_PATTERN, text))


# 测试示例
if __name__ == "__main__":
    # 手机号
    print("手机号验证：")
    print(is_valid_phone("13812345678"))   # True
    print(is_valid_phone("12345678901"))   # False（第二位不是 3-9）
    print(is_valid_phone("1381234567"))    # False（位数不足）

    # 身份证号
    print("\n身份证号验证：")
    print(is_valid_id_card("110101199001011234"))  # True
    print(is_valid_id_card("11010119900101123X"))  # True（末位 X）
    print(is_valid_id_card("11010119900101123"))   # False（少一位）

    # 邮箱
    print("\n邮箱验证：")
    print(is_valid_email("test@example.com"))      # True
    print(is_valid_email("user.name+tag@mail.cn")) # True
    print(is_valid_email("invalid@"))              # False
