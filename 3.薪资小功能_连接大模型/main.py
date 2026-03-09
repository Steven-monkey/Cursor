import os  # 导入 Python 标准库 os，用来访问环境变量、路径等系统相关功能（这里主要用来拿 API Key）
import textwrap  # 导入 textwrap 库，用来整理多行字符串的缩进，让输出更好看

import pandas as pd  # 导入第三方库 pandas，并简写为 pd，用来读 Excel、处理表格数据
from openai import OpenAI  # 从 openai 包中导入 OpenAI 类，用来创建 DeepSeek 的客户端对象


# =========================
# 一、基础配置
# =========================

"""
使用说明：
1）DEEPSEEK_API_KEY：在系统环境变量里设置你的 DeepSeek API 密钥（比如在 PowerShell 里：$env:DEEPSEEK_API_KEY="你的密钥"）。
2）Excel 文件路径：确保下面 EXCEL_PATH 指向的路径和实际 Excel 文件位置一致。
3）运行本文件后：终端会提示你输入问题，你输入关于工资的中文问题即可。
"""

# Excel 文件的相对路径（字符串），程序通过它找到工资表
EXCEL_PATH = "薪资小功能_连接大模型/salary_slips_leader.xlsx"

# DeepSeek 使用的模型名字（字符串），"deepseek-chat" 是对话模型
DEEPSEEK_MODEL = "deepseek-chat"


# =========================
# 二、工具函数
# =========================


def load_salary_excel(excel_path: str) -> pd.DataFrame:
    """
    读取工资 Excel 文件。

    参数：
        excel_path: Excel 文件路径，类型是 str（字符串）。

    返回：
        DataFrame 对象（pandas 提供的表格数据结构，可以看成“内存里的 Excel 表”）。
    """
    # pd.read_excel：pandas 提供的读 Excel 文件的函数
    # 参数 excel_path：要读取的文件路径
    # 参数 engine="openpyxl"：指定用 openpyxl 这个引擎来读 .xlsx 文件
    return pd.read_excel(excel_path, engine="openpyxl")


def build_context_from_df(df: pd.DataFrame, max_rows: int = 50) -> str:
    """
    把 DataFrame（表格）里的前 max_rows 行，拼接成一段文字，
    作为大模型的“背景知识”。

    注意：大模型看不到 Excel 文件本身，只能看到我们给它的纯文本。
    """
    # df.head(max_rows)：从表格开头取前 max_rows 行，避免一次性内容太多
    small_df = df.head(max_rows)

    # small_df.to_string(index=False)：把这部分表格转成纯文本形式，index=False 表示不显示行号
    table_str = small_df.to_string(index=False)

    # 下面用一个多行 f 字符串，把说明文字 + 表格文本拼接起来
    # f""" ... {max_rows} ... {table_str} ... """：
    #   - f 表示这是一个“格式化字符串”，里面可以用 {变量名} 把变量值插进去
    context_text = f"""
    下方是一张工资相关的 Excel 表格的部分数据（最多显示前 {max_rows} 行）。
    每一行代表一个人的某个月工资记录，包含多列信息（例如：姓名、部门、月份、基本工资、奖金等）。
    请在回答用户问题时，把这张表当作事实依据，根据表里的数据来回答。
    如果表里没有足够信息，请说明“表中没有相关记录”。

    表格内容如下（纯文本展示）：

    {table_str}
    """

    # textwrap.dedent：去掉多行字符串左侧多余的缩进
    # .strip()：再去掉字符串首尾多余的空白（空格、换行）
    return textwrap.dedent(context_text).strip()


def init_deepseek_client() -> OpenAI:
    """
    创建 DeepSeek 客户端对象。

    返回：
        OpenAI 类型的 client，用来后面发起聊天请求。
    """
    # os.environ.get("DEEPSEEK_API_KEY")：
    #   从系统环境变量里取名为 "DEEPSEEK_API_KEY" 的值（也就是你的密钥）
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    # 用拿到的 api_key 和 DeepSeek 的 base_url 创建客户端对象
    client = OpenAI(
        api_key=api_key,  # 把密钥作为 api_key 参数传入
        base_url="https://api.deepseek.com",  # DeepSeek 官方提供的接口地址
    )

    # 返回这个客户端对象，后面调用 ask_deepseek 时会用到
    return client


