@echo off
title Twin AutoClicker - KALRAV 726
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
    set PY=py
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        set PY=python
    ) else (
        echo Python was not found.
        echo Install Python 3.11+ from https://www.python.org/downloads/
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PY% -m venv .venv
)

echo Installing dependency...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt

echo Starting Twin AutoClicker...
.venv\Scripts\python.exe autoclicker.py
