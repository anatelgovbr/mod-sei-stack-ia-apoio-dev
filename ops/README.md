# Ambientes Docker locais

Cada pasta sobe um ambiente independente. No Windows, os scripts `.bat` do dia a dia ficam nesta pasta, e os outros ficam na pasta de cada ambiente; no Linux e no WSL, cada script tem um alvo do `make` com o mesmo nome (ver [Comandos](#comandos)). Os três ambientes usam o motor de contêineres da sua máquina, que no Windows é o Podman ou o Docker Engine dentro do WSL (ver [Primeira vez em uma máquina Windows](#primeira-vez-em-uma-máquina-windows)), e podem ficar no ar ao mesmo tempo, mas dividem a memória e as CPUs dele.

| Pasta | O que sobe | Depende de |
|---|---|---|
| [`docker-sei-localhost/`](docker-sei-localhost/) | SEI e SIP de desenvolvimento em `http://localhost:8000`, com banco, Solr, memcached, JODConverter e MailCatcher | `.env` da própria pasta |
| [`docker-qa/`](docker-qa/) | Contêiner `qa`, com PHPUnit, PHPStan e Psalm, e o SonarQube local em `http://localhost:9000` | Imagem do `httpd` e a `ConfiguracaoSEI.php` que o SEI cria na primeira vez que sobe |
| [`docker-e2e/`](docker-e2e/) | SEI, banco e memcached próprios para os testes e2e (de ponta a ponta), feitos no navegador com Playwright. Esse SEI não abre no navegador da sua máquina | Imagem do `httpd` e `.env` de `docker-sei-localhost` |

Como usar cada ambiente:

- Ambiente do SEI: endereços e credenciais na seção "Ambiente local" do [README da raiz](../README.md#ambiente-local).
- QA: testes unitários na seção "Testes" do [README da raiz](../README.md#testes); análise e SonarQube local em [`docs/sonarqube_local/README.md`](../docs/sonarqube_local/README.md).
- E2E: seção "Testes" do [README da raiz](../README.md#testes).

## Comandos

Com o Podman no Windows, dê dois cliques no `.bat`, no Explorador de Arquivos. Para passar opções, rode o `.bat` em um terminal aberto na pasta dele, como `executar_testes_unitarios.bat --group smoke`. No fim, o script espera uma tecla para fechar a janela.

No Linux e no WSL, rode `make <alvo>` na raiz do repositório. O alvo tem o mesmo nome do `.bat` e faz o mesmo que ele (ver [Linux e WSL](#linux-e-wsl)).

### Dia a dia, nesta pasta

| Windows | Linux e WSL | O que faz |
|---|---|---|
| `iniciar_ambiente_dev_local.bat` | `make iniciar_ambiente_dev_local` | Sobe o SEI e o SIP em `http://localhost:8000` e espera o SEI ficar pronto. Na primeira vez, cria o `.env` de `docker-sei-localhost` a partir do modelo; nas outras, avisa quando o `.env` difere do modelo |
| `parar_ambiente_dev_local.bat` | `make parar_ambiente_dev_local` | Desliga o ambiente do SEI. O banco fica guardado para a próxima vez |
| `executar_testes_unitarios.bat` | `make executar_testes_unitarios` | Roda os testes unitários no `qa`. Se o `qa` estiver desligado, sobe só ele, sem o Sonar. As opções do PHPUnit vão no fim do comando do Windows ou em `OPCOES="..."` no `make` |
| `executar_testes_e2e.bat` | `make executar_testes_e2e` | Roda os testes e2e no navegador, no SEI do e2e. Se esse SEI estiver desligado, sobe antes. No fim, volta o banco do e2e ao estado inicial e deixa o SEI do e2e no ar. As opções do pytest vão no fim do comando do Windows ou em `OPCOES="..."` no `make` |
| `executar_testes_integracao.bat` | `make executar_testes_integracao` | Roda os testes de integração, com o banco e o servidor de e-mail reais do SEI do e2e. Se a imagem do `qa` faltar, constrói antes; se o SEI do e2e estiver desligado, sobe antes. No fim, volta o banco do e2e ao estado inicial. As opções do PHPUnit vão no fim do comando do Windows ou em `OPCOES="..."` no `make` |

Antes de abrir o MR (merge request, o pedido de integração no GitLab), rode os três scripts de testes. Em uma máquina nova, rode antes o `iniciar_ambiente_dev_local` uma vez, que cria o `.env`, a imagem do `httpd` e a `ConfiguracaoSEI.php` que os testes usam. Depois disso, você não precisa subir nada antes, porque cada script sobe o que falta. Com o SonarQube local no ar, os testes e2e chegam a levar o dobro do tempo.

Os testes deixam o `qa` e o SEI do e2e no ar. Para liberar a memória do Docker, desligue os dois pelo `parar_ambiente_qa`, de `docker-qa`, e pelo `parar_ambiente_e2e`, de `docker-e2e`.

### Ambiente do SEI, em `docker-sei-localhost`

| Windows | Linux e WSL | O que faz |
|---|---|---|
| `destruir_ambiente_dev_local.bat` | `make destruir_ambiente_dev_local` | Pede confirmação, desliga o ambiente do SEI e **apaga o banco**, com tudo o que foi gravado nele. A próxima subida começa com os dados iniciais da imagem do banco |
| `reconstruir_imagem_dev_local_sem_cache.bat` | `make reconstruir_imagem_dev_local_sem_cache` | Reconstrói do zero a imagem do `httpd`, por exemplo para trazer uma correção do PHP. Depois, rode o `iniciar_ambiente_dev_local`, nesta pasta, para recriar os contêineres |
| `atualizar_imagens_dev_local.bat` | `make atualizar_imagens_dev_local` | Baixa de novo as imagens do ambiente do SEI e a base da imagem do `httpd`. Depois, rode o `iniciar_ambiente_dev_local`, nesta pasta, para recriar os contêineres |

### SonarQube local e `qa`, em `docker-qa`

| Windows | Linux e WSL | O que faz |
|---|---|---|
| `iniciar_ambiente_qa.bat` | `make iniciar_ambiente_qa` | Sobe o SonarQube local, em `http://localhost:9000`, e o `qa`. Na primeira vez, configura o Sonar local com as mesmas regras do Sonar da Anatel |
| `parar_ambiente_qa.bat` | `make parar_ambiente_qa` | Desliga o SonarQube local e o `qa`. Os dados do Sonar ficam guardados |
| `destruir_ambiente_qa.bat` | `make destruir_ambiente_qa` | Pede confirmação, desliga o SonarQube local e o `qa` e **apaga os dados do Sonar**: as análises, as issues, o token do scanner e a cópia do código usada na análise. O próximo `iniciar_ambiente_qa` configura o Sonar de novo |
| `executar_analise_codigo_alterado.bat` | `make executar_analise_codigo_alterado` | Roda a análise estática, com o PHPStan e o Psalm, nos arquivos que mudaram em relação à branch `origin/desenvolvimento` e envia o resultado ao Sonar local. Outra base vai no fim do comando do Windows ou em `BASE=...` no `make` |

### Testes e2e, em `docker-e2e`

| Windows | Linux e WSL | O que faz |
|---|---|---|
| `iniciar_ambiente_e2e.bat` | `make iniciar_ambiente_e2e` | Sobe o SEI do e2e, com banco e memcached próprios, e constrói as imagens dos testes |
| `parar_ambiente_e2e.bat` | `make parar_ambiente_e2e` | Desliga o SEI do e2e e apaga o banco dele, que é descartável |

## O que os ambientes compartilham

- **Imagem `ops_sei-docker-httpd`.** O compose de `docker-sei-localhost` constrói essa imagem. O `qa` parte dela, e o SEI do e2e a usa. O `iniciar_ambiente_qa` e o `iniciar_ambiente_e2e` constroem a imagem quando ela ainda não existe, sem subir o SEI.
- **`.env` de `docker-sei-localhost`.** É o arquivo com as configurações dos três ambientes: imagens, banco e chaves de acesso. Fica fora do Git. Na primeira vez, o `iniciar_ambiente_dev_local` cria o `.env` a partir do modelo `envs/env-mysql-sei5.env`. Nas outras, avisa quando o `.env` difere do modelo e lista as variáveis diferentes. Mudança para a equipe toda vai no modelo, por MR.
- **`preparar_podman.bat`.** Os outros scripts do Windows chamam esse arquivo, nesta pasta, para ligar a máquina do Podman quando ela está desligada. Você não precisa rodar esse arquivo sozinho.
- **Código e testes.** Os três ambientes leem `fontes/sei/src/main/php` e `tests/` direto da sua cópia do repositório, sem copiar o código para dentro da imagem.
- **Nomes de projeto fixos.** O Docker mostra os ambientes como `ops_sei-docker`, `sei-sonar` e `sei-e2e`. Os dois primeiros não seguem o nome da pasta, porque os volumes com o banco do SEI e os dados do Sonar já existem com esses nomes nas máquinas da equipe. Trocar esses nomes exige migrar os volumes.

## Uploads e pastas temporárias

O `httpd` de desenvolvimento mantém `/opt/sei/temp` e `/opt/sip/temp` na montagem do código em `/opt`. Os arquivos continuam nas pastas `fontes/sei/src/main/php/sei/temp` e `fontes/sei/src/main/php/sip/temp` do repositório, visíveis pelo Explorer do Windows. Não há `tmpfs` nem volume separado nessas pastas do ambiente de desenvolvimento.

Com o código no disco Windows, o arquivo criado pelo Apache pode aparecer com outro proprietário: a escrita funciona, mas o `chmod(0660)` de `InfraPagina::processarUpload` falha com `Operation not permitted`. Dar permissão `777` na pasta não resolve essa troca de proprietário. O script [`iniciar-httpd.sh`](docker-sei-localhost/iniciar-httpd.sh) cria e remove um arquivo de diagnóstico em cada pasta, identifica o UID (identificador numérico do usuário) atribuído pela montagem e, quando necessário, ajusta o UID da conta `apache` dentro do contêiner. A conta mantém seu grupo e continua sem privilégios de root.

Antes de executar o `/command.sh` original da imagem, o script verifica que o Apache consegue aplicar `chmod(0660)` nas duas pastas. Se os proprietários forem incompatíveis ou a permissão continuar falhando, a inicialização para com erro. No disco Linux, os arquivos já pertencem ao Apache e seu UID não muda. A correção não altera o código do SEI/SIP, a imagem compartilhada com QA/e2e, os usuários do host nem o volume do banco. Os temporários permanecem no host ao reiniciar ou recriar o contêiner, sujeitos à limpeza normal do SEI/SIP.

**Atenção ao armazenamento definitivo:** o Compose atual não monta um volume em `/var/sei/arquivos`, repositório configurado pela imagem. Essa limitação já existia: recriar o `httpd` descarta os arquivos gravados na camada do contêiner, mesmo que seus registros permaneçam no banco. Se houver documentos salvos, faça uma cópia desse diretório antes de recriar, com `docker cp httpd:/var/sei/arquivos <pasta-de-backup>`, e restaure-a depois, com `docker cp <pasta-de-backup>\. httpd:/var/sei/arquivos`. Após restaurar, execute `docker exec httpd chown -R apache:apache /var/sei/arquivos` para alinhar o proprietário ao usuário do serviço. A correção do upload não muda a persistência desse repositório.

Para aplicar a mudança a um ambiente já ligado, termine ou cancele os uploads pendentes e, em um PowerShell na raiz do repositório, rode:

```powershell
cd ops\docker-sei-localhost
docker compose up -d --no-deps --force-recreate --wait httpd
```

O comando recria somente o `httpd`, sem reconstruir a imagem, reiniciar o banco ou apagar volumes. Depois, recarregue a página do SEI, entre novamente se solicitado e selecione o arquivo em **Anexar Arquivo**. Nas próximas subidas, o `iniciar_ambiente_dev_local.bat` executa o ajuste normalmente.

## Primeira vez em uma máquina Windows

Há duas opções para rodar os ambientes no Windows. As duas são gratuitas, não usam o Docker Desktop e sobem o mesmo SEI, em `http://localhost:8000/sei`. A diferença está no jeito de usar:

- **Opção 1. Podman, com interface gráfica.** O Podman Desktop é um programa com janelas parecido com o Docker Desktop. O código fica no disco `C:`, e os comandos são scripts `.bat`, que rodam com dois cliques. Serve para quem prefere usar o Windows como de costume.
- **Opção 2. WSL com Docker, sem interface gráfica.** Tudo é feito no terminal do Ubuntu, a janela de comandos do Linux, com o comando `make`. O código fica no disco do Linux, e o ambiente fica mais rápido. Serve para quem já usa terminal Linux.

Se você não usa terminal Linux no dia a dia, escolha a Opção 1. As duas usam o WSL 2 (Subsistema do Windows para Linux), recurso do próprio Windows que roda Linux dentro dele, porque os contêineres do projeto são Linux.

| Característica | [Opção 1. Podman](#opção-1-podman-com-interface-gráfica) | [Opção 2. WSL com Docker](#opção-2-wsl-com-docker-sem-interface-gráfica) |
|---|---|---|
| Interface gráfica | Sim. O Podman Desktop mostra os contêineres, as imagens, os volumes e os logs, como o Docker Desktop | Não. Tudo pelo terminal do Ubuntu |
| Motor de contêineres | Podman, em uma máquina virtual Linux que ele cria no WSL 2 | Docker Engine, instalado no Ubuntu do WSL 2 |
| Onde fica o código | No disco `C:` | No disco do Linux, dentro do Ubuntu |
| Como rodar os comandos | Scripts `.bat`, com dois cliques | `make <alvo>`, no terminal do Ubuntu |
| Velocidade de leitura do código pelos contêineres | Mais lenta, porque o código chega à máquina do Podman a partir do `C:` | Mais rápida, porque o código fica no disco do Linux |
| Editor de código | Qualquer editor do Windows | Editor ligado ao WSL, como o VS Code com a extensão WSL |

### Opção 1. Podman, com interface gráfica

O [Podman](https://podman.io/docs/installation#windows) é um motor de contêineres gratuito e de código aberto. Ele roda os contêineres em uma máquina virtual Linux que cria no WSL 2. O [Podman Desktop](https://podman-desktop.io/docs/installation/windows-install) é a interface gráfica do Podman, parecida com a do Docker Desktop. Os scripts `.bat` usam os comandos `docker` e `docker compose`, que falam com o Podman.

Um administrador da máquina faz os passos 1 a 3 uma vez, em um PowerShell aberto como administrador:

1. Se a máquina ainda não tem o WSL 2, instale com `wsl --install --no-distribution` e reinicie o Windows. O Podman cria a própria distribuição Linux.
2. Se o Docker Desktop estiver instalado, desinstale com `winget uninstall --id Docker.DockerDesktop --exact`. Com ele instalado, o `docker` continua falando com o Docker Desktop, e não com o Podman.
3. Instale o Podman com `winget install --id RedHat.Podman --exact`, ou pelo instalador da [página do Podman](https://podman.io/docs/installation#windows).

Depois, com o seu usuário, em um PowerShell comum:

4. Instale o `docker` e o `docker compose`, nas versões testadas com o Podman 5.8. Os dois são só os comandos, sem o Docker Desktop:

   ```powershell
   $ProgressPreference = "SilentlyContinue"
   $pasta = "$env:LOCALAPPDATA\docker-cli"
   Invoke-WebRequest https://download.docker.com/win/static/stable/x86_64/docker-28.5.2.zip -OutFile "$env:TEMP\docker.zip"
   Expand-Archive "$env:TEMP\docker.zip" -DestinationPath $pasta -Force
   [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "User") + ";$pasta\docker", "User")
   New-Item -ItemType Directory -Force "$env:USERPROFILE\.docker\cli-plugins" | Out-Null
   Invoke-WebRequest https://github.com/docker/compose/releases/download/v2.40.3/docker-compose-windows-x86_64.exe -OutFile "$env:USERPROFILE\.docker\cli-plugins\docker-compose.exe"
   ```

5. Feche o PowerShell e abra outro, para o `Path` novo valer. Crie e ligue a máquina do Podman e deixe o `docker` no endereço padrão, que o Docker Desktop trocava pelo dele:

   ```powershell
   podman machine init --rootful
   podman machine start
   docker context use default
   ```

   Com o `--rootful`, os contêineres rodam como root dentro da máquina, como no Docker, para o qual os ambientes foram feitos. Daí em diante, os scripts ligam a máquina quando ela está desligada, por exemplo depois de reiniciar o Windows.

   Se o Docker Desktop já esteve instalado, tire também do `config.json` do `docker` o programa de senhas dele, que saiu junto com o Docker Desktop. Sem isso, o `docker` não baixa as imagens e avisa `"docker-credential-desktop": executable file not found`:

   ```powershell
   $cfg = "$env:USERPROFILE\.docker\config.json"
   if (Test-Path $cfg) { $j = Get-Content $cfg -Raw | ConvertFrom-Json; if ($j.credsStore -eq "desktop") { $j.PSObject.Properties.Remove("credsStore"); $j | ConvertTo-Json -Depth 10 | Set-Content $cfg -Encoding ascii } }
   ```

6. Confira com `docker version`: a seção `Server` precisa mostrar `Podman Engine`. Se o `podman machine start` avisar que outro programa ocupa o endereço padrão do Docker, rode `setx DOCKER_HOST npipe:////./pipe/podman-machine-default` e abra outro terminal, como explica o [guia do Podman para Windows](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md).
7. Instale o Podman Desktop com `winget install --id RedHat.Podman-Desktop --exact`, ou pelo [instalador](https://podman-desktop.io/downloads), e abra o programa. Ele mostra a máquina criada no passo 5: não crie outra máquina por ele. Nele, você vê os contêineres, as imagens, os volumes e os logs, e liga e desliga os contêineres. Os scripts funcionam mesmo sem o Podman Desktop.
8. Rode o `iniciar_ambiente_dev_local.bat`, nesta pasta. Na primeira vez, ele cria o `.env` do ambiente do SEI a partir do modelo e constrói as imagens, o que leva alguns minutos.
9. Abra `http://localhost:8000/sei` e entre com o usuário `teste` e a senha `teste`.

Imagens, contêineres e volumes ficam na máquina do Podman, no perfil do seu usuário. Ao trocar de usuário, ou ao apagar a máquina com `podman machine rm`, tudo começa do zero, e a primeira subida de cada ambiente constrói as imagens de novo.

### Opção 2. WSL com Docker, sem interface gráfica

O [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) é o motor de contêineres da Docker, gratuito e de código aberto, sem a interface gráfica do Docker Desktop. Ele roda dentro de um Ubuntu no [WSL 2](https://learn.microsoft.com/pt-br/windows/wsl/install). Instalar, subir os ambientes e rodar os testes é tudo feito no terminal do Ubuntu, e o código fica no disco do Linux.

Um administrador da máquina faz os passos 1 e 2 uma vez, em um PowerShell aberto como administrador:

1. Se a máquina ainda não tem o WSL 2, instale com `wsl --install --no-distribution` e reinicie o Windows.
2. Se o Docker Desktop estiver instalado, desinstale com `winget uninstall --id Docker.DockerDesktop --exact`. Com ele instalado, o `docker` do Ubuntu pode continuar falando com o Docker Desktop.

Depois, com o seu usuário:

3. Em um PowerShell comum, instale o Ubuntu 24.04 com `wsl --install -d Ubuntu-24.04`. Na primeira vez, o Ubuntu pede um usuário e uma senha do Linux. Essa é a senha que o `sudo` pede nos próximos passos, todos no terminal do Ubuntu.
4. Instale o Docker Engine pelo [guia da Docker para Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). Depois, siga o [guia de pós-instalação](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) para rodar o `docker` sem `sudo` e instale o `make` com `sudo apt install -y make`.
5. Feche o terminal do Ubuntu e abra outro. Confira com `docker run --rm hello-world`, que precisa mostrar `Hello from Docker!`. Se o `docker` responder `permission denied`, rode `wsl --terminate Ubuntu-24.04` em um PowerShell e abra o Ubuntu de novo. Se ele avisar `"docker-credential-desktop.exe": executable file not found`, o Ubuntu ainda guarda a configuração do Docker Desktop: apague com `rm ~/.docker/config.json`.
6. Clone o repositório no disco do Linux, e não em `/mnt/c`, que é o `C:` visto pelo Ubuntu: `mkdir -p ~/projetos && cd ~/projetos && git clone <endereço do repositório>`, com o endereço do botão de clonar do projeto no GitLab. O clone por SSH precisa de uma chave SSH no Ubuntu cadastrada no GitLab, como explica o [guia do GitLab](https://docs.gitlab.com/user/ssh/).
7. Na pasta do repositório, rode `make iniciar_ambiente_dev_local`. Na primeira vez, ele cria o `.env` do ambiente do SEI a partir do modelo e constrói as imagens, o que leva alguns minutos.
8. Abra `http://localhost:8000/sei` no navegador do Windows e entre com o usuário `teste` e a senha `teste`.

Para abrir o código no VS Code, instale a [extensão WSL](https://code.visualstudio.com/docs/remote/wsl) e rode `code .` na pasta do repositório, no terminal do Ubuntu. No Explorador de Arquivos, o repositório aparece em `\\wsl.localhost\Ubuntu-24.04\home\<usuário do Linux>\projetos`.

Imagens, contêineres e volumes ficam no disco do Ubuntu. Daí em diante, use os alvos do `make` de [Comandos](#comandos). As particularidades do Linux estão em [Linux e WSL](#linux-e-wsl).

## Linux e WSL

No Linux e no WSL, rode `make <alvo>` na raiz do repositório ou nesta pasta. O `Makefile` da raiz só inclui o desta pasta, onde ficam os alvos. Cada alvo faz o mesmo que o script do Windows de mesmo nome, e `make` sozinho lista os alvos com o que cada um faz. Se o `make` não estiver instalado, instale com `sudo apt install make`.

No Linux, os alvos funcionam com o [Docker Engine](https://docs.docker.com/engine/install/), que no Ubuntu se instala como no passo 4 da [Opção 2. WSL com Docker](#opção-2-wsl-com-docker-sem-interface-gráfica), ou com o [Podman](https://podman.io/docs/installation) sem root, testado na versão 4.9.3, do `apt` do Ubuntu 24.04. O Podman não traz os comandos `docker` e `docker compose`. No Ubuntu, adicione o [repositório da Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) e instale só esses dois comandos, sem o motor da Docker, nas versões testadas com o Podman. Depois, ligue a API do Podman e aponte o `docker` para ela em todo terminal. Com o `podman` instalado, o `make` passa a usar o builder clássico, que o Podman atende:

```bash
sudo apt install -y docker-ce-cli=5:28.5.2-1~ubuntu.24.04~noble docker-compose-plugin=2.40.3-1~ubuntu.24.04~noble
sudo apt-mark hold docker-ce-cli docker-compose-plugin
systemctl --user enable --now podman.socket
echo 'export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock' >> ~/.bashrc
source ~/.bashrc
```

Na primeira vez, rode `make iniciar_ambiente_dev_local`. Ele cria o `.env` do ambiente do SEI a partir do modelo e constrói as imagens, o que leva alguns minutos.

| Para | Comando |
|---|---|
| Passar opções ao PHPUnit | `make executar_testes_unitarios OPCOES="--filter MdAptIntegracaoTest"` |
| Passar opções ao pytest | `make executar_testes_e2e OPCOES="-k login"` |
| Acompanhar os testes e2e na tela, pelo WSLg | `make assistir_testes_e2e OPCOES="-k arquivo_que_some"` |
| Analisar em relação a outra base | `make executar_analise_codigo_alterado BASE=origin/master` |

Com o Docker Engine, os contêineres rodam como root. No disco Linux, o que eles gravam no repositório fica com dono root, como `ops/docker-qa/cache`, `ops/docker-qa/relatorios`, `ops/docker-qa/sonar/token.local` e, na falha de um teste e2e, `tests/e2e/test-results`. Apagar esses arquivos exige `sudo`. Com o Podman sem root, o root do contêiner é o seu usuário, e esses arquivos ficam com você.

Ao trocar o Docker pelo Podman, antes de subir os ambientes, devolva ao seu usuário o que o Docker gravou, porque o contêiner sem root não consegue gravar em arquivo de root. Apague também o token do Sonar antigo, para o `make iniciar_ambiente_qa` configurar o Sonar novo. Na raiz do repositório, rode:

```bash
sudo chown -R "$USER:$USER" .
rm -f ops/docker-qa/sonar/token.local
```

O `Makefile` de `docker-sei-localhost` vem do projeto sei-docker e lê o `env.env`, e não o `.env` que os três ambientes usam. Não use esse Makefile.
