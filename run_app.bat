@echo off
chcp 65001 > nul
title بورصة الوحيد Pro - EGX
color 0A

echo.
echo  ╔═══════════════════════════════════════════╗
echo  ║                                           ║
echo  ║       بورصة الوحيد Pro - EGX           ║
echo  ║       أنت في أمان شديد...                ║
echo  ║                                           ║
echo  ╚═══════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] فحص Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo.
    echo [!] Python غير مثبت! يرجى تثبيته من https://python.org
    pause
    exit /b 1
)

echo [2/3] تثبيت المكتبات (أول مرة فقط)...
if not exist ".installed" (
    pip install -r requirements.txt
    echo. > .installed
    echo     ✓ تم التثبيت
) else (
    echo     ✓ المكتبات مثبتة مسبقاً
)

echo.
echo [3/3] تشغيل التطبيق...
echo.
echo  → افتح المتصفح على: http://localhost:8501
echo  → لإيقاف التطبيق: اضغط Ctrl+C
echo.

streamlit run app.py --server.headless=false --browser.serverAddress=localhost --theme.base=dark

pause
