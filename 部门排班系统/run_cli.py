#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
部门排班系统 - 命令行启动入口

【本文件在项目中的位置】
  - 位于：项目根目录
  - 作用：命令行方式的【入口】，执行 python run_cli.py 时从这里开始
  - 调用链：run_cli.py → paiban.cli.main() → input/print 交互 → 调用 core 生成排班

【与 run_gui.py 的关系】
  - 两个入口，一个调 gui，一个调 cli，但最终都调用 src/paiban/core.py 的排班逻辑
"""
import sys
import os

# 同 run_gui.py，必须把 src 加入路径，才能 import paiban
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from paiban.cli import main

if __name__ == "__main__":
    main()
