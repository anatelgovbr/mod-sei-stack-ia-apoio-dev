@echo off
:: ============================================================
:: Roda os testes funcionais do SEI, com Playwright, no
:: navegador, no SEI do e2e.
::
::   executar_testes_e2e.bat
::   executar_testes_e2e.bat -k login
::   executar_testes_e2e.bat sei/web/modulos/apoio-plano-trabalho
::
:: As opcoes do pytest vao no fim. Os testes ficam em
:: tests\e2e, na raiz do repositorio. Sem o SEI do e2e no ar,
:: chama antes o iniciar_ambiente_e2e.bat, de docker-e2e. O SEI
:: do e2e usa a configuracao de tests\e2e\sei\config. No fim, o
:: banco do e2e volta ao estado inicial para a proxima rodada. Na
:: falha, o retrato da tela e o passo a passo ficam em
:: tests\e2e\test-results.
:: ============================================================
setlocal
call "%~dp0preparar_podman.bat"
:: Console em UTF-8: o seed e o pytest escrevem os acentos em UTF-8.
chcp 65001 >nul
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
echo Testes funcionais: o seed roda antes dos testes e o reset do banco, depois. Cada rodada leva alguns minutos a mais que os testes.
echo.
%DC% run --rm pw %*
set FALHA=%errorlevel%

:: Saida do seed: na falha dele, o pytest nem comeca.
if not "%FALHA%"=="0" %DC% logs --no-color --no-log-prefix seed

echo.
if "%FALHA%"=="0" (
  echo Testes funcionais: todos passaram.
) else (
  echo Testes funcionais: houve falha. Retrato e passo a passo em tests\e2e\test-results
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
