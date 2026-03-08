#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 上面两行：指定用 python 运行；声明文件编码为 utf-8，支持中文

"""
run_gui.py - 图形界面的启动文件
双击 启动排班界面.bat 或执行 python run_gui.py 时，从这里开始。
"""
import sys   # 系统相关，用到 sys.path
import os    # 操作系统相关，用到路径拼接

# 把 src 目录插入到 Python 的模块搜索路径的最前面（索引 0）
# __file__ 是当前文件 run_gui.py 的路径；abspath 转成绝对路径；dirname 取所在目录；join 和 'src' 拼成完整路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 从 paiban 包的 gui 模块导入 main 函数
from paiban.gui import main

# 只有直接运行本文件时 __name__ 才等于 "__main__"；被其他文件 import 时不会等于
# 这样避免 import 时自动执行 main
if __name__ == "__main__":
    main()  # 调用 main，启动图形界面
