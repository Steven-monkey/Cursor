#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_cli.py - 命令行的启动文件

执行 python run_cli.py 时，从这里开始。流程和 run_gui 类似，只是最后调的是 cli 不是 gui。
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from paiban.cli import main

if __name__ == "__main__":
    main()
