@echo off
title DCS-Dashboard
cd /d "%~dp0"
python core\dashboard.py
if errorlevel 1 pause
