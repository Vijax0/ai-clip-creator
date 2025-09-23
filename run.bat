@echo off
call "%~dp0miniconda\Scripts\activate.bat" "%~dp0miniconda"
call conda activate app_env
python "main.py"
pause