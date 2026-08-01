@echo off
setlocal
cd /d "%~dp0.."
python scripts\run_chunk3_beta_4_qa.py
exit /b %ERRORLEVEL%
