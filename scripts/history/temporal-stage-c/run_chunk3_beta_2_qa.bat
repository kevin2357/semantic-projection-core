@echo off
setlocal
cd /d "%~dp0.."
python scripts\run_chunk3_beta_2_qa.py
exit /b %ERRORLEVEL%
