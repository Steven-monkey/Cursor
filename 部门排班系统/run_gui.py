#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部门排班系统 - 图形界面启动入口

【本文件在项目中的位置】
  - 位于：项目根目录
  - 作用：程序的【入口】之一，用户双击 启动排班界面.bat 或执行 python run_gui.py 时，Python 会从这里开始执行
  - 调用链：run_gui.py → paiban.gui.main() → 图形界面弹出

【目录穿插关系】
  - 本文件在根目录，而核心代码在 src/paiban/ 里
  - Python 默认只在"当前目录"和"已安装的包"里找 import，找不到 src/paiban
  - 所以要先 sys.path.insert(0, 'src')，把 src 加入搜索路径，这样写 from paiban.gui import main 才能找到
"""
import sys
import os

# 把 src 目录加入 Python 的模块搜索路径
# __file__ 是当前文件路径，dirname 取所在目录，join 拼出 部门排班系统/src
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# 从 paiban 包的 gui 模块导入 main 函数，然后执行
# paiban 对应 src/paiban/ 文件夹，gui 对应 gui.py 文件
from paiban.gui import main

# 只有直接运行本文件时（而不是被其他文件 import 时）才执行 main
if __name__ == "__main__":
    main()
