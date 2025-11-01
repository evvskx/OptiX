@echo off

set NAME=OptiX
set ICON="resources/icon.ico"

rmdir /q /s dist > nul 2>&1
rmdir /q /s build > nul 2>&1
rmdir /q /s src\cli\__pycache__ > nul 2>&1
rmdir /q /s src\jobs\__pycache__ > nul 2>&1
rmdir /q /s src\runner\__pycache__ > nul 2>&1

where py > nul 2>&1
if %errorlevel% neq 0 (
    echo Python not installed.
    exit /b 1
)

where PyInstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found, installing.
    py -3.13 -m ensurepip >nul 2>&1
    py -3.13 -m pip install PyInstaller
    where PyInstaller > nul 2>&1
    if %errorlevel% neq 0 (
        echo Error while installing.
        exit /b 1
    )
)

py -3.13 -m PyInstaller resources\.spec

cls
rmdir /q /s build > nul 2>&1
mkdir build > nul 2>&1
move dist\%NAME%.exe build\%NAME%.exe > nul

rmdir /q /s dist

echo Build completed! Path: build\%NAME%.exe
