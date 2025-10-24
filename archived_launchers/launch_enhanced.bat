@echo off
REM Enhanced 3D City Launcher - GTA Style with Procedural Systems
REM Copyright 2025 Intellegix
REM Licensed under the Apache License, Version 2.0

echo ========================================
echo   Enhanced 3D AI City Simulation
echo   GTA-Style with Modular Systems
echo ========================================
echo.
echo Features:
echo - 50 Procedural Buildings (5 styles)
echo - 30 Vehicles (11 types)
echo - 10 AI NPCs
echo - Xbox Controller Support
echo - Third-Person Camera
echo.
echo Launching...
echo.

python world_3d_enhanced.py --size 64

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to launch enhanced 3D world
    echo.
    echo Troubleshooting:
    echo 1. Install dependencies: pip install -r requirements.txt
    echo 2. Check Python version: python --version
    echo 3. Verify Panda3D: pip show panda3d
    echo.
)

pause
