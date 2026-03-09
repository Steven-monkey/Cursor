"""
口语规范化工具
功能：将文本中的口语化表达替换为规范的书面语
示例：90后 -> 九零后，一会 -> 一会儿
"""
# 上面三行是「文档字符串」：用三个引号包住，说明这个程序是干什么的，给别人看或自己以后看

import re
# import = 导入、引入
# re = Python 自带的「正则表达式」模块，用来做「查找并替换」文字

# 下面定义一个「字典」：口语词 -> 规范词 的对应关系
# REPLACE_MAP 是变量名：REPLACE=替换，MAP=映射表，全称就是「替换映射表」
REPLACE_MAP = {
    # 年代表达：数字+后 -> 汉字+后
    "90后": "九零后",
    "00后": "零零后",
    "80后": "八零后",
    "70后": "七零后",
    # 时间/程度
    "一会": "一会儿",
    "一会会": "一会儿",
    # 疑问词
    "啥": "什么",
    "干嘛": "干什么",
    "咋": "怎么",
    "咋样": "怎么样",
    # 程度/语气
    "挺好": "很好",
    "有点儿": "有些",
    "有点": "有些",
    # 语气词：嘛 -> 吗
    "可以嘛": "可以吗",
    "不是嘛": "不是吗",
}
# 字典用 { } 包住，每项是 "键": "值" ，键=要被换掉的词，值=换成的词


def normalize_text(text: str) -> str:
# def = 定义函数（把一段逻辑包成一个可以重复调用的「功能」）
# normalize_text = 函数名，意思是「规范化文本」
# (text: str) = 参数：text 是传入的一串文字，: str 表示「类型是字符串」
# -> str = 返回值类型：这个函数会返回一个字符串
    """
    将句子中的口语化词语替换为较为规范的书面表达。

    Args:
        text: 待规范化的原始文本

    Returns:
        规范化后的文本
    """
    result = text
    # result = 结果。先把用户输入的 text 复制给 result，后面会在 result 上做替换

    for spoken, formal in REPLACE_MAP.items():
    # for ... in ... = 循环：把 REPLACE_MAP 里每一项都做一遍
    # .items() = 取出字典里所有的「键和值」成对
    # spoken = 口语词（键），formal = 规范词（值）
        pattern = re.escape(spoken)
        # pattern = 模式、匹配规则
        # re.escape() = 把字符串里的特殊符号转义，这样在正则里不会被当成「通配符」等
        result = re.sub(pattern, formal, result)
        # re.sub(要找的, 换成什么, 在哪儿找) = 在 result 里把 pattern 替换成 formal

    return result
    # return = 返回。把替换好的 result 作为函数的「结果」交出去


def main():
# def main(): = 定义主函数 main，程序的主要流程写在这里
    """主函数：提供交互式命令行界面，支持连续输入并规范化。"""
    print("口语规范化小工具（输入空行退出）")
    # print() = 在屏幕上打印一段文字，提示用户怎么用

    while True:
    # while True = 无限循环：条件永远为真，所以会一直执行下面的代码，直到遇到 break
        s = input("请输入一句话：").strip()
        # input() = 等待用户在键盘输入，括号里是提示语
        # .strip() = 去掉字符串两端的空格、换行等空白字符
        # s = 用户输入的那一句话，存到变量 s 里

        if not s:
        # if not s = 如果 s 是空的（用户直接按回车没打字）
            print("已退出。")
            break
            # break = 跳出 while 循环，程序结束
        print("规范表达：", normalize_text(s))
        # normalize_text(s) = 调用前面写的函数，把 s 规范化
        # 整行：先规范化 s，再和 "规范表达：" 一起打印出来


if __name__ == "__main__":
# __name__ = Python 给每个文件的一个特殊变量
# 当你「直接运行」这个 .py 文件时，__name__ 的值是 "__main__"
# 这样写的意思是：只有「直接运行这个文件」时才执行下一行，被别的文件 import 时不会自动跑
    main()
    # 调用 main 函数，程序从这里真正开始执行
