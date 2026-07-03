---
name: sei-code-review-security
description: >
  Skill orquestradora de code review e security review para diffs, PRs, branches
  ou modulos completos em SEI. Classifica a mudanca, expande escopo quando
  preciso, aciona gates por artefato, aplica V01-V10, verifica reaproveitamento
  em RN/INT/DTO, avalia qualidade de codigo e emite um veredito de merge.
  Nao altera codigo.

  Aliases: sei-revisao-codigo-seguranca, sei-revisao-pr, sei-security-review
---

# sei-code-review-security

Skill de **triagem em tempo de revisao**. Consolida gates por artefato, seguranca,
reaproveitamento e qualidade para devolver um **veredito curto** sobre diff, PR,
branch ou modulo completo.

## Posicionamento

| Skill | Momento | Papel |
|---|---|---|
| `sei-guardrails-modulo` | durante a implementacao | impedir erro antes de escrever |
| `code-review` | pos-implementacao | qualidade sem contexto SEI |
| **`sei-code-review-security`** | **sobre diff, PR ou modulo completo** | gates + seguranca + qualidade + veredito |

Esta skill consolida evidencias e executa seu contrato operacional por este
arquivo. Referencias complementares ficam restritas a material tematico e
sub-checklists especializados.

## Fontes de verdade

- `AGENTS.md` — guardrails universais, padrao transacional, escopo de escrita
- `.agents/references/roteamento-de-skills.md` — matriz de demanda e gates
- `.agents/references/gates-de-implementacao.md` — gates G/R/C/D
- `.agents/references/mapa-modulos-scripts.md` — impacto de release por modulo
- `.agents/security/matriz-vulnerabilidades-sei.md` — vetores V01-V10
- `.agents/checklists/checklist-seguranca.md` — criterios por artefato, severidades e itens AppSec `C1-C10`

## Referencias complementares

- `.agents/security/origem-referencias-seguranca.md` — curadoria AppSec PHP aplicada a code review do SEI
- `references/reutilizacao-rn-int-dto.md` — checklist `U1-U10` para reaproveitamento em RN/INT/DTO

## Quando usar

- revisao de diff, branch ou PR com arquivos em `modulos/**`
- review ou security review de modulo completo
- pedido de "revise", "code review" ou "security review" sobre mudanca SEI

## Entradas

- diff, branch, lista de arquivos alterados ou diretorio de modulo
- objetivo da mudanca em 1 frase
- opcional: modulo-alvo, contrato funcional e evidencias de gate ja executadas

Se a entrada for um diretorio de modulo, tratar como **review de modulo
completo**. Nesse caso, expandir automaticamente o escopo para:

- `*Integracao.php` do modulo
- paginas `*_lista.php` e `*_cadastro.php`
- classes `*RN.php`
- DTO, BD, DDL e modelagem relevante do modulo
- scripts SEI e SIP mapeados em `.agents/references/mapa-modulos-scripts.md`,
  quando existirem

## Procedimento

1. Delimitar escopo e revisar o delta primeiro, expandindo para o contexto do arquivo
   ou metodo quando o gate exigir.
2. Conferir escopo permitido em `AGENTS.md`; mudanca fora de `modulos/**` gera
    BLOQUEANTE (G6) e recomendacao de `escrever-adr`.
3. Classificar a mudanca usando `.agents/references/roteamento-de-skills.md`.
4. Se a entrada for um diretorio de modulo, expandir automaticamente o escopo
   para os artefatos obrigatorios do modulo e para os scripts SEI/SIP mapeados.
5. Mapear os artefatos alterados ou incluidos no escopo e acionar os gates
   correspondentes conforme
   `.agents/references/roteamento-de-skills.md` e
   `.agents/references/gates-de-implementacao.md`.
6. Usar esta ordem de evidencia por gate:
    - reaproveitar saida existente, se o gate ja tiver sido executado
    - executar a validacao local disponivel (`audit.py`, `php -l`, `release_check`) quando aplicavel
    - completar com inspecao manual sempre que a automacao nao for suficiente
7. Se houver script SEI ou SIP mapeado para o modulo, executar `release_check`
   correspondente e consolidar impacto de versao, recursos, menus, parametros e
   multi-SGBD no resultado.
8. Aplicar `.agents/security/matriz-vulnerabilidades-sei.md` (V01-V10) e
   `.agents/checklists/checklist-seguranca.md`, incluindo os itens `C1-C10`.
9. Fazer analise de fluxo de dados: entrada -> SQL, HTML/JS, arquivo,
   desserializacao, redirect, chamada externa, log ou execucao.
10. Verificar reaproveitamento em RN/INT/DTO so para funcoes, metodos e classes
    novas ou alteradas nessas camadas.
11. Revisar arquitetura SEI, transacao, pos-commit, permissoes, release e
    modelagem no contexto do escopo revisado.
12. Classificar `TODO:` encontrado no diff ou no contexto revisado como
    `divida conhecida`, `risco relevante`, `bloqueante` ou `ignorar`. `TODO:`
    nao bloqueia por si so e nao dispensa gates obrigatorios.
