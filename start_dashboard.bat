@echo off
title DCS-Dashboard
cd /d "%~dp0"
python dashboard.py
if errorlevel 1 pause
