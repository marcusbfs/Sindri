rem @echo off

REM Common variables
call "%~dp0variables.bat"

rem create venv 
call "%~dp0build_venv.bat"

rem create shortcut bat
call "%~dp0create_pyvenv_shortcut.bat"

call %deactivate_venv%