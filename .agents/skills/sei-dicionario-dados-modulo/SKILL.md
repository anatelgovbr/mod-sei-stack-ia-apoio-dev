---
name: sei-dicionario-dados-modulo
description: >
  Cria, atualiza ou verifica dicionario.md/CHANGELOG.md de um modulo customizado do SEI/SIP. Fonte
  estrutural: script de instalacao/atualizacao ja dentro deste repositorio, localizavel sozinho
  (sem caminho externo a confirmar). Para SEI, SIP ou Julgar usar sei-dicionario-dados-core.
---

# sei-dicionario-dados-modulo

Formato de `dicionario.md` e `CHANGELOG.md` (estrutura, categorias, templates de coluna, ordem de
colunas) e a ferramenta de validação são compartilhados com `sei-dicionario-dados-core` e vivem em
`.agents/references/dicionario-dados/`. Ler `formato-dicionario-de-dados.md` inteiro antes de
escrever ou editar qualquer arquivo — não replicar regra de formato aqui, não confiar em versão de
memória.

## Contrato obrigatório

Confirmar antes de qualquer escrita:

1. Nome exato do módulo.
2. Operação: criar | atualizar | verificar | changelog histórico.
3. Versão-alvo exata (`getVersao()`/constante `VERSAO_MODULO_*` do módulo).

Não precisa perguntar caminho de repositório externo — a fonte já está neste repositório.

## Bloqueios

- Módulo não mapeado em `.agents/references/mapa-modulos-scripts.md` e sem script fisicamente
  localizável em `fontes/sei/src/main/php/sei/scripts/` nem `sip/scripts/` → módulo pode ser novo
  (não é erro), mas confirmar com o desenvolvedor antes de criar script novo.
- Divergência entre o DDL acumulado do script e os DTOs do módulo → reportar a divergência exata;
  não decidir sozinho qual prevalece.
- Descrição de domínio (`sta_*`/`tipo_*`) sem evidência após esgotar README → DTO → RN → páginas/JS
  → bloqueia só aquele campo específico, não a entrega inteira; sinalizar ao desenvolvedor.

## Fonte estrutural

Script de instalação/atualização do módulo, localizado via
`.agents/references/mapa-modulos-scripts.md`
(`fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_<modulo>.php`). Já dentro deste
repositório — não precisa de caminho externo nem confirmação de localização com o desenvolvedor.

Cada versão é um método de instalação contendo `$nmVersao = 'X.Y.Z';` (a primeira versão às vezes é
só um literal dentro de `INSERT INTO infra_parametro (valor, nome) VALUES ('X.Y.Z', ...)` no método
de instalação inicial — checar os dois padrões). Script é ISO-8859-1: nunca ler com `Read` direto
(corrompe acento para U+FFFD) — usar `iconv -f ISO-8859-1 -t UTF-8 <arquivo>` ou Python com
`encoding='latin-1'`.

Banco ao vivo **nunca** é usado para módulo customizado, nem como validação — a fonte e a
conferência são sempre script + DTOs.

## dicionario.md vs CHANGELOG.md

- **`CHANGELOG.md`**: só fato estrutural — tabela/coluna/FK/PK/índice criado, alterado ou removido.
  Sem descrição de negócio; não precisa consultar DTO/RN/INT/BD/páginas.
- **`dicionario.md`**: exige descrição de negócio para toda coluna nova ou ainda sem descrição.
  Abrir DTO, RN, INT, BD e páginas do módulo
  (`fontes/sei/src/main/php/sei/web/modulos/<modulo>/`) na ordem de evidência de
  `formato-dicionario-de-dados.md` (README → DTO → RN → páginas) — vale para qualquer campo, não
  só domínio de `sta_*`/`tipo_*`. Não concluir "sem evidência" antes de esgotar as 4 camadas,
  incluindo página/JS — significado real de um campo às vezes só existe como literal HTML
  (`value="X"`, `<label>`), sem constante nomeada em RN nem PHPDoc no DTO.

DDL acumulado até a versão-alvo define a estrutura persistida; o DTO é a conferência obrigatória,
não a fonte estrutural. Divergência entre os dois bloqueia (ver "Bloqueios").

## Modo incremental (padrão a partir da segunda rodada)

Módulos já documentados uma vez cobrem o que existia até a última versão registrada. Para versão
nova do módulo:

1. Localizar só o bloco de versão novo (`$nmVersao = 'X.Y.Z'`) no script já existente — não
   reprocessar o histórico inteiro.
2. Bloco vazio → sem mudança de schema, não criar entrada.
3. Com mudança real: entrada nova no topo do `CHANGELOG.md` + atualização pontual do
   `dicionario.md` só nos campos tocados (tabela/coluna nova, alterada ou removida por essa
   versão) — não retrabalhar tabelas que não mudaram.

Modo "do zero" (módulo nunca documentado) — ler o script inteiro, cruzar com todos os DTOs, montar
os dois arquivos completos. Ver `specs/exemplo-prompt-fork-dicionario-changelog-modulo.md` para um
exemplo de execução real — retrato de um caso específico, não fonte de regra; a fonte de regra
atual é sempre `formato-dicionario-de-dados.md`.

## Não fazer

- Não acessar banco/Docker para conferir módulo — fonte e conferência são script + DTOs.
- Não inventar código de domínio de `sta_*`/`tipo_*` sem constante/label encontrado no código.
- Não citar RN/DTO/gerador de código como justificativa dentro do `dicionario.md` — isso é
  metodologia, vai só na resposta ao desenvolvedor.
- Não escrever descrição de negócio no `CHANGELOG.md`.
- Não criar script novo de instalação para módulo já mapeado em `mapa-modulos-scripts.md`.
- Não usar descrição de RN gerada por ferramenta (padrão "Descrição X N") como evidência de
  significado sem checar se não é placeholder nunca preenchido.
