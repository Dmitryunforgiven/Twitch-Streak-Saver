@echo off

:: set variables
set VENV_DIR=./streak
set CHROMEDRIVER_PATH=./chromedriver.exe
set SCRIPT_PATH=./main.py

:: start python venv
call %VENV_DIR%\Scripts\activate

:: setting chromedriver path
set PATH=%CHROMEDRIVER_PATH%;%PATH%

:: running the main script
python %SCRIPT_PATH%

:: deactivating venv if the script exits
deactivate