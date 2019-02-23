set current_dir=%cd%
set desktop_dir="D:\Desktop"

set app_name=TPCAE
set work_folder=%desktop_dir%\%app_name%_build
set code_folder="D:\Google Drive\TCC\TCC_software\TPCAE"
set db_folder=%code_folder%\db
set venv=deploy_venv
set venv_scripts=%venv%\Scripts
set logfile=deploy_time.txt
set s7z="C:\Program Files\7-Zip\7z.exe"

cd %code_folder%
mkdir %work_folder%

call pyinstaller.exe -D -w --clean main.py -n %app_name% --distpath %work_folder% --workpath %work_folder%\build

cd %work_folder%
mkdir %app_name%\db
xcopy %db_folder% %app_name%\db /E

cd %current_dir%