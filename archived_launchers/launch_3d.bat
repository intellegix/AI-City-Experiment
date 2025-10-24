@echo off
REM AI City Simulation - 3D GTA Style Launcher
REM Crafted by Intellegix

echo ================================================================================
echo AI CITY SIMULATION - 3D GTA STYLE
echo Crafted by Intellegix
echo ================================================================================
echo.

cd /d "%~dp0"

echo Installing 3D dependencies (if needed)...
pip install -q panda3d panda3d-gltf Pillow 2>nul
echo.

echo Starting 3D simulation with GTA-style graphics...
echo.
echo CONTROLS:
echo   WASD        - Move player
echo   Q/E         - Rotate camera
echo   Mouse Wheel - Zoom
echo   ESC         - Exit
echo.

python world_3d.py --size 64

pause
