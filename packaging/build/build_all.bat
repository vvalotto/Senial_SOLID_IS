@echo off
REM build_all.bat - Build Windows

setlocal enabledelayedexpansion
set "SCRIPT_DIR=%~dp0"
set "PACKAGING_DIR=%SCRIPT_DIR%.."
set "ROOT_DIR=%PACKAGING_DIR%\.."
set "RELEASE_DIR=%PACKAGING_DIR%\release"

echo ================================================
echo   Build de Senial SOLID v6.0.0
echo ================================================
echo.

python --version >nul 2>&1 || (
    echo ERROR: Python no encontrado
    exit /b 1
)

echo ==^> Instalando herramientas...
python -m pip install --upgrade pip setuptools wheel build --quiet
echo OK Herramientas instaladas

echo ==^> Verificando versiones...
python "%SCRIPT_DIR%verify_versions.py" || exit /b 1
echo OK Versiones verificadas

echo ==^> Limpiando builds anteriores...
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
echo OK Limpieza completada

echo ==^> Creando estructura...
mkdir "%RELEASE_DIR%\wheels"
mkdir "%RELEASE_DIR%\source"
mkdir "%RELEASE_DIR%\config"
mkdir "%RELEASE_DIR%\docs"
mkdir "%RELEASE_DIR%\scripts"
echo OK Estructura creada

goto :main

:build_package
set "package_dir=%~1"
set "package_name=%~2"
echo ==^> Building %package_name%...
cd "%ROOT_DIR%\%package_dir%"
python -m build || exit /b 1
if exist "dist\*.whl" copy "dist\*.whl" "%RELEASE_DIR%\wheels\" >nul
if exist "dist\*.tar.gz" copy "dist\*.tar.gz" "%RELEASE_DIR%\source\" >nul
echo OK %package_name% built
cd "%ROOT_DIR%"
goto :eof

:main
echo ==^> Iniciando build...
call :build_package "supervisor" "supervisor"
call :build_package "dominio_senial" "dominio-senial"
call :build_package "adquisicion_senial" "adquisicion-senial"
call :build_package "procesamiento_senial" "procesamiento-senial"
call :build_package "presentacion_senial" "presentacion-senial"
call :build_package "persistidor_senial" "persistidor-senial"
call :build_package "configurador" "configurador"
call :build_package "lanzador" "lanzador"

REM Build metapackage
echo ==^> Building senial-solid...
cd "%PACKAGING_DIR%\metapackage"
python -m build || exit /b 1
if exist "dist\*.whl" copy "dist\*.whl" "%RELEASE_DIR%\wheels\" >nul
if exist "dist\*.tar.gz" copy "dist\*.tar.gz" "%RELEASE_DIR%\source\" >nul
echo OK senial-solid built
cd "%ROOT_DIR%"

echo ==^> Copiando archivos adicionales...
copy "%ROOT_DIR%\configurador\config.json" "%RELEASE_DIR%\config\" >nul 2>nul
copy "%ROOT_DIR%\README.md" "%RELEASE_DIR%\" >nul 2>nul
copy "%ROOT_DIR%\LICENSE" "%RELEASE_DIR%\" >nul 2>nul
echo OK Archivos copiados

echo ================================================
echo OK Build completado
echo ================================================

endlocal
