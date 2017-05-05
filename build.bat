@echo off

if not exist dist\ mkdir dist
if exist dist\app.zip rm dist\app.zip
if exist dist\app\ rmdir /s /q dist\app\
mkdir dist\app

copy /y src\*.py dist\app\

powershell -Command "& Compress-Archive -Path dist\app\* -DestinationPath dist\app.zip -CompressionLevel NoCompression

