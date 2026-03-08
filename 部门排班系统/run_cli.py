#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 指定用 python 运行；声明编码 utf-8

"""
run_cli.py - 命令行的启动文件
执行 python run_cli.py 时，从这里开始。
"""
import sys   # 用到 sys.path.insert
import os    # 用到路径操作

# 同 run_gui.py：把 src 加入搜索路径，这样 Python 才能找到 paiban
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 从 paiban 包的 cli 模块导入 main 函数
from paiban.cli import main

# 直接运行本文件时才执行
if __name__ == "__main__":
    main()  # 调用 main，进入命令行交互
