@echo off
:: SonarQube local e container qa, com os dados do Sonar e a copia do codigo
setlocal
echo Isto apaga as analises e as issues do SonarQube local, o token do scanner e a copia do codigo.
set /p CONFIRMA=Digite sim para continuar: 
if /i not "%CONFIRMA%"=="sim" (
  echo Nada foi apagado.
  pause
  exit /b 0
)
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"
docker compose down --volumes
:: O token do scanner pertencia ao Sonar apagado. Sem ele, o proximo iniciar_ambiente_qa.bat configura o Sonar de novo.
del /q "sonar\token.local" >nul 2>&1

pause
