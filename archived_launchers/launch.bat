@echo off
REM AI City Simulation Launcher
REM Crafted by Intellegix

echo ================================================================================
echo AI CITY SIMULATION LAUNCHER
echo Crafted by Intellegix
echo ================================================================================
echo.

cd /d "%~dp0"

echo Starting simulation with optimized settings...
echo.

python main.py --size 256 --npcs 50

pause