13. Compor `code-review` apenas na dimensao de qualidade e manutenibilidade.
    Seguranca, severidade e veredito final permanecem nesta skill.
14. Executar segunda passada obrigatoria para tentar derrubar falso positivo antes
    do veredito.
15. Consolidar achados introduzidos e pre-existentes, resultado por gate,
    impacto de release e veredito.

## Gates por artefato

| Artefato no escopo | Gate a acionar | Codigos |
|---|---|---|
| `*_lista.php`, `*_cadastro.php`, `controlador.php` | `sei-verificacao-pagina` | P1-P10 |
| `*RN.php` | `sei-verificacao-rn` | T1-T5 |
| `*BD.php`, DTO, DDL `.sql` | `sei-verificacao-banco-dados` | R1-R15 |
| `*Integracao.php` (Ajax/WS, `tratarLinkSemAssinatura`) | `sei-verificacao-controladores` | CI1-CI4 |
| `*_tarefa.php` | `sei-verificacao-tarefa` | K1-K7 |
| qualquer PHP alterado | `sei-testes-validacao` | `php -l` |
| script SEI/SIP mapeado do modulo | `sei-verificacao-banco-dados` em `release_check` | R1/R3/R4/R5/R6 |

## Ordem de prioridade em review de modulo completo

1. permissoes e link assinado
2. transacao e pos-commit
3. release, versionamento e scripts SEI/SIP
4. modelagem e multi-SGBD
5. controladores e superficie AJAX/WS
6. reaproveitamento e qualidade

## Reaproveitamento em RN/INT/DTO

Para cada funcao, metodo ou classe nova ou alterada em RN/INT/DTO, aplicar o
checklist `U1-U10` de `references/reutilizacao-rn-int-dto.md`.

Pergunta obrigatoria:

- essa funcao realmente precisa existir?

## Arquitetura SEI

- camadas corretas (`RN x INT x DTO x pagina x operacao`)
- link assinado + permissao por acao (`V01/V02`; `G3/G4`)
- padrao transacional `*Controlado` / `*Interno` (`AGENTS.md`)
- efeitos colaterais (email, Solr, integracao externa) apos o commit (`V07`)
- em operacoes API/WS, aplicar `D3` apenas quando houver uso de classe interna
  como contrato/payload sem justificativa; fora desse contexto, uso de classes
  internas suportadas pelas versoes alvo do modulo nao e achado por si so

## Fluxo de dados e superficie de ataque

- mapear entradas relevantes: `PaginaSEI::GET/POST`, payloads AJAX/WS, XML,
  upload, parametros de script e dados persistidos reaproveitados
- rastrear se essas entradas chegam a SQL, HTML/JS, log, arquivo, include,
  desserializacao, redirect, chamada externa ou execucao de comando
- priorizar achados confirmados por fluxo real sobre heuristica solta

## Seguranca transversal

Aplicar `.agents/security/matriz-vulnerabilidades-sei.md` (`V01-V10`) sempre.
Aplicar tambem `.agents/checklists/checklist-seguranca.md`, nos itens `C1-C10`,
para segredos, execucao, desserializacao, arquivos, XML, URLs externas e
dependencias. Reportar apenas o que tiver evidencia `arquivo:linha`.

Secret hardcoded (chave, token ou senha) em codigo ou config entra como `V10` e
deve ser reportado com evidencia.

## Qualidade de codigo

Compor `code-review` apenas na dimensao de qualidade e manutenibilidade:

- legibilidade e clareza dos nomes; coesao alta e acoplamento baixo
- complexidade (ciclomatica, aninhamento, metodos longos)
- tratamento de erro (sem `catch` vazio, sem vazar stacktrace)
- codigo morto, branches/condicoes redundantes, comentarios enganosos
- duplicacao e responsabilidades misturadas
- performance: `N+1`, query em loop, `retObj*` superfaturado, consulta sem
  criterio ou limite
- adequacao de testes: comportamento novo ou alterado tem teste? edge cases
  relevantes estao cobertos?

Sugerir sempre a simplificacao objetiva minima que resolve, sem reescrever o que
ja esta claro.

## Banco, release, permissoes e multi-SGBD

- impacto de release: gates `R1/R3/R4/R6` e `mapa-modulos-scripts.md`
- limites Oracle: tabela/coluna ate 26, indice/FK/sequence ate 30 (`R3`)
- tipos portaveis (sem `AUTO_INCREMENT`, `IDENTITY`, `SERIAL` direto)
- sincronismo de versao em `*Integracao.php`
- recursos SIP `md_<sigla>_<recurso>` e perfis `MD_<sigla>_<recurso>`

## Evidencias complementares

- se ja houver relatorio confiavel disponivel (`composer audit`, SonarQube,
  GitHub secret scanning, dependencia institucional), usar como evidencia
  complementar
- a ausencia dessas ferramentas nao e achado

## Segunda passada obrigatoria

