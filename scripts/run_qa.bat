@echo off
setlocal
python "%~dp0run_qa.py" %*
exit /b %ERRORLEVEL%
