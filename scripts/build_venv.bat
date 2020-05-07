REM Common variables
call "%~dp0variables.bat"

call python -m venv "%venv_dir%"
call %activate_venv%

pip install -r "%repo_path%\requirements.txt"