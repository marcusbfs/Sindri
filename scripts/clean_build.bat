SET p=%~dp0

pushd "%p%.."

del /f /s /q build 1>nul
rmdir /s /q build

rem del  /f /s /q dist 1>nul
rem rmdir /s /q dist

del /f /s /q __pycache__ 1>nul
rmdir /s /q __pycache__

del /f /s /q cesp.spec
del /f /s /q scripts\cesp.spec

popd
