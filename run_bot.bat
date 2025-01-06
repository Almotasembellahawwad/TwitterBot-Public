@echo off
title Twitter Bot Manager
color 0A

echo ===============================================
echo Twitter Bot Manager
echo Created by: Motasem
echo GitHub: https://github.com/mohasbks
echo ===============================================
echo.

:check_python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.8 or later.
    echo Press any key to exit...
    pause > nul
    exit
)

:check_pip
pip --version > nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed! Please install pip.
    echo Press any key to exit...
    pause > nul
    exit
)

:check_requirements
if not exist requirements.txt (
    echo requirements.txt not found!
    echo Press any key to exit...
    pause > nul
    exit
)

:menu
cls
echo ===============================
echo     Twitter Bot Manager-by Motasem
echo ===============================
echo.
echo [1] Install Requirements
echo [2] Start Bot
echo [3] Exit
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto install_requirements
if "%choice%"=="2" goto start_bot
if "%choice%"=="3" exit

echo Invalid choice! Please try again.
timeout /t 2 > nul
goto menu

:install_requirements
cls
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Requirements installed successfully!
echo Press any key to return to menu...
pause > nul
goto menu

:start_bot
cls
echo [*] Initializing Twitter Bot...
echo [*] Press Ctrl+C to stop the bot
echo.

set /p TWITTER_USERNAME="Enter your Twitter username/email: "
set /p TWITTER_PASSWORD="Enter your Twitter password: "

echo.
echo Starting bot with provided credentials...
python twitter_bot.py %TWITTER_USERNAME% %TWITTER_PASSWORD%

pause
exit
