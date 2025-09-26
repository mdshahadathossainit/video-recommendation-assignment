@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
set "OUTPUT_FILE=project_file_list.txt"

echo Generating project file list...
echo. > "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo File List for Video Recommendation Project >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"

rem Use the 'dir' command with /s (subdirectories) and /b (bare format)
dir /s /b "%PROJECT_ROOT%app" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo Root Files >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"

dir /s /b "%PROJECT_ROOT%alembic" >> "%OUTPUT_FILE%"
dir /s /b "%PROJECT_ROOT%alembic.ini" >> "%OUTPUT_FILE%"
dir /s /b "%PROJECT_ROOT%requirements.txt" >> "%OUTPUT_FILE%"
dir /s /b "%PROJECT_ROOT%youtube_fetcher.py" >> "%OUTPUT_FILE%"
dir /s /b "%PROJECT_ROOT%.env" >> "%OUTPUT_FILE%"
dir /s /b "%PROJECT_ROOT%pyproject.toml" >> "%OUTPUT_FILE%"
dir /s /b "%PROJECT_ROOT%README.md" >> "%OUTPUT_FILE%"

echo Done! File list saved to "%OUTPUT_FILE%"
pause
