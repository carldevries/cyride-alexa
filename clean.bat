@echo off

for /r %%d in (*.pyc) do rm %%d

for /r %%D in (.cache) do (

    if exist %%~fsD rmdir /s /q %%~fsD
)

for /r %%D in (__pycache__) do (

    if exist %%~fsD rmdir /s /q %%~fsD
)

echo.
echo ##########################################################################
echo.
echo Clean Finished!
echo.
echo ##########################################################################