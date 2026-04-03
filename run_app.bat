@echo off
cd /d %~dp0

echo Activating virtual environment...
call .venv\Scripts\activate

echo Starting Streamlit App...
streamlit run streamlit_app.py

pause