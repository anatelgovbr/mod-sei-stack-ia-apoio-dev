@echo off
:: ============================================================
:: Roda os testes de integracao, com PHPUnit, com o banco e o
:: servidor de e-mail reais do SEI do e2e.
::
::   executar_testes_integracao.bat
::   executar_testes_integracao.bat --filter MdPetVinculoUsuExtRNTest
::
:: As opcoes do PHPUnit vao no fim. Os testes ficam em
:: tests\integracao, na raiz do repositorio. Sem a imagem do qa,
:: que traz o PHPUnit, constroi antes. Sem o SEI do e2e no ar,
:: chama antes o iniciar_ambiente_e2e.bat, de docker-e2e. O seed
:: roda antes dos testes e, no fim, o banco do e2e volta ao
:: estado inicial para a proxima rodada.
:: ============================================================
setlocal
call "%~dp0preparar_podman.bat"
:: Console em UTF-8: o seed e o PHPUnit escrevem os acentos em UTF-8.
chcp 65001 >nul

:: O e2e e a imagem do httpd leem as variaveis do .env de docker-sei-localhost, que o iniciar_ambiente_dev_local.bat cria na primeira vez.
if not exist "%~dp0docker-sei-localhost\.env" (
  echo.
  echo Falta o .env de docker-sei-localhost. Rode antes o iniciar_ambiente_dev_local.bat, em ops, uma vez: ele cria o .env e a imagem do httpd que o SEI do e2e usa.
  echo.
  pause
  exit /b 1
)

:: A imagem do qa traz o PHPUnit, e a do e2e so tem o SEI. Ela parte da imagem do httpd do ambiente.
cd /d "%~dp0docker-qa"
docker image inspect sei-qa:local >nul 2>&1
if errorlevel 1 (
  docker image inspect ops_sei-docker-httpd >nul 2>&1
  if errorlevel 1 (
    echo Construindo a imagem do httpd, so na primeira vez...
    docker compose -f ..\docker-sei-localhost\docker-compose.yml build httpd
    if errorlevel 1 goto falha_na_imagem
  )
  echo Construindo a imagem do qa...
  docker compose build qa
  if errorlevel 1 goto falha_na_imagem
)

cd /d "%~dp0docker-e2e"
set DC=docker compose --env-file ..\docker-sei-localhost\.env

set E2EUP=
for /f %%C in ('docker ps -q -f "name=^sei-e2e-httpd-1$"') do set E2EUP=%%C
if not defined E2EUP (
  echo O SEI do e2e nao esta rodando. Subindo antes, pelo iniciar_ambiente_e2e.bat...
  call "%~dp0docker-e2e\iniciar_ambiente_e2e.bat" < nul
  if errorlevel 1 (
    pause
    exit /b 1
  )
)

echo.
echo Testes de integracao: o seed roda antes dos testes e o reset do banco, depois.
echo.
%DC% run --rm integracao %*
set FALHA=%errorlevel%

:: Saida do seed: na falha dele, o PHPUnit nem comeca.
if not "%FALHA%"=="0" %DC% logs --no-color --no-log-prefix seed

echo.
if "%FALHA%"=="0" (
  echo Testes de integracao: todos passaram.
) else (
  echo Testes de integracao: houve falha. Veja a saida acima.
)

:: Banco de volta ao estado inicial: apaga seed, banco, memcached e httpd, com os volumes, e sobe
:: de novo. O /command.sh do httpd aponta o SIP do banco novo para o endereco do e2e.
echo.
echo Resetando o banco do e2e para a proxima rodada...
%DC% rm -s -f -v seed database memcached httpd >nul 2>&1
%DC% up -d --wait httpd >nul 2>&1
if errorlevel 1 (
  echo Falha no reset do banco do e2e. Rode o parar_ambiente_e2e.bat e o iniciar_ambiente_e2e.bat, em ops\docker-e2e.
  echo Situacao dos conteineres e fim do log do banco e do httpd:
  %DC% ps -a
  %DC% logs --no-color --tail 40 database httpd
) else (
  echo Banco do e2e pronto para a proxima rodada.
)
echo.
pause
exit /b %FALHA%

:falha_na_imagem
echo.
echo Falha no build da imagem. Veja a saida acima.
echo.
pause
exit /b 1
