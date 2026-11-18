@echo off
:: Para o ambiente do SEI. O banco continua no volume para a proxima vez.
setlocal
call "%~dp0preparar_podman.bat"
cd /d "%~dp0docker-sei-localhost"

docker compose down
if errorlevel 1 (
  echo.
  echo Falha ao parar o ambiente do SEI. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

pause
