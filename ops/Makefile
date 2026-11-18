# Atalhos para Linux, inclusive WSL, dos .bat de ops/: cada alvo faz o mesmo que o .bat de mesmo
# nome, em ops/ ou na pasta do ambiente. Rode na raiz do repositorio, cujo Makefile inclui este, ou nesta pasta.
# Sem alvo, lista os alvos. As opcoes do PHPUnit e do pytest vao em OPCOES, e a base da analise em BASE:
#   make executar_testes_unitarios OPCOES="--filter MdAptIntegracaoTest"
#   make executar_testes_e2e OPCOES="-k login"
#   make executar_analise_codigo_alterado BASE=origin/master
# O Makefile de docker-sei-localhost vem do pengovbr e le o env.env, e nao o .env que os tres ambientes usam.

SHELL := /bin/bash
.SHELLFLAGS := -ec
.ONESHELL:
.SILENT:
.DEFAULT_GOAL := ajuda

OPS := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
# Com o Podman instalado: o Podman nao tem o BuildKit, entao o docker usa o builder classico, que o Podman atende pelo Buildah.
ifneq ($(shell command -v podman 2>/dev/null),)
export DOCKER_BUILDKIT := 0
endif
# O e2e le as variaveis do .env do ambiente do SEI.
E2E := docker compose --env-file ../docker-sei-localhost/.env
BASE ?= origin/desenvolvimento

# O qa e o SEI do e2e partem da imagem do httpd do ambiente. Na primeira vez, constroi so a imagem, sem subir o SEI.
define IMAGEM_HTTPD
if ! docker image inspect ops_sei-docker-httpd >/dev/null 2>&1; then
  echo "Construindo a imagem do httpd, so na primeira vez..."
  docker compose -f ../docker-sei-localhost/docker-compose.yml build httpd
fi
endef

define QA_NO_AR
if [ -z "$$(docker ps -q -f 'name=^qa$$')" ]; then
  echo "O container qa nao esta rodando. Rode antes make iniciar_ambiente_qa."
  exit 1
fi
endef

# O e2e e a imagem do httpd leem as variaveis do .env de docker-sei-localhost, que o iniciar_ambiente_dev_local cria na primeira vez.
define ENV_EXISTE
if [ ! -f "$(OPS)/docker-sei-localhost/.env" ]; then
  echo "Falta o .env de docker-sei-localhost. Rode antes make iniciar_ambiente_dev_local uma vez: ele cria o .env e a imagem do httpd que o SEI do e2e usa."
  exit 1
fi
endef
# Na falha da subida do SEI do e2e, mostra por que: a situacao dos conteineres e o fim do log do banco e do httpd.
define E2E_DIAGNOSTICO
echo "Situacao dos conteineres do e2e e fim do log do banco e do httpd:"
$(E2E) ps -a
$(E2E) logs --no-color --tail 40 database httpd
endef
# Imagens e SEI do e2e, na pasta docker-e2e: pelo iniciar_ambiente_e2e e pelo executar_testes_e2e, quando o SEI do e2e esta parado.
define E2E_SOBE
$(ENV_EXISTE)
$(IMAGEM_HTTPD)
echo "Imagem do Playwright. Na primeira vez, o Docker baixa 3,4 GB e instala os pacotes..."
$(E2E) build pw
echo "Subindo o banco, o memcached e o SEI do e2e..."
if ! $(E2E) up -d --wait httpd; then
  echo "Falha ao subir o SEI do e2e."
  $(E2E_DIAGNOSTICO)
  exit 1
fi
endef

# Antes de apagar dados: sem a resposta sim, nada e apagado. O texto vai sem virgula, que separaria os argumentos do call.
define CONFIRMAR
echo "$(1)"
read -r -p "Digite sim para continuar: " CONFIRMA
if [ "$${CONFIRMA,,}" != "sim" ]; then
  echo "Nada foi apagado."
  exit 0
