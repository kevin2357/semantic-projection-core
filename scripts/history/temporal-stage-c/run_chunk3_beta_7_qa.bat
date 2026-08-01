@echo off
setlocal
cd /d "%~dp0\.."
set "PYTHONPATH=%CD%\src;%PYTHONPATH%"
python scripts\run_chunk3_beta_7_qa.py
exit /b %ERRORLEVEL%
