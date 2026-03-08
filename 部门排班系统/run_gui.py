#!/usr/bin/env python
# 这行叫"shebang"，告诉操作系统用 Python 来运行这个文件

# -*- coding: utf-8 -*-
# 声明文件使用 UTF-8 编码，支持中文显示

"""
run_gui.py - 图形界面版本的启动文件
作用：执行 python run_gui.py 或双击 启动排班界面.bat 时，从这里开始
GUI = Graphical User Interface，即有窗口、按钮、输入框的界面
"""

import sys
# 导入 sys 模块，用于修改 sys.path（模块搜索路径）

import os
# 导入 os 模块，用于路径操作（拼接、获取目录等）

# 把 src 目录插入到 Python 模块搜索路径的最前面（索引 0）
# 这样 import paiban 时，Python 才能找到 src/paiban 这个包
# __file__：当前脚本的路径
# os.path.abspath(__file__)：转为绝对路径
# os.path.dirname(...)：取所在目录（部门排班系统）
# os.path.join(目录, 'src')：拼成 部门排班系统/src 的完整路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 从 paiban 包的 gui 模块导入 main 函数
# gui 模块负责图形界面，main 是界面的启动函数
from paiban.gui import main

# 直接运行本文件时 __name__ 等于 "__main__"
# 被其他文件 import 时 __name__ 是 "run_gui"
# 避免 import 时自动启动窗口
if __name__ == "__main__":
    main()
    # 调用 main，创建并显示排班系统的图形界面窗口
