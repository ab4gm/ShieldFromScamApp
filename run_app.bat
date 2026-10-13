@echo off
echo Starting ShieldFromScamApp...
echo.
echo If the app does not open automatically, go to: http://localhost:8501
echo Press Ctrl+C in this window to stop the app.
echo.
cd /d "%~dp0"
streamlit run Home.py
pause
