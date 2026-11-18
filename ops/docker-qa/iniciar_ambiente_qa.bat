@echo off
:: ============================================================
:: Sobe o SonarQube local e o container qa, sem depender do
:: ambiente do SEI no ar.
::
::   iniciar_ambiente_qa.bat
::
:: O qa parte da imagem do httpd do SEI. Se ela ainda nao
:: existe, constroi so a imagem, pelo docker-compose.yml de
:: ..\docker-sei-localhost, sem subir o SEI. O --build constroi
:: a imagem qa, com as ferramentas de analise e de teste, e a
:: reconstroi quando o Dockerfile, o composer.lock ou a imagem
:: do httpd mudam.
:: ============================================================
setlocal
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"

:: O qa monta a ConfiguracaoSEI.php dos testes por cima da ConfiguracaoSEI.php da maquina,
:: que o SEI cria na primeira vez que sobe. Sem ela, o qa nao sobe.
if not exist "..\..\fontes\sei\src\main\php\sei\config\ConfiguracaoSEI.php" (
  echo.
  echo A ConfiguracaoSEI.php da maquina ainda nao existe. Suba o SEI uma vez, pelo iniciar_ambiente_dev_local.bat, em ops
  echo.
  pause
  exit /b 1
)

docker image inspect ops_sei-docker-httpd >nul 2>&1
if errorlevel 1 (
  echo Construindo a imagem do httpd, base do qa, so na primeira vez...
  docker compose -f ..\docker-sei-localhost\docker-compose.yml build httpd
  if errorlevel 1 (
    echo.
    echo Falha no build da imagem do httpd. Veja a saida acima.
    echo.
    pause
    exit /b 1
  )
)

docker compose up -d --build
if errorlevel 1 (
  echo.
  echo Falha ao subir o SonarQube local e o qa. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

:: O SonarQube leva alguns minutos para subir. Mostra as linhas novas do log dele a cada 5 segundos,
:: ate ele responder UP, por no maximo 10 minutos. Se ele ja estiver no ar, segue direto.
echo.
echo Aguardando o SonarQube local responder. Log do SonarQube:
powershell -NoProfile -Command "$n = 0; $fim = (Get-Date).AddMinutes(10); while ($true) { if ((docker exec qa curl -s http://sonarqube:9000/api/system/status) -match 'status.:.UP') { exit 0 }; $l = @(docker compose logs --no-color --no-log-prefix sonarqube 2>$null); if ($l.Count -gt $n) { $l[$n..($l.Count - 1)]; $n = $l.Count }; if ((Get-Date) -gt $fim) { exit 1 }; Start-Sleep 5 }"
if errorlevel 1 (
  echo.
  echo O SonarQube local nao respondeu em 10 minutos. Veja o log acima.
  echo.
  pause
  exit /b 1
)

:: Na primeira vez, deixa o SonarQube local igual ao da Anatel e gera o token do scanner
if not exist "sonar\token.local" (
  echo Configurando o SonarQube local, so na primeira vez...
  docker exec qa sh /sonar/configurar.sh
  if errorlevel 1 (
    echo.
    echo Falha ao configurar o SonarQube local. Veja a saida acima.
    echo.
    pause
    exit /b 1
  )
)

echo.
echo QA pronto. SonarQube local: http://localhost:9000
echo Para analisar o que mudou:  executar_analise_codigo_alterado.bat
echo Para os testes unitarios:   executar_testes_unitarios.bat, em ops
echo.

pause
