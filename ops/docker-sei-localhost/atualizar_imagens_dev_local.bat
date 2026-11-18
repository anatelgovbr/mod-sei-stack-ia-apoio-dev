@echo off
:: Baixa de novo as imagens do ambiente do SEI e a base da imagem do httpd. Depois, o iniciar_ambiente_dev_local.bat, em ops, recria os containers com elas.
setlocal
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"

docker compose pull
if errorlevel 1 (
  echo.
  echo Falha ao baixar as imagens. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

:: A imagem do httpd e construida aqui, e o pull pula o httpd. O --pull baixa de novo a base dela.
docker compose build --pull httpd
if errorlevel 1 (
  echo.
  echo Falha no build da imagem do httpd. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

pause
