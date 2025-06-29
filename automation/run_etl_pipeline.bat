@echo off
REM ETL Pipeline Runner for Windows Task Scheduler
REM This batch file runs the ETL pipeline every 24 hours

echo Starting ETL Pipeline at %date% %time%

REM Change to the project directory
cd /d "C:\Users\admin\Desktop\My Projects\BI Project\LAB"

REM Run the ETL pipeline using the virtual environment Python
"C:\Users\admin\Desktop\My Projects\BI Project\LAB\venv\Scripts\python.exe" automated_etl_pipeline.py

echo ETL Pipeline completed at %date% %time%

REM Optional: Add a pause for manual testing
REM pause
