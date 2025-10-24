@echo off
REM AI Civilization Experiment - LLM Mode (Qwen 1.5B)
REM Launches with 10 citizens using Qwen 1.5B for natural language decisions
REM NOTE: Requires transformers and torch installed

echo Installing dependencies if needed...
pip install transformers torch -q

cd "mods\ai_civilization\scripts"
python simulation.py --citizens 10 --use-llm --fps 10
pause
