#!/usr/bin/env python
# 这行叫"shebang"，告诉操作系统用 Python 来运行这个文件
# 在 Linux/Mac 上可以直接 ./run_cli.py 执行

# -*- coding: utf-8 -*-
# 声明文件使用 UTF-8 编码，这样才能正确显示中文，避免乱码

"""
run_cli.py - 命令行版本的启动文件
作用：当你运行 python run_cli.py 时，程序从这里开始执行
命令行版 = 没有窗口界面，用户通过键盘输入、屏幕输出来交互
"""

import sys
# 导入 sys 模块：系统相关功能
# 我们会用到 sys.path，它是 Python 查找模块时的搜索路径列表

import os
# 导入 os 模块：操作系统相关功能
# 我们会用到 os.path 来拼接文件路径（例如把 src 加到路径里）

# 把 src 目录添加到 Python 的模块搜索路径的最前面
# 为什么要这样做？因为 paiban 包在 src 目录下，Python 默认不知道去哪里找
# os.path.dirname(...) 取文件所在目录
# os.path.abspath(__file__) 获取 run_cli.py 的绝对路径
# os.path.join(目录, 'src') 把目录和 'src' 拼成完整路径
# sys.path.insert(0, 路径) 把路径插到搜索列表第一位，优先从这里找
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 从 paiban 包的 cli 模块导入 main 函数
# paiban 是包名，cli 是其中的一个模块（cli.py）
# main 是命令行的主入口函数
from paiban.cli import main

# if __name__ == "__main__": 是 Python 的惯用写法
# __name__ 是 Python 的内置变量：直接运行本文件时值为 "__main__"
# 被其他文件 import 时，__name__ 是 "run_cli" 或模块名
# 这样写的好处：只有直接运行 run_cli.py 才执行 main()，被 import 时不会自动执行
if __name__ == "__main__":
    main()
    # 调用 main 函数，进入命令行交互流程