def ask_deepseek(client: OpenAI, context_text: str, user_question: str) -> str:
    """
    调用 DeepSeek 模型：
    把“表格内容的文字版本 + 用户的问题”一起发给模型，拿到回答。

    参数：
        client: init_deepseek_client 创建出来的 OpenAI 客户端。
        context_text: 由 build_context_from_df 生成的表格说明文本。
        user_question: 用户在命令行里输入的问题（中文字符串）。

    返回：
        模型返回的回答内容（字符串）。
    """
    # messages：这是 Chat Completions 接口要求的“对话历史”参数
    # 它是一个列表（[]），里面每一项是一个字典（{}），表示一条消息
    messages = [
        {
            "role": "system",  # role 表示“说话的身份”，system 用来给模型定规则和角色
            "content": (
                # content 是具体的说明文字，这里用小括号包起来，方便多行拼接
                "你是一个工资表助手。你只能根据我给你的工资 Excel 表中展示的数据来回答问题，"
                "不要自己编造表里没有的信息。如果表中没有对应记录，要如实说明。"
                "回答请使用简体中文，语气尽量友好、简洁。"
            ),
        },
        {
            "role": "user",  # 这一条消息的身份是“用户”
            "content": (
                "下面是工资 Excel 表的部分内容（以文本形式给出）：\n\n"
                f"{context_text}\n\n"  # 把表格的文字内容插进去
                "用户的问题是：\n"
                f"{user_question}\n\n"  # 把用户的问题插进去
                "请根据上面给出的表格内容，回答这个问题。"
            ),
        },
    ]

    # client.chat.completions.create(...)：
    #   调用 DeepSeek 的“聊天补全”接口，生成回答
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,  # 指定使用哪个模型，这里用上面配置的 "deepseek-chat"
        messages=messages,  # 把刚刚准备好的对话内容传进去
        stream=False,  # 不使用流式返回，一次性拿到完整回答，写法更简单
    )

    # response.choices[0]：
    #   模型可能会返回多个“候选回答”，这里我们只取第一个
    # .message.content：
    #   从这个候选回答对象里拿出真正的文本内容
    return response.choices[0].message.content


# =========================
# 三、主程序入口
# =========================


def main():
    """
    程序主入口（主流程）：
      1. 读取 Excel 表格
      2. 构造“表格文字说明”（给模型看的文本）
      3. 初始化 DeepSeek 客户端
      4. 读取用户问题，调用模型并打印回答
    """

    # 第 1 步：读取 Excel 文件，得到 df（DataFrame 对象）
    df = load_salary_excel(EXCEL_PATH)

    # 第 2 步：把 df 转成文字说明（只取前 50 行，避免太长）
    context_text = build_context_from_df(df, max_rows=50)

    # 第 3 步：创建 DeepSeek 客户端，用于后续请求
    client = init_deepseek_client()

    # 第 4 步：从命令行读取用户输入的问题
    # input("请输入你的问题：")：在终端显示提示文字，并等待用户输入一行内容
    # .strip()：去掉输入内容前后多余的空格和换行
    user_question = input("请输入你的问题：").strip()

    # 调用上面的 ask_deepseek 函数，把客户端、上下文、问题传进去，拿到回答字符串
    answer = ask_deepseek(client, context_text, user_question)

    # 打印一个标题行，\n 表示换行
    print("\n模型回答：\n")

    # 再打印具体的回答内容
    print(answer)


# 下面这段 if 是 Python 里很常见的“入口判断”写法：
# - __name__ 是一个内置变量，当前文件被“直接运行”时，它的值是 "__main__"
# - 如果当前文件只是被别的文件 import，这里的 main() 不会自动执行
if __name__ == "__main__":
    # 只有在“直接运行本文件”时，才会调用 main() 开始整个流程
    main()
