@echo off
setlocal
set "ROOT=%~dp0.."
set "PYTHONPATH=%ROOT%\src;%PYTHONPATH%"
python "%~dp0run_chunk3_beta_9_qa.py"
exit /b %ERRORLEVEL%
