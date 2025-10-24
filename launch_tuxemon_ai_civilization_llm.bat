@echo off
REM Launch Tuxemon AI Civilization with LLM-powered citizens
echo ============================================================
echo TUXEMON AI CIVILIZATION EXPERIMENT - LLM MODE
echo ============================================================
echo Starting with 10 AI citizens using Qwen 1.5B LLM...
echo This mode is slower but provides more nuanced decision-making
echo.
python launch_tuxemon_civilization.py --citizens 10 --llm
pause
