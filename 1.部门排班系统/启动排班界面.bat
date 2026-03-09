@echo off
REM 不显示后面的命令本身，只显示输出
chcp 65001 >nul
REM 设为 UTF-8 编码，>nul 不显示切换信息
cd /d "%~dp0"
REM 切换到 bat 所在目录；%~dp0 是 bat 文件所在路径
echo 正在启动部门排班系统...
python run_gui.py
REM 执行 run_gui.py
if errorlevel 1 pause
REM 如果出错（返回值>=1），暂停以便看到错误信息
