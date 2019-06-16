set current_dir=%cd%
set desktop_dir=D:\Desktop

set app_name=Sindri
set work_folder=%desktop_dir%\%app_name%_build
set code_folder="D:\Google Drive\TCC\TCC_software\Sindri"
set "db_folder=%code_folder%\db"
set "texts_folder=%code_folder%\texts"
set venv=deploy_venv
set venv_scripts=%venv%\Scripts
set logfile=deploy_time.txt
set innofile="D:\Google Drive\TCC\TCC_software\Sindri_inno.iss"
set s7z="C:\Program Files\7-Zip\7z.exe"
set icon_file="D:\Google Drive\TCC\TCC_software\images\main_logo.ico"

cd %app_name%
mkdir %work_folder%

call pyinstaller.exe -D -w --clean main.py -n %app_name% --distpath %work_folder% --workpath %work_folder%\build --icon %icon_file%
REM call python -OO -m PyInstaller -D -w --clean main.py -n %app_name% --distpath %work_folder% --workpath %work_folder%\build --icon %icon_file%

cd %work_folder%
mkdir "%app_name%\db"
mkdir "%app_name%\texts"

xcopy %db_folder% %app_name%\db /E
xcopy %texts_folder% %app_name%\texts /E
xcopy %innofile% %work_folder% /E

REM if exist %s7z% (call %s7z% a Sindri -t"zip" Sindri & call %s7z% a Sindri.exe Sindri -sfx)

call %work_folder%\Sindri_inno.iss

cd %current_dir%