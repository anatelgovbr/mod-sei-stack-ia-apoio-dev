@echo off
:: Chamado pelos outros .bat: nao precisa ser rodado sozinho. Sem o Podman instalado, nao faz nada.
:: Eles chamam este arquivo antes do cd: depois do cd, o caminho do proprio script pode apontar para a pasta errada.
:: O Podman nao tem o BuildKit, entao o docker usa o builder classico, que o Podman atende pelo Buildah.
:: A maquina virtual do Podman liga se estiver desligada, por exemplo depois de reiniciar o Windows.
where podman >nul 2>&1 || exit /b 0
set "DOCKER_BUILDKIT=0"
podman machine inspect --format "{{.State}}" 2>nul | findstr "running" >nul || podman machine start
