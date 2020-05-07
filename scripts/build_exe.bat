REM Common variables
call "%~dp0variables.bat"

call %activate_venv%

black %main_py_file%
pyinstaller -F %main_py_file%
pyinstaller %main_py_file% -y -F --distpath "%dist_folder%" --workpath "%build_folder%"