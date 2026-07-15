@echo off
setlocal
set "PYTHONPATH=%~dp0..\src;%PYTHONPATH%"
python "%~dp0run_chunk3_beta_10_qa.py"
exit /b %ERRORLEVEL%
