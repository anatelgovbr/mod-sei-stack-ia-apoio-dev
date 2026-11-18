@echo off
:: Sobe o ambiente do SEI de desenvolvimento, em http://localhost:8000/sei.
setlocal
call "%~dp0preparar_podman.bat"
cd /d "%~dp0docker-sei-localhost"

:: Na primeira vez, cria o .env a partir do modelo. Depois, avisa quando o .env difere do modelo:
:: mudanca para todos vai no modelo, que esta no Git.
if not exist ".env" (
  copy envs\env-mysql-sei5.env .env >nul
  echo Criei o .env de docker-sei-localhost a partir de envs\env-mysql-sei5.env.
)
powershell -NoProfile -Command "$atual = Get-Content .env; $dif = Get-Content envs\env-mysql-sei5.env | Where-Object { $_ -match '^[A-Za-z0-9_]+=' -and $atual -notcontains $_ } | ForEach-Object { ($_ -split '=')[0] }; if ($dif) { ''; 'O .env difere do modelo envs\env-mysql-sei5.env em: ' + ($dif -join ', ') + '.'; 'Se nao foi de proposito, apague o .env de docker-sei-localhost e rode de novo: o iniciar_ambiente_dev_local.bat cria outro a partir do modelo.'; '' }"

:: Espera o SEI ficar pronto: o Apache so abre a porta no fim do /command.sh da imagem.
docker compose up -d --wait
if errorlevel 1 (
  echo.
  echo Falha ao subir o ambiente do SEI. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

echo.
echo Ambiente do SEI no ar: http://localhost:8000/sei
echo SonarQube local e analise do codigo: iniciar_ambiente_qa.bat, em ops\docker-qa
echo.

pause
