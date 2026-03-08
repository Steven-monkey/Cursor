#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_gui.py - 图形界面的启动文件

双击 启动排班界面.bat 或执行 python run_gui.py 时，从这里开始。

流程：先把 src 加到 Python 的搜索路径 -> 然后 from paiban.gui import main -> 执行 main()
为什么要把 src 加进去？因为 paiban 在 src/paiban/ 里，不加的话 Python 找不到。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from paiban.gui import main

if __name__ == "__main__":
    main()
