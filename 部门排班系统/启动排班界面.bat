@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在启动部门排班系统...
python 排班系统界面.py
if errorlevel 1 pause
