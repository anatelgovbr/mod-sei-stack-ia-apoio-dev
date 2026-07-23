---
name: sei-dicionario-dados-core
description: >
  Cria, atualiza ou verifica dicionario.md/CHANGELOG.md de SEI, SIP ou Julgar. Fonte estrutural:
  pacote de release externo (script/DDL) — nao o banco ao vivo. Caminho do repositorio de pacotes e
  confirmado com o desenvolvedor, nunca presumido. Para modulo customizado usar
  sei-dicionario-dados-modulo.
---

# sei-dicionario-dados-core

Formato de `dicionario.md` e `CHANGELOG.md` (estrutura, categorias, templates de coluna, ordem de
colunas) e a ferramenta de validação são compartilhados com `sei-dicionario-dados-modulo` e vivem
em `.agents/references/dicionario-dados/`. Ler `formato-dicionario-de-dados.md` inteiro antes de
escrever ou editar qualquer arquivo — não replicar regra de formato aqui, não confiar em versão de
memória.

Procedimento de localização de fonte (específico deste padrão de origem) está em
`references/localizacao-fonte-pacotes.md` — ler antes de reconstruir histórico ou localizar versão.

## Contrato obrigatório

Confirmar antes de qualquer escrita:

1. Alvo exato: SEI, SIP ou Julgar.
2. Operação: criar | atualizar | verificar | changelog histórico.
3. Versão-alvo exata.
4. Caminho do repositório de pacotes de release, ou caminho já extraído da versão específica —
   perguntar ao desenvolvedor ou usar o já indicado na conversa/projeto. Não presumir nome,
   organização de pastas ou localização; o nome usado hoje para esse repositório não é garantido
   nem permanente.

## Bloqueios

- Caminho do repositório de pacotes não localizado nem informado → perguntar ao desenvolvedor;
  não prosseguir com suposição de caminho.
- Versão-alvo não identificada → checar constante de versão no código (`SEI_VERSAO`/`SIP_VERSAO`)
  antes de perguntar.
- Divergência entre o DDL do pacote e o código (DTO/RN) do alvo → reportar as duas versões
  encontradas e o ponto exato da divergência; não decidir sozinho qual prevalece.
- **Julgar especificamente:** existe também um script de atualização já dentro deste repositório
  (`fontes/sei/src/main/php/sei/scripts/`, ver `.agents/references/mapa-modulos-scripts.md`), além
  do pacote externo. Confirmar com o desenvolvedor qual é a fonte preferida antes de reconstruir
  histórico ou atualizar o dicionário do Julgar — não presumir que o pacote externo prevalece só
  porque é o padrão dos outros dois alvos desta skill.

## Fonte estrutural

Script de atualização/DDL dentro do pacote de release informado no contrato (zip ou pasta já
extraída). Banco ao vivo **não é fonte estrutural** — é só validação opcional quando um ambiente
rodando estiver disponível (`comparar_schema.py schema`, mecanismo de acesso depende do ambiente
corrente, perguntar se necessário). Ver `references/localizacao-fonte-pacotes.md` para o
procedimento completo de localização.

## dicionario.md vs CHANGELOG.md

- **`CHANGELOG.md`**: só fato estrutural — tabela/coluna/FK/PK/índice criado, alterado ou removido.
  Sem descrição de negócio; não precisa consultar DTO/RN/páginas.
- **`dicionario.md`**: exige descrição de negócio para toda coluna nova ou ainda sem descrição.
  Abrir DTO, RN e páginas do alvo (`fontes/sei/src/main/php/sei/web/rn/`, páginas correspondentes)
  na ordem de evidência de `formato-dicionario-de-dados.md` (README → DTO → RN → páginas). Não
  concluir "sem evidência" antes de esgotar as 4 camadas.

## Modo incremental (padrão a partir da segunda rodada)

Histórico completo de SEI/SIP/Julgar reconstruído uma vez já cobre o que existia até a última
versão documentada. Para versão nova:

1. Localizar só o bloco/método daquela versão específica no script do pacote informado — não
   reprocessar pacotes/versões já documentados.
2. Bloco vazio após remover comentário/whitespace → sem mudança de schema, não criar entrada.
3. Com mudança real: inserir entrada no topo do `CHANGELOG.md` (ordem decrescente) e atualizar
   `dicionario.md` só nos campos tocados por essa versão.

Modo "do zero" (reconstrução completa do histórico) só quando SEI/SIP/Julgar ainda não tiver
`CHANGELOG.md`, ou por pedido explícito de reconstrução total — ver
`references/localizacao-fonte-pacotes.md` para o procedimento extenso (formato de pacote por
época, SIP com numeração própria, duplicação entre pacotes).

## Não fazer

- Não presumir caminho, nome ou localização do repositório de pacotes.
- Não tratar banco ao vivo como fonte estrutural — só validação, quando disponível.
- Não presumir mecanismo de acesso a banco (container, host) — perguntar se for usar validação.
- Não usar `unzip` como requisito — usar `zipfile` do Python.
- Não excluir a pasta do Julgar do repositório de pacotes sem antes confirmar a fonte preferida
  (ver bloqueio específico acima).
- Não decidir sozinho divergência entre pacote e código — bloquear e perguntar.
- Não escrever descrição de negócio no `CHANGELOG.md`.
- Não citar RN/DTO/script/nome de pacote como justificativa dentro do `dicionario.md` — isso é
  metodologia, vai só na resposta ao desenvolvedor.
- Não inventar código de domínio (`sta_*`/`tipo_*`) sem constante ou label encontrado no código.
