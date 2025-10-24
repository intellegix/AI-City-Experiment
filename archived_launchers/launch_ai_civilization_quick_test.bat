@echo off
REM AI Civilization Experiment - Quick Test Mode
REM Runs 20 citizens headless for 100 ticks to validate setup

cd "mods\ai_civilization\scripts"
python simulation.py --citizens 20 --headless --max-ticks 100
pause
