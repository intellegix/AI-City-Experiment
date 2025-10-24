@echo off
REM AI Civilization Experiment - Headless Background Mode
REM Runs 100 citizens in background for 10000 ticks (long experiment)

cd "mods\ai_civilization\scripts"
python simulation.py --citizens 100 --headless --max-ticks 10000
pause
