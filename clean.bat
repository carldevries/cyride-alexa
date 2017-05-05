@echo off

for /r %%d in (*.pyc) do rm %%d

for /r %%d in (.cache) do rmdir /s /q %%d

for /r %%d in (__pycache__) do rmdir /s /q %%d

for /r %%d in (*.bak) do rm /s/q %%d