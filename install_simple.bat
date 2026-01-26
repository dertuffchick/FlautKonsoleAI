@echo off
chcp 65001 >nul
cls

echo ========================================
echo     FLAUT AI - Простая установка
echo ========================================
echo.

echo Установка Python...
python --version >nul 2>nul
if errorlevel 1 (
    curl -L -o python_install.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
    python_install.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_install.exe
)

echo.
echo Установка зависимостей...
python -m pip install --upgrade pip --quiet
python -m pip install typing-extensions aiohttp websockets g4f requests colorama --quiet

echo.
echo Запуск FLAUT AI...
echo ========================================
python flaut_ai_final.py

pause