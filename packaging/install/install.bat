@echo off
REM install.bat - Instalación Windows

setlocal
set "SCRIPT_DIR=%~dp0"
set "PACKAGING_DIR=%SCRIPT_DIR%.."
set "ROOT_DIR=%PACKAGING_DIR%\.."
set "RELEASE_DIR=%PACKAGING_DIR%\release"

echo ================================================
echo   Instalacion de Senial SOLID v6.0.0
echo ================================================
echo.

python --version >nul 2>&1 || (
    echo ERROR: Python no encontrado
    exit /b 1
)

echo ==^> Instalando paquetes...
python -m pip install --upgrade pip --quiet

for %%p in (supervisor dominio_senial adquisicion_senial procesamiento_senial ^
            presentacion_senial persistidor_senial configurador lanzador senial_solid) do (
    echo Instalando %%p...
    for %%f in ("%RELEASE_DIR%\wheels\%%p*.whl") do (
        python -m pip install "%%f" --quiet
    )
)

echo OK Paquetes instalados

echo ==^> Configurando...
if not exist "%USERPROFILE%\.senial_solid" mkdir "%USERPROFILE%\.senial_solid"
if exist "%RELEASE_DIR%\config\config.json" (
    copy "%RELEASE_DIR%\config\config.json" "%USERPROFILE%\.senial_solid\" >nul
)
echo OK Configuracion completada

echo ================================================
echo OK Instalacion completada
echo ================================================
echo.
echo Ejecutar: senial-solid
echo.

endlocal
