@echo off
setlocal
cd /d "%~dp0.."
python scripts\run_chunk3_beta_6_qa.py
exit /b %ERRORLEVEL%