fi
endef

.PHONY: ajuda \
	iniciar_ambiente_dev_local parar_ambiente_dev_local destruir_ambiente_dev_local reconstruir_imagem_dev_local_sem_cache atualizar_imagens_dev_local \
	iniciar_ambiente_qa parar_ambiente_qa destruir_ambiente_qa executar_testes_unitarios executar_analise_codigo_alterado \
	iniciar_ambiente_e2e parar_ambiente_e2e executar_testes_e2e assistir_testes_e2e executar_testes_integracao

ajuda: ## Lista os alvos
	awk -F ':.*## ' '/^[a-z0-9_]+:.*## /{printf "  %-40s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ---------- Ambiente do SEI, em docker-sei-localhost ----------

iniciar_ambiente_dev_local: ## Sobe o ambiente do SEI, em http://localhost:8000/sei. Na primeira vez, cria o .env
	cd "$(OPS)/docker-sei-localhost"
	# Na primeira vez, cria o .env a partir do modelo. Depois, avisa quando o .env difere do modelo:
	# mudanca para todos vai no modelo, que esta no Git.
	if [ ! -f .env ]; then
	  cp envs/env-mysql-sei5.env .env
	  echo "Criei o .env de ops/docker-sei-localhost a partir de envs/env-mysql-sei5.env."
	fi
	DIF=$$(awk -F= 'FILENAME == ARGV[1] { sub(/\r$$/, ""); atual[$$0]; next } { sub(/\r$$/, "") }
	  /^[A-Za-z0-9_]+=/ && !($$0 in atual) { printf "%s%s", sep, $$1; sep = ", " }' .env envs/env-mysql-sei5.env)
	if [ -n "$$DIF" ]; then
	  echo
	  echo "O .env difere do modelo envs/env-mysql-sei5.env em: $$DIF."
	  echo "Se nao foi de proposito, apague o .env e rode de novo: o make iniciar_ambiente_dev_local cria outro a partir do modelo."
	  echo
	fi
	# Espera o SEI ficar pronto: o Apache so abre a porta no fim do /command.sh da imagem.
	docker compose up -d --wait
	echo
	echo "Ambiente do SEI no ar: http://localhost:8000/sei"
	echo "SonarQube local e analise do codigo: make iniciar_ambiente_qa"

parar_ambiente_dev_local: ## Desliga o ambiente do SEI. O banco fica guardado
	cd "$(OPS)/docker-sei-localhost"
	docker compose down

destruir_ambiente_dev_local: ## Pede confirmacao, desliga o ambiente do SEI e apaga o banco
	cd "$(OPS)/docker-sei-localhost"
	$(call CONFIRMAR,Isto apaga o banco do ambiente do SEI e tudo o que foi gravado nele.)
	docker compose down --volumes

reconstruir_imagem_dev_local_sem_cache: ## Reconstroi sem cache a imagem do httpd
	cd "$(OPS)/docker-sei-localhost"
	docker compose build --no-cache httpd
	echo "Imagem pronta. Rode make iniciar_ambiente_dev_local para recriar os containers."

atualizar_imagens_dev_local: ## Baixa de novo as imagens do ambiente do SEI e a base da imagem do httpd
	cd "$(OPS)/docker-sei-localhost"
	docker compose pull
	# A imagem do httpd e construida aqui, e o pull pula o httpd. O --pull baixa de novo a base dela.
	docker compose build --pull httpd
	echo "Imagens atualizadas. Rode make iniciar_ambiente_dev_local para recriar os containers."

# ---------- SonarQube local e container qa, em docker-qa ----------

iniciar_ambiente_qa: ## Sobe o SonarQube local, em http://localhost:9000, e o container qa
	cd "$(OPS)/docker-qa"
	# O qa monta a ConfiguracaoSEI.php dos testes por cima da ConfiguracaoSEI.php da maquina,
	# que o SEI cria na primeira vez que sobe. Sem ela, o qa nao sobe.
	if [ ! -f ../../fontes/sei/src/main/php/sei/config/ConfiguracaoSEI.php ]; then
	  echo "A ConfiguracaoSEI.php da maquina ainda nao existe. Suba o SEI uma vez, com make iniciar_ambiente_dev_local."
	  exit 1
	fi
	$(IMAGEM_HTTPD)
	docker compose up -d --build
	# O SonarQube leva alguns minutos para subir. Mostra o log dele ate ele responder UP, por no maximo
	# 10 minutos. Se ele ja estiver no ar, segue direto.
	sonar_no_ar() { [[ "$$(docker exec qa curl -s http://sonarqube:9000/api/system/status)" == *'"status":"UP"'* ]]; }
	if ! sonar_no_ar; then
	  echo "Aguardando o SonarQube local responder. Log do SonarQube:"
	  docker compose logs -f --no-color --no-log-prefix sonarqube & LOG=$$!
	  trap 'kill $$LOG 2>/dev/null' EXIT
	  for i in $$(seq 120); do
	    sleep 5
	    sonar_no_ar && break
	    if [ $$i -eq 120 ]; then
	      echo "O SonarQube local nao respondeu em 10 minutos. Veja o log acima."
	      exit 1
	    fi
	  done
	fi
	# Na primeira vez, deixa o SonarQube local igual ao da Anatel e gera o token do scanner.
	if [ ! -f sonar/token.local ]; then
	  echo "Configurando o SonarQube local, so na primeira vez..."
	  docker exec qa sh /sonar/configurar.sh
	fi
	echo
	echo "QA pronto. SonarQube local: http://localhost:9000"
	echo "Para analisar o que mudou:  make executar_analise_codigo_alterado"
	echo "Para os testes unitarios:   make executar_testes_unitarios"

parar_ambiente_qa: ## Desliga o SonarQube local e o qa. Os dados do Sonar ficam guardados
	cd "$(OPS)/docker-qa"
	docker compose down

destruir_ambiente_qa: ## Pede confirmacao, desliga o SonarQube local e o qa e apaga os dados do Sonar e a copia do codigo
	cd "$(OPS)/docker-qa"
	$(call CONFIRMAR,Isto apaga as analises e as issues do SonarQube local e o token do scanner e a copia do codigo.)
	docker compose down --volumes
	# O token do scanner pertencia ao Sonar apagado. Sem ele, o proximo iniciar_ambiente_qa configura o Sonar de novo.
	rm -f sonar/token.local

executar_testes_unitarios: ## Roda os testes unitarios. Se o qa estiver desligado, sobe so ele, sem o Sonar. Opcoes em OPCOES="..."
	cd "$(OPS)/docker-qa"
	# Sem o qa no ar, sobe so ele: os testes nao usam o SonarQube local.
	if [ -z "$$(docker ps -q -f 'name=^qa$$')" ]; then
	  echo "Subindo o container qa, sem o SonarQube local..."
	  if ! docker compose up -d --build qa; then
	    echo "Falha ao subir o qa. Rode make iniciar_ambiente_qa, que confere o que falta."
	    exit 1
	  fi
	fi
	docker exec qa sh /qa/testar.sh $(OPCOES)

executar_analise_codigo_alterado: ## Analisa no SonarQube local o que mudou em relacao a BASE, por padrao origin/desenvolvimento
	cd "$(OPS)/docker-qa"
	$(QA_NO_AR)
	if [ ! -f sonar/token.local ]; then
	  echo "O SonarQube local ainda nao foi configurado. Rode antes make iniciar_ambiente_qa."
	  exit 1
	fi
	echo "[1/3] Arquivos alterados em relacao a $(BASE) ..."
	g() { git -C ../.. -c core.quotepath=off "$$@"; }
	# O qa grava em cache/ como root, e no disco Linux o usuario nao escreve na pasta: o qa grava as listas.
	grava() { docker exec -i qa sh -c "mkdir -p /qa/cache && cat > /qa/cache/$$1"; }
	# Ponto em que a branch saiu da base. Com varios candidatos, o git escolhe um.
	if ! MB=$$(g merge-base HEAD "$(BASE)" 2>/dev/null); then
	  echo "Nao achei $(BASE) no git. Atualize com:"
	  echo "   git fetch origin desenvolvimento:refs/remotes/origin/desenvolvimento"
	  exit 1
	fi
	g diff -U0 --no-color --no-ext-diff $$MB -- fontes/sei/src/main/php | grava alteracoes.diff
	# Contra a base de hoje: o que ja chegou nela por outro commit sai da analise.
	g diff -U0 --no-color --no-ext-diff "$(BASE)" -- fontes/sei/src/main/php | grava alteracoes-base.diff
	g ls-files --others --exclude-standard -- fontes/sei/src/main/php | grava novos.txt
	VERSAO=$$(g rev-parse --short HEAD)
	echo "[2/3] PHPStan e Psalm nos arquivos alterados ..."
	# O SonarQube fica parado enquanto o Psalm roda: com o ambiente SEI no ar, os dois juntos passam da memoria do Docker.
	docker compose stop sonarqube >/dev/null 2>&1 || true
	FALHA=0
	docker exec qa sh /qa/analisar.sh || FALHA=$$?
	# O up, e nao o start: quando o qa subiu sozinho, pelos testes unitarios, o container do Sonar ainda nao existe.
	docker compose up -d sonarqube >/dev/null 2>&1 || true
	if [ $$FALHA -eq 3 ]; then
	  echo "Nada para analisar: nenhum arquivo alterado em relacao a $(BASE)."
	  exit 0
	fi
	if [ $$FALHA -ne 0 ]; then
	  echo "Falha na analise dos arquivos alterados."
	  exit 1
	fi
	echo "[3/3] Enviando para o SonarQube local, versao $$VERSAO, depois que ele subir de novo ..."
	# Com o gate reprovado, o scanner sai com erro: os links do resultado aparecem antes.
	GATE=0
	docker compose run --rm -e VERSAO=$$VERSAO scanner || GATE=$$?
	echo
	echo "Resultado: http://localhost:9000/dashboard?id=sei-local"
	echo "Achados abertos: http://localhost:9000/project/issues?id=sei-local&resolved=false"
	exit $$GATE

# ---------- Testes e2e, em um SEI proprio, em docker-e2e ----------

iniciar_ambiente_e2e: ## Sobe o SEI do e2e e constroi as imagens dos testes e2e
	cd "$(OPS)/docker-e2e"
	$(E2E_SOBE)
	echo
	echo "E2E pronto. Para rodar os testes:  make executar_testes_e2e"
	echo "Para parar e apagar o banco do e2e:  make parar_ambiente_e2e"

parar_ambiente_e2e: ## Desliga o SEI do e2e e apaga o banco dele
	cd "$(OPS)/docker-e2e"
	$(E2E) down --volumes

executar_testes_e2e: ## Roda os testes e2e e volta o banco ao estado inicial. Se o SEI do e2e estiver desligado, sobe antes. Opcoes em OPCOES="..."
	cd "$(OPS)/docker-e2e"
	if [ -z "$$(docker ps -q -f 'name=^sei-e2e-httpd-1$$')" ]; then
	  echo "O SEI do e2e nao esta rodando. Subindo antes, como o make iniciar_ambiente_e2e..."
	  $(E2E_SOBE)
	fi
	echo "Testes funcionais: o seed roda antes dos testes e o reset do banco, depois. Cada rodada leva alguns minutos a mais que os testes."
	FALHA=0
	$(E2E) run --rm pw $(OPCOES) || FALHA=$$?
	# Saida do seed: na falha dele, o pytest nem comeca.
	if [ $$FALHA -ne 0 ]; then
	  $(E2E) logs --no-color --no-log-prefix seed
	  echo "Testes funcionais: houve falha. Retrato e passo a passo em tests/e2e/test-results"
	fi
	# Banco de volta ao estado inicial: apaga seed, banco, memcached e httpd, com os volumes, e sobe
	# de novo. O /command.sh do httpd aponta o SIP do banco novo para o endereco do e2e.
	echo "Resetando o banco do e2e para a proxima rodada..."
	$(E2E) rm -s -f -v seed database memcached httpd >/dev/null 2>&1 || true
	if $(E2E) up -d --wait httpd >/dev/null 2>&1; then
	  echo "Banco do e2e pronto para a proxima rodada."
	else
	  echo "Falha no reset do banco do e2e. Rode make parar_ambiente_e2e e make iniciar_ambiente_e2e."
	  $(E2E_DIAGNOSTICO)
	fi
	exit $$FALHA

assistir_testes_e2e: ## Roda os testes e2e com o navegador na tela, pelo WSLg, devagar e com a janela dos e-mails aberta. Opcoes em OPCOES="..."
	cd "$(OPS)/docker-e2e"
	if [ -z "$$(docker ps -q -f 'name=^sei-e2e-httpd-1$$')" ]; then
	  echo "O SEI do e2e nao esta rodando. Subindo antes, como o make iniciar_ambiente_e2e..."
	  $(E2E_SOBE)
	fi
	echo "O seed roda antes dos testes: as janelas abrem depois de alguns minutos."
	$(E2E) run --rm -e DISPLAY=:0 -e E2E_PAUSA_SEGUNDOS=6 -v /mnt/wslg/.X11-unix:/tmp/.X11-unix pw --headed --slowmo 500 $(OPCOES)

executar_testes_integracao: ## Roda os testes de integracao, com banco e e-mail reais, e volta o banco ao estado inicial. Se o SEI do e2e estiver desligado, sobe antes. Opcoes em OPCOES
	$(ENV_EXISTE)
	cd "$(OPS)/docker-qa"
	# A imagem do qa traz o PHPUnit, e a do e2e so tem o SEI.
	if [ -z "$$(docker images -q sei-qa:local)" ]; then
	  echo "Construindo a imagem do qa..."
	  $(IMAGEM_HTTPD)
	  docker compose build qa
	fi
	cd "$(OPS)/docker-e2e"
	if [ -z "$$(docker ps -q -f 'name=^sei-e2e-httpd-1$$')" ]; then
	  echo "O SEI do e2e nao esta rodando. Subindo antes, como o make iniciar_ambiente_e2e..."
	  $(E2E_SOBE)
	fi
	echo "Testes de integracao: o seed roda antes dos testes e o reset do banco, depois."
	FALHA=0
	$(E2E) run --rm integracao $(OPCOES) || FALHA=$$?
	# Saida do seed: na falha dele, o PHPUnit nem comeca.
	if [ $$FALHA -ne 0 ]; then
	  $(E2E) logs --no-color --no-log-prefix seed
	fi
	# Banco de volta ao estado inicial: apaga seed, banco, memcached e httpd, com os volumes, e sobe
	# de novo. O /command.sh do httpd aponta o SIP do banco novo para o endereco do e2e.
	echo "Resetando o banco do e2e para a proxima rodada..."
	$(E2E) rm -s -f -v seed database memcached httpd >/dev/null 2>&1 || true
	if $(E2E) up -d --wait httpd >/dev/null 2>&1; then
	  echo "Banco do e2e pronto para a proxima rodada."
	else
	  echo "Falha no reset do banco do e2e. Rode make parar_ambiente_e2e e make iniciar_ambiente_e2e."
	  $(E2E_DIAGNOSTICO)
	fi
	exit $$FALHA
