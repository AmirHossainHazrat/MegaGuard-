@echo off
title MegaGuard AI - Enterprise Starter
echo [!] Starting Watchdog...
start /b python app_monitor.py
echo [!] Starting MegaGuard Main UI...
python main.py
pause