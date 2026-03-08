@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 正在安装部门排班系统依赖...
pip install -r requirements.txt
REM pip 安装 requirements.txt 里列出的库
echo.
REM 空一行
echo 安装完成！双击 启动排班界面.bat 即可使用。
pause
REM 暂停，等用户按键才关闭
