rem @echo off

REM Common variables
call "%~dp0variables.bat"

set python_exe="%venv_dir%\Scripts\pythonw.exe"
(
    echo @echo off
    echo cd "%repo_path%\Sindri"
    echo start "" %python_exe% %main_py_file%

) > %shortcut_name%
