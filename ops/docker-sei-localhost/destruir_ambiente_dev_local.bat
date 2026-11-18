@echo off
:: Para o ambiente do SEI e apaga o banco: o proximo iniciar_ambiente_dev_local.bat sobe um banco novo.
setlocal
echo Isto apaga o banco do ambiente do SEI, com tudo o que foi gravado nele.
set /p CONFIRMA=Digite sim para continuar: 
if /i not "%CONFIRMA%"=="sim" (
  echo Nada foi apagado.
  pause
  exit /b 0
)
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"

docker compose down --volumes
if errorlevel 1 (
  echo.
  echo Falha ao apagar o ambiente do SEI. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

pause
