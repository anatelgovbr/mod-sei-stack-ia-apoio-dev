@echo off
:: ============================================================
:: Roda os testes unitarios dos modulos, com PHPUnit, no
:: container qa.
::
::   executar_testes_unitarios.bat
::   executar_testes_unitarios.bat --testdox
::   executar_testes_unitarios.bat --filter MdAptIntegracaoTest
::
:: As opcoes do PHPUnit vao no fim. Os testes ficam em
:: tests\unit, na raiz do repositorio. Sem o qa no ar, sobe so
:: o qa, sem o SonarQube local; o SEI nao precisa estar no ar.
:: ============================================================
setlocal
call "%~dp0preparar_podman.bat"
:: Console em UTF-8: o detalhe das falhas dos testes sai com acentos em UTF-8.
chcp 65001 >nul
cd /d "%~dp0docker-qa"

:: Sem o qa no ar, sobe so ele: os testes nao usam o SonarQube local.
set QAUP=
for /f %%C in ('docker ps -q -f "name=^qa$"') do set QAUP=%%C
if not defined QAUP (
  echo Subindo o container qa, sem o SonarQube local...
  docker compose up -d --build qa
  if errorlevel 1 (
    echo.
    echo Falha ao subir o qa. Rode o iniciar_ambiente_qa.bat, em ops\docker-qa, que confere o que falta.
    echo.
    pause
    exit /b 1
  )
)

docker exec qa sh /qa/testar.sh %*
set FALHA=%errorlevel%

echo.
if "%FALHA%"=="0" (
  echo Testes unitarios: todos passaram.
) else (
  echo Testes unitarios: houve falha. Veja a saida acima.
)
echo.
pause
exit /b %FALHA%
