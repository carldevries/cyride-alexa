@echo off

if not exist logs\ mkdir logs
if exist logs\run_tests.log rm logs\run_tests.log

pytest > logs\run_tests.log