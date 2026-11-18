@echo off
:: ============================================================
:: Reconstroi, sem cache, a imagem do httpd (SEI).
::
::   reconstruir_imagem_dev_local_sem_cache.bat
::
:: Use depois de mudar o Dockerfile ou para buscar de novo os
:: pacotes que o Dockerfile instala, como uma correcao do PHP.
:: Os containers no ar continuam com a imagem antiga ate o
:: iniciar_ambiente_dev_local.bat, em ops, que os recria. A
:: imagem do qa parte desta e e reconstruida no
:: iniciar_ambiente_qa.bat, em ops\docker-qa.
:: ============================================================
setlocal
call "%~dp0..\preparar_podman.bat"
cd /d "%~dp0"

echo.
echo Imagem do httpd, sem cache ...
docker compose build --no-cache httpd
if errorlevel 1 (
  echo.
  echo Falha no build da imagem do httpd. Veja a saida acima.
  echo.
  pause
  exit /b 1
)

echo.
echo Imagem pronta. Rode o iniciar_ambiente_dev_local.bat, em ops, para recriar os containers.
echo.
pause
