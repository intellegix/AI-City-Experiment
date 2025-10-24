@echo off
REM Ultra-Realistic 3D City Launcher
REM Copyright 2025 Intellegix
REM Licensed under the Apache License, Version 2.0

echo ========================================
echo   ULTRA-REALISTIC 3D CITY
echo   Photorealistic GTA-Style Simulation
echo ========================================
echo.
echo Crafted by Intellegix
echo Apache License 2.0
echo.
echo Features:
echo - Detailed buildings with realistic architecture
echo - Photorealistic vehicles with proper geometry
echo - Animated pedestrians with body parts
echo - Environmental props (street lights, trees, etc.)
echo - Advanced lighting and shadows
echo - Realistic materials (glass, metal, concrete)
echo - GTA-style third-person camera
echo - Xbox controller support
echo.
echo ========================================
echo.

REM Default: Afternoon lighting
python world_ultra_realistic.py --size 64 --time afternoon

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to launch
    echo.
    echo Troubleshooting:
    echo 1. Install dependencies: pip install -r requirements.txt
    echo 2. Check Python version: python --version
    echo 3. Verify Panda3D: pip show panda3d
    echo.
)

pause
