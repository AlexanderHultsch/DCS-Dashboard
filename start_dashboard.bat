@echo off
title DCS-Dashboard
cd /d "%~dp0"
python -c "" >nul 2>nul
if errorlevel 1 (
    py -3 core\dashboard.py
) else (
    python core\dashboard.py
)
if errorlevel 1 pause
