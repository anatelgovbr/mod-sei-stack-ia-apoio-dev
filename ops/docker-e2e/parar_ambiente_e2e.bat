@echo off
:: Banco, memcached e SEI do e2e. O banco do e2e e descartavel: o --volumes apaga o banco junto,
:: e o proximo iniciar_ambiente_e2e.bat sobe um banco novo.
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"
docker compose --env-file ..\docker-sei-localhost\.env down --volumes

pause
