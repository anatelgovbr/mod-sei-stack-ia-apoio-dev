@echo off
:: SonarQube local e container qa. Os volumes ficam: dados do Sonar e copia do codigo.
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"
docker compose down

pause
