@echo off
python "%~dp0run_scoring.py" %*
exit /b %errorlevel%
