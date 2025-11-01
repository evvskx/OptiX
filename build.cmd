@echo off

set NAME=OptiX
set ICON="resources/icon.ico"

:cleanup
    rmdir /q /s dist > nul 2>&1
    rmdir /q /s build > nul 2>&1

    rmdir /q /s src\cli\__pycache__ > nul 2>&1
    rmdir /q /s src\jobs\__pycache__ > nul 2>&1
    rmdir /q /s src\runner\__pycache__ > nul 2>&1

:install
    where PyInstaller >nul 2>&1
    if %errorlevel% neq 0 (
        py -3.13 pip install PyInstaller
    )

:build
    py -3.13 -m PyInstaller resources\.spec

    cls

    rmdir /q /s build > nul 2>&1
    mkdir build > nul 2>&1
    move dist\%NAME%.exe build\%NAME%.exe > nul
    rmdir /q /s dist

    echo Build complete! Available in: build\%NAME%.exe