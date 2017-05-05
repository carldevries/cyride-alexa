@echo off

if not exist logs\ mkdir logs
if exist logs\pep8.log rm logs\pep8.log

for /r src %%d in (*.py) do (
    echo %%d >> logs\pep8.log
    echo. >> logs\pep8.log
    pep8 --show-source --show-pep8 %%d >> logs\pep8.log
    echo. >> logs\pep8.log
    echo ##################################################### >> logs\pep8.log
)