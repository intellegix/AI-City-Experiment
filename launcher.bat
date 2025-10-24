@echo off
REM ============================================================
REM AI CITY EXPERIMENT - TUXEMON UI LAUNCHER
REM Multimodal Claude Infrastructure Integration
REM ============================================================
REM
REM This launcher starts the Tuxemon-based AI civilization
REM experiment with intelligent citizens using behavior trees.
REM
REM Copyright 2025 Intellegix
REM Licensed under the Apache License, Version 2.0
REM ============================================================

cls
echo ============================================================
echo    AI CITY EXPERIMENT - TUXEMON UI
echo ============================================================
echo.
echo    Multimodal Claude Infrastructure
echo    Intelligent AI Citizens Simulation
echo.
echo ============================================================
echo.
echo Starting Tuxemon AI Civilization...
echo - 20 AI citizens with behavior trees
echo - Full sprite-based UI
echo - Interactive tilemap world
echo.
echo ============================================================
echo.

python launch_tuxemon_civilization.py --citizens 20

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo ERROR: Failed to launch Tuxemon UI
    echo ============================================================
    echo.
    echo Troubleshooting:
    echo 1. Ensure Python is installed and in PATH
    echo 2. Install dependencies: pip install -r requirements.txt
    echo 3. Check Tuxemon is installed in the Tuxemon folder
    echo.
)

pause