- revisar cada achado e tentar derruba-lo com contexto adicional ou protecao ja existente
- separar fato, hipotese e risco residual
- remover achado que nao se sustente com explorabilidade plausivel ou evidencia suficiente

## Criterios de validacao

- BLOQUEANTE e ALTA exigem evidencia `arquivo:linha` + origem (gate, vetor ou regra).
- Achado `[pre-existente]` nao bloqueia o merge da mudanca atual; entra como risco.
- `TODO:` preexistente, rastreado, fora do escopo e sem risco critico atual nao
  bloqueia o merge. Se indicar falha de permissao, seguranca, transacao,
  release, auditoria ou integridade, classificar conforme o risco real.
- Secao `Seguranca` lista somente achados confirmados; nao listar checks OK no formato padrao.
- Uso de classes internas do core nao e achado por si so; so reportar se houver risco atual de seguranca, transacao, incompatibilidade com as versoes suportadas do modulo ou violacao explicita de contrato API/WS.
- Toda revisao relevante exige segunda passada curta para revalidar explorabilidade,
  contexto e falso positivo dos achados.
- Ambiguidade arquitetural ou evidencia inconclusiva resulta em `precisa de analise humana`.
- Review de modulo completo deve consolidar resultado por gate aplicavel em `PASS`, `WARN` ou `BLOCK`.
- Se nenhum achado relevante for encontrado, a resposta deve dizer isso explicitamente.
- O veredito final e exclusivo desta skill, mesmo quando houver saidas de gates ou `code-review`.

## Formato de saida

- `Triagem`: tipo, arquivos, camadas, gates acionados e escopo
- `Resultados por gate`: `PASS`, `WARN` ou `BLOCK` por skill/gate acionado
- `Bloqueantes`: somente achados BLOQUEANTES introduzidos
- `Riscos relevantes`: ALTA, MEDIA ou pre-existentes relevantes
- `Duplicacao / reaproveitamento`: equivalente encontrado, camada e necessidade real
- `Qualidade`: achados de manutenibilidade e lacunas de teste
- `Seguranca`: somente vetores SEI e achados `C1-C10` com evidencia
- `Impacto SEI`: release, permissoes, multi-SGBD e transacao
- `Recomendacoes`: menor ajuste objetivo que resolve
- `Veredito`: `aprovado`, `aprovado com ajustes`, `bloquear merge` ou `precisa de analise humana`

## Modelo de saida

```text
## Triagem
Tipo: <classificacao> · Arquivos: <n> · Camadas: <pagina/rn/bd/int/...>
Gates acionados: <skills> · Escopo: OK / fora de escopo

## Resultados por gate
- <skill/gate> - PASS | WARN | BLOCK
- <skill/gate> - PASS | WARN | BLOCK

## Bloqueantes
- [BLOQUEANTE][introduzido] <arquivo:linha> - <achado> (V0x / G<n> / regra)

## Riscos relevantes
- [ALTA|MEDIA][introduzido|pre-existente] <arquivo:linha> - <achado>

## Duplicacao / reaproveitamento
- <metodo novo> - equivalente em <RN/arquivo>? camada certa? precisa existir?

## Qualidade
- [sev] <arquivo:linha> - legibilidade/coesao/acoplamento/complexidade/erro/codigo morto/comentario/duplicacao/N+1 + simplificacao sugerida
- Testes: <comportamento novo tem teste? lacuna a cobrir?>

## Seguranca
- somente vetores V01-V10 e achados C1-C10 efetivamente encontrados (nao listar checks OK no formato padrao)

## Impacto SEI
- Banco/scripts/release · Permissoes/SIP · Multi-SGBD · Transacao/pos-commit

## Recomendacoes
- <acao objetiva e minima>

## Veredito
**aprovado | aprovado com ajustes | bloquear merge | precisa de analise humana**
```

## Regra do veredito

- Qualquer BLOQUEANTE aberto -> `bloquear merge`.
- Ambiguidade arquitetural, ou achado relevante sem evidencia conclusiva ->
  `precisa de analise humana`.
- So ALTA, MEDIA ou BAIXA resolviveis com ajuste pontual ->
  `aprovado com ajustes`.
- Sem achado relevante e gates PASS -> `aprovado`.
- Quando nao houver achados, declarar explicitamente:
  `Nao encontrei achados bloqueantes nem riscos relevantes no escopo revisado.`

## Regras

- Achado entra como BLOQUEANTE ou ALTA so com evidencia `arquivo:linha` + gate/regra de origem.
- Sem evidencia conclusiva -> pergunta ao revisor; veredito = `precisa de analise humana`.
- `[pre-existente]` nao bloqueia o merge da mudanca atual - registrar para tratar a parte.
- Mudanca fora de `modulos/**` -> BLOQUEANTE (G6) + recomendar `escrever-adr`.
- Nunca classificar achado para baixo para facilitar aprovacao.

## Limites

- Nao altera codigo. Nao altera o core.
- Nao recria V01-V10 nem as regras dos gates.
- Nao depende de MCP nem de servicos externos para emitir veredito.
