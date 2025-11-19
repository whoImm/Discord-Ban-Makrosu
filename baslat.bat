@echo off
chcp 65001 >nul
title Discord Oto Ban Makrosu

echo.
echo ========================================
echo   DISCORD OTO BAN MAKROSU
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadı!
    echo Lütfen Python'u https://python.org adresinden indirin ve kurun.
    echo.
    pause
    exit /b 1
)

if not exist "main.py" (
    echo HATA: main.py dosyası bulunamadı!
    echo Lütfen tüm dosyaların aynı klasörde olduğundan emin olun.
    echo.
    pause
    exit /b 1
)

if not exist "kurulum_kontrol.py" (
    echo HATA: kurulum_kontrol.py dosyası bulunamadı!
    echo.
    pause
    exit /b 1
)

echo Python ve gerekli dosyalar kontrol edildi.
echo Kurulum kontrolü yapılıyor...
echo.

python kurulum_kontrol.py

if errorlevel 1 (
    echo.
    echo Program sonlandı.
    pause
)