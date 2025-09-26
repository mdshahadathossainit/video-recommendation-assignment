@echo off
echo Starting the video recommendation project setup and run...

REM Change directory to the project's root folder
cd /d "%~dp0"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running database migrations...
REM Run alembic from the correct directory to find the 'app' module
alembic upgrade head

echo Starting the FastAPI server...
uvicorn app.main:app --reload