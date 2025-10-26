@echo off

set NAME=OptiX
set ICON="resources/icon.ico"
set UPX="resources/upx"

:cleanup
    rmdir /q /s dist > nul 2>&1
    rmdir /q /s build > nul 2>&1

    rmdir /q /s src\cli\__pycache__ > nul 2>&1
    rmdir /q /s src\jobs\__pycache__ > nul 2>&1
    rmdir /q /s src\runner\__pycache__ > nul 2>&1

:install
    where pyinstaller >nul 2>&1
    if %errorlevel% neq 0 (
        pip install pyinstaller
    )

:build
    pyinstaller resources\.spec

    cls

    rmdir /q /s build > nul 2>&1
    mkdir build > nul 2>&1
    move dist\%NAME%.exe build\%NAME%.exe > nul
    rmdir /q /s dist

    echo Build complete! Available in: build\%NAME%.exe