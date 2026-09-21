# Adaptador: SEI

Família InfraPHP. Aplique `convencoes-infraphp.md`.

## Reconhecimento

Reconheça SEI, núcleo do SEI, core do SEI e `docs/dicionario_dados/sei/` como evidências diretas. Nome de tabela sem prefixo de módulo é provisório; discrimine-o pelo script, DTOs e destino.

## Fonte estrutural

`fontes/sei/src/main/php/sei/scripts/atualizar_versao_sei.php`, classe `VersaoSeiRN extends InfraScriptVersao`. A definição de dados para conferência fica em `fontes/sei/src/main/php/sei/web/dto/` e `bd/`; ela não substitui o script versionado.

## Versionamento

Regras comuns de versão-alvo, âncora, assinatura de bloco, baseline e bloqueios para adaptadores `setArrVersoes` ficam em `convencoes-infraphp.md`.

### Gramática e ordenação

O rodapé chama `setArrVersoes` com chaves de faixa `M.m.*` e valores `versao_M_m_0`. Ordene pelas chaves do mapa, não pelo nome isolado do método.

## Vocabulário de negócio

Estes termos são legados na estrutura física do SEI, mas o vocabulário de negócio usado por usuário, manual e documentação funcional é outro. Ao redigir prosa (descrição de tabela, descrição de coluna e demais textos livres do dicionário), traduza os termos abaixo; nunca altere o identificador físico correspondente.

| Termo físico/legado (prosa) | Termo de negócio a usar na prosa |
|---|---|
| procedimento | processo |
| tipo de procedimento | tipo de processo |
| serie | tipo de documento |

- Aplique a tradução somente em prosa; identificador físico preserva a forma definida em "Identificadores e âncoras", inclusive quando citado entre crases dentro de uma frase. Ajuste artigo, adjetivo e pronome da frase para manter a concordância correta em português com o termo de negócio substituído; não é necessária uma regra mecânica passo a passo para isso.
- Não aplique a tradução de `serie` quando o termo não se referir à classificação do tipo de documento do SEI (por exemplo, série histórica ou série temporal).
- CHANGELOG.md relata efeito estrutural sobre o identificador físico; não aplique esta tradução a ele.

### Identificadores e âncoras

- Versões sem método próprio pertencem à faixa explícita `M.m.*`; não crie bloco implícito para patch.

### Extração por versão

Localize a entrada do mapa, delimite o método apontado por contagem de chaves e preserve a ordem das operações. Siga apenas auxiliares chamados pelo bloco e atribua somente os efeitos estruturais que eles executam. Quando houver ramificação por banco, compare os resultados antes de declarar uma estrutura comum.

### Versão-alvo

Leia `const SEI_VERSAO` em `fontes/sei/src/main/php/sei/web/SEI.php` a cada execução. A faixa estrutural acima não é a versão corrente e não deve ser usada como título por substituição.

## Títulos

- Dicionários: `Dicionário de Dados do SEI`.
- `CHANGELOG.md`: `Changelog do SEI`.
- Relatório de atualização: aplique o template de `convencoes-infraphp.md` com slug `sei`.

## Camadas semânticas

| Evidência | Caminhos |
|---|---|
| Documentação | `docs/manual_desenvolvimento_md/*.md` pertinente |
| Estrutura | `sei/scripts/atualizar_versao_sei.php` |
| Modelo, regra, consulta e escrita | `sei/web/dto/`, `rn/` e `bd/` |
| Integração | `sei/web/api/`, `ws/` e `.wsdl` |
| Interface e comportamento | páginas `sei/web/*.php` e `sei/web/js/*.js` |
| Relatórios, testes e comentários | inventarie no escopo a cada execução |

## Estratégia de busca

Siga a ordem de investigação de `convencoes-infraphp.md`. Exclua `sei/web/modulos/`, editores e dependências vendorizadas.

## Particularidades

- Rotinas `fix*` só integram uma versão quando há chamada comprovada dentro do bloco mapeado.
- Operações de reparo de índices sobre listas devem ser atribuídas apenas quando o objeto resultante for determinável pelo código.
- Tabelas de módulo não integram o esquema do núcleo mesmo quando referenciadas pelo SEI.

## Validações

- Confirme que nenhuma tabela `md_*` foi incluída no dicionário do núcleo.
- Compare cada objeto tocado com DTO e BD quando existirem.
- Valide que a versão do título veio de `SEI_VERSAO`, separada da faixa estrutural.
- Restrinja criação de entradas a objetos alcançados por blocos estruturais comprovados.

## Bloqueios

- Tabela isolada compatível com mais de um alvo: bloqueie até a confirmação do alvo.

## Destino

- Dicionários e `CHANGELOG.md`: `docs/dicionario_dados/sei/`.
