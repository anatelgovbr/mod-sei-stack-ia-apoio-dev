@echo off
:: ============================================================
:: Sobe o SEI do e2e: banco, memcached e httpd proprios, sem
:: depender do ambiente de desenvolvimento no ar.
::
::   iniciar_ambiente_e2e.bat
::
:: Constroi as imagens uma vez; depois, cada rodada do
:: executar_testes_e2e.bat, em ops, so roda os testes e
:: reseta o banco. Rode de novo quando o requirements.txt mudar.
:: ============================================================
setlocal
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"
set DC=docker compose --env-file ..\docker-sei-localhost\.env

:: O e2e e a imagem do httpd leem as variaveis do .env de docker-sei-localhost, que o iniciar_ambiente_dev_local.bat cria na primeira vez.
if not exist "..\docker-sei-localhost\.env" (
  echo.
  echo Falta o .env de docker-sei-localhost. Rode antes o iniciar_ambiente_dev_local.bat, em ops, uma vez: ele cria o .env e a imagem do httpd que o SEI do e2e usa.
  echo.
  pause
  exit /b 1
)

:: O SEI do e2e usa a imagem do httpd do ambiente. Na primeira vez, constroi so a imagem.
docker image inspect ops_sei-docker-httpd >nul 2>&1
if errorlevel 1 (
  echo Construindo a imagem do httpd, so na primeira vez...
  docker compose -f ..\docker-sei-localhost\docker-compose.yml build httpd
  if errorlevel 1 (
    echo.
    echo Falha no build da imagem do httpd. Veja a saida acima.
    echo.
    pause
    exit /b 1
  )
)

echo Imagem do Playwright. Na primeira vez, o Docker baixa 3,4 GB e instala os pacotes...
%DC% build pw
if errorlevel 1 (
  echo.
  echo Falha no build da imagem do Playwright. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

echo Subindo o banco, o memcached e o SEI do e2e...
%DC% up -d --wait httpd
if errorlevel 1 (
  echo.
  echo Falha ao subir o SEI do e2e.
  echo Situacao dos conteineres e fim do log do banco e do httpd:
  %DC% ps -a
  %DC% logs --no-color --tail 40 database httpd
  echo.
  pause
  exit /b 1
)

echo.
echo E2E pronto. Para rodar os testes:  executar_testes_e2e.bat, em ops
echo Para parar e apagar o banco do e2e:  parar_ambiente_e2e.bat
echo.
pause
