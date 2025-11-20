@echo off
echo ====================================
echo  ESP32 Boat Control - GUI Launcher
echo ====================================
echo.

cd /d "%~dp0"

echo Iniciando aplicacion...
python main.py

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo iniciar la aplicacion
    echo.
    echo Soluciones:
    echo 1. Verifica que Python este instalado
    echo 2. Ejecuta: pip install -r requirements.txt
    echo 3. Activa el entorno virtual si usas uno
    pause
)
