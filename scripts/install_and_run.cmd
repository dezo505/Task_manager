@echo off
python --version >nul 2>&1
IF ERRORLEVEL 1 (exit /b)
pip --version >nul 2>&1
IF ERRORLEVEL 1 (exit /b)
pip install -r requirements.txt
python ../main.py
@echo on
