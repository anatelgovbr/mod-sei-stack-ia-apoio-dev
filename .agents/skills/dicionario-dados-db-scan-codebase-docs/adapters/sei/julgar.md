# Adaptador: Julgar

Família InfraPHP. Aplique `convencoes-infraphp.md`.

## Reconhecimento

Reconheça Julgar, julgamento, `trf4/julgamento/` e `docs/dicionario_dados/julgar/` como evidências diretas. Nomes sem prefixo, como `sessao_julgamento`, `colegiado`, `algoritmo` e `andamento_sessao`, são provisórios; discrimine-os nos scripts Julgar.

## Fonte estrutural

| Lado | Arquivo | Papel |
|---|---|---|
| SEI | `fontes/sei/src/main/php/sei/scripts/md_julgar_atualizacao_sei.php` | fonte estrutural versionada |
| SIP | `fontes/sei/src/main/php/sip/scripts/md_julgar_atualizacao_sip.php` | fonte obrigatória para conferir cada faixa |

A definição de dados para conferência fica em `fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/dto/` e `bd/`.

## Versionamento

Regras comuns de versão-alvo, âncora, baseline e bloqueios para adaptadores `setArrVersoes` ficam em `convencoes-infraphp.md`.

### Gramática e ordenação

O rodapé usa `setArrVersoes` com chaves `M.m.*` e métodos `versao_M_m_0`. Ordene pelo mapa.

### Identificadores e âncoras

- Assinatura de bloco: `public function versao_M_m_p($strVersaoAtual): void`.
- Parâmetro de instalação: `MD_JULGAR_VERSAO`.
- Auxiliares: descubra chamadas transitivas a partir de cada método mapeado; método apenas definido não pertence à versão.

### Extração por versão

Delimite cada método apontado pelo mapa, preserve a ordem do bloco e siga somente auxiliares chamados por ele. Extraia os lados SEI e SIP separadamente antes de combinar efeitos compatíveis.

### Versão-alvo

Leia o retorno de `public function getVersao(): string` em `MdJulgarIntegracao.php`. É método de instância, não chamada estática. Confira o valor contra `setStrVersaoAtual` do script.

## Títulos

- Dicionários: `Dicionário de Dados do Módulo SEI Julgar`.
- `CHANGELOG.md`: `Changelog do Módulo SEI Julgar`.
- Relatório de atualização: aplique o template de `convencoes-infraphp.md` com slug `julgar`.

## Camadas semânticas

Raiz do código: `fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/`.

| Evidência | Caminhos |
|---|---|
| Estrutura | os dois scripts declarados em "Fonte estrutural" |
| Modelo, regra, consulta e escrita | `dto/`, `rn/`, `bd/` e `int/` |
| Integração | `MdJulgarIntegracao.php` e contratos encontrados no inventário |
| Interface e comportamento | páginas da raiz, `int/` e `js/` |
| Documentação, relatórios, testes e comentários | inventarie na raiz a cada execução |

## Estratégia de busca

Siga a ordem de investigação de `convencoes-infraphp.md` sobre a pasta inteira.

## Particularidades

- Para auxiliar com guarda de execução única chamado por mais de uma versão, atribua o efeito à primeira chamada executada no caminho incremental analisado.
- Tipos literais e métodos de tipo InfraPHP convivem no script e têm a mesma autoridade estrutural.
- Reveja o lado SIP em cada faixa, sem presumir ausência de DDL.

## Validações

- Compare os objetos estruturais com DTO e BD Julgar.
- Confirme a versão-alvo no método de instância e no rodapé do script.
- Confirme que todo auxiliar seguido possui chamada no bloco da versão.
- Rode as validações gerais da skill com `--padrao-pk 'id_{tabela}'` e os objetos técnicos declarados.

## Bloqueios

- Versão-alvo divergente de `setStrVersaoAtual`: bloqueie escrita e validações dependentes da versão; permita verificação parcial no alcance comprovado e reporte ambas as fontes.
- DDL novo no lado SIP incompatível com o SEI: bloqueie e reporte, sem escolher precedência.
- Classificação por nome de tabela sem confirmação no script: bloqueie se ainda houver ambiguidade.

## Destino

- Dicionários e `CHANGELOG.md`: `docs/dicionario_dados/julgar/`.
