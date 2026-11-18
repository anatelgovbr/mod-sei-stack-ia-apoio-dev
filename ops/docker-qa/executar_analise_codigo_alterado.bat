@echo off
:: ============================================================
:: Analisa no SonarQube local, em http://localhost:9000, tudo o
:: que mudou em relacao a desenvolvimento.
::
::   executar_analise_codigo_alterado.bat
::   executar_analise_codigo_alterado.bat origin/master
::
:: Entram os arquivos alterados, commitados ou nao, e os novos.
:: PHPStan e Psalm mostram so as linhas alteradas. O SonarQube
:: local e o container qa sobem pelo iniciar_ambiente_qa.bat,
:: nesta pasta.
:: ============================================================
setlocal
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"

set QAUP=
for /f %%C in ('docker ps -q -f "name=^qa$"') do set QAUP=%%C
if not defined QAUP (
  echo.
  echo O container qa nao esta rodando. Rode antes o iniciar_ambiente_qa.bat, em ops\docker-qa
  echo.
  pause
  exit /b 1
)
if not exist "sonar\token.local" (
  echo.
  echo O SonarQube local ainda nao foi configurado. Rode antes o iniciar_ambiente_qa.bat, em ops\docker-qa
  echo.
  pause
  exit /b 1
)

set BASE=origin/desenvolvimento
if not "%~1"=="" set BASE=%~1

echo.
echo [1/3] Arquivos alterados em relacao a %BASE% ...
if not exist "cache" mkdir "cache"
pushd ..\..
:: Ponto em que a branch saiu da base. Com varios candidatos, o git escolhe um.
set MB=
for /f %%M in ('git merge-base HEAD %BASE% 2^>nul') do set MB=%%M
if not defined MB (
  popd
  echo.
  echo Nao achei %BASE% no git. Atualize com:
  echo    git fetch origin desenvolvimento:refs/remotes/origin/desenvolvimento
  echo.
  pause
  exit /b 1
)
git -c core.quotepath=off diff -U0 --no-color --no-ext-diff %MB% -- fontes/sei/src/main/php > ops\docker-qa\cache\alteracoes.diff
:: Contra a base de hoje: o que ja chegou nela por outro commit sai da analise.
git -c core.quotepath=off diff -U0 --no-color --no-ext-diff %BASE% -- fontes/sei/src/main/php > ops\docker-qa\cache\alteracoes-base.diff
git -c core.quotepath=off ls-files --others --exclude-standard -- fontes/sei/src/main/php > ops\docker-qa\cache\novos.txt
for /f %%V in ('git rev-parse --short HEAD') do set VERSAO=%%V
popd

echo [2/3] PHPStan e Psalm nos arquivos alterados ...
:: O SonarQube fica parado enquanto o Psalm roda: com o ambiente SEI no ar, os dois juntos passam da memoria do Docker.
docker compose stop sonarqube >nul 2>&1
docker exec qa sh /qa/analisar.sh
set FALHA=%errorlevel%
:: O up, e nao o start: quando o qa subiu sozinho, pelos testes unitarios, o container do Sonar ainda nao existe.
docker compose up -d sonarqube >nul 2>&1
if "%FALHA%"=="3" (
  echo.
  echo Nada para analisar: nenhum arquivo alterado em relacao a %BASE%.
  echo.
  pause
  exit /b 0
)
if not "%FALHA%"=="0" (
  echo.
  echo Falha na analise dos arquivos alterados.
  echo.
  pause
  exit /b 1
)

echo [3/3] Enviando para o SonarQube local, versao %VERSAO%, depois que ele subir de novo ...
:: Com o gate reprovado, o scanner sai com erro: os links do resultado aparecem antes.
docker compose run --rm -e VERSAO=%VERSAO% scanner
set GATE=%errorlevel%

echo.
echo Resultado: http://localhost:9000/dashboard?id=sei-local
start "" "http://localhost:9000/project/issues?id=sei-local&resolved=false"
pause
exit /b %GATE%
