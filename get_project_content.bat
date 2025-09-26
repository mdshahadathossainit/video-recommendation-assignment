@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
set "OUTPUT_FILE=project_files.txt"

echo Generating project file contents...
echo. > "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo app/main.py >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%app\main.py" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo app/database.py >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%app\database.py" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo app/models.py >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%app\models.py" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo app/config.py >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%app\config.py" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo app/db/fetcher.py >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%app\db\fetcher.py" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo app/api/v1/routers/fetch.py >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%app\api\v1\routers\fetch.py" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo ==================== >> "%OUTPUT_FILE%"
echo .env >> "%OUTPUT_FILE%"
echo ==================== >> "%OUTPUT_FILE%"
type "%PROJECT_ROOT%.env" >> "%OUTPUT_FILE%"
echo. >> "%OUTPUT_FILE%"

echo Done! All file contents have been saved to "%OUTPUT_FILE%"
pause
