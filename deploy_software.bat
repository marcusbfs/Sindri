

set current_dir=%cd%
set current_dir=C:\Users\Marcus\Desktop

set app_name="TPCAE"
set work_folder=%current_dir%\%app_name%_build
set code_folder="C:\Users\Marcus\Google Drive\TCC\TCC_software\TPCAE"
set db_folder=%code_folder%\db
set venv=deploy_venv
set venv_scripts=%venv%\Scripts
set logfile=deploy_time.txt

cd %current_dir%
mkdir %work_folder%
cd %work_folder%

echo %time% >> %logfile%

mkdir code
xcopy %code_folder% code /E

call virtualenv %venv%
call %venv_scripts%\activate.bat
call pip install -U -r code\requirements_to_deploy.txt
call %venv_scripts%\pyinstaller.exe -D -w --clean code\main.py -n %app_name% --distpath .

call %venv_scripts%\deactivate.bat

mkdir %app_name%\db
xcopy %db_folder% %app_name%\db /E

set s7z="C:\Program Files\7-Zip\7z.exe"
call %s7z% a TPCAE -t"zip" TPCAE
call %s7z% a TPCAE.exe TPCAE -sfx

echo %time% >> %logfile%
cd %current_dir%