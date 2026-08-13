---
name: dicionario-dados-db-scan-codebase-docs
description: >
  Cria, atualiza e verifica dicionários de dados e changelogs estruturais de banco de dados **a partir de** processamento/pesquisa profunda de codebase, scripts de banco, dicionário já existente, documentação e qualquer material complementar que contextualize requisitos sintáticos, semânticos e função negocial da solução **para definir** descrições de Tabelas e Colunas **com base em** fórmula/padrão de qualidade de descrição previamente definido.
---

# dicionario-dados-db-scan-codebase-docs

Interprete pedidos em linguagem natural e transforme evidências versionadas da codebase em documentação estrutural e semântica verificável.
Regras de conteúdo ficam nas referências; regras de localização e leitura ficam nos adaptadores.

## Fontes de regra

Carregue somente o necessário para a intenção inferida:

| Arquivo | Autoridade sobre |
|---|---|
| `references/contrato-de-adaptador.md` | Seleção do adaptador e tratamento de alvo ainda não suportado; leia sempre |
| `registro-adaptadores.md` | Alvos reconhecidos neste repositório e o adaptador correspondente; consulte ao selecionar o adaptador |
| `references/criacao-adaptador.md` | Composição e contrato de novo adaptador; leia somente depois de autorização explícita |
| `adapters/<família>/<alvo>.md` | Caminhos, convenções e estratégia de busca; leia o adaptador selecionado e as heranças que ele declarar |
| `references/formato-dicionario-de-dados.md` | Forma dos artefatos; leia as seções dos arquivos que serão escritos ou verificados |
| `references/principios-qualidade-dados.md` | Conteúdo, redação e critérios A1 a A10; leia "Critérios de aceitação" sempre e as demais seções quando houver dicionário semântico |
| `references/templates-descricao.md` | Fórmulas obrigatórias para descrições; leia sempre que escrever ou revisar tabelas e colunas |
| `references/insumos-complementares.md` | Leitura e uso de materiais fornecidos; leia somente quando houver insumo |
| `references/processo-analise-semantica.md` | Evidência, confiança, conflito e lacuna; leia integralmente para dicionário semântico e leia as seções correspondentes sempre que houver relatório, conflito ou lacuna |

## Interpretação do pedido

O usuário não precisa conhecer nomes de operação, arquivos ou termos internos. Selecione o alvo pelo contrato de adaptador e determine:

1. **Alvo:** sistema, módulo, esquema ou conjunto de tabelas envolvido.
2. **Intenção:** criar documentação ausente, atualizar documentação existente ou verificar sua consistência.
3. **Artefatos:** dicionário semântico, histórico estrutural ou ambos.
4. **Versão-alvo:** versão declarada pela fonte indicada no adaptador.

Crie quando os artefatos não existirem ou houver pedido de reconstrução; atualize quando existirem e houver mudanças posteriores; verifique sem escrever quando o pedido for de auditoria, revisão ou comparação. Intenção explícita do pedido prevalece sobre o estado dos arquivos: um pedido de verificação nunca cria artefato, mesmo quando ele ainda não existe. Investigue antes de perguntar e agrupe apenas ambiguidades que possam mudar o resultado.

Em pedido semântico sem insumos, convide uma vez e prossiga sem aguardar:

> Se você tiver manuais, capturas de tela, documentos, planilhas ou outros materiais de negócio, posso usá-los como evidência complementar. Eles não são obrigatórios; continuarei analisando e comparando tudo com a codebase.

## Política de execução

Use conteúdo colado, anexos e arquivos locais indicados sem nova autorização. Banco, container, ambiente, URL ou serviço remoto só podem ser lidos depois de buscas locais insuficientes e autorização explícita para a fonte e o escopo. Evidência externa é complementar: não define estrutura, versão, alcance nem resolve divergência estrutural.

## Fluxo

1. Infira alvo, intenção e artefatos; selecione o adaptador e resolva a versão-alvo.
2. Inventarie insumos fornecidos e leia a fonte estrutural até a versão-alvo.
3. Em criação, processe o alcance necessário; em atualização, extraia somente blocos posteriores com mudança estrutural.
4. Para descrições, investigue a codebase conforme o adaptador e confronte os insumos pelo processo semântico.
5. Escreva ou verifique somente os artefatos inferidos, seguindo formato, princípios e fórmulas obrigatórias.
6. Avalie A1 a A10 e execute os subcomandos aplicáveis; marque um critério como não aplicável somente quando seu artefato estiver fora do escopo inferido.
7. Reporte escopo, insumos usados, evidências, conflitos, lacunas e resultados; não publique metodologia ou origem técnica nos artefatos.

Em atualização, mude estrutura e descrição documentadas apenas nos objetos afetados pela mudança solicitada, e registre no `CHANGELOG.md` somente versões com mudança física. Não reescreva descrição de tabela ou coluna fora desse escopo por ajuste de estilo ou fórmula; amplie o escopo somente diante de divergência estrutural confirmada (A8) ou domínio incompleto confirmado (A2), e registre o motivo da ampliação no relatório. Antes de republicar os dicionários, valide contra a fórmula obrigatória as descrições dentro do escopo tratado. Em verificação, avalie `dicionario_tabelas.md` e `dicionario_colunas.md` inteiros e não altere arquivos.

## Ferramenta

Use `scripts/verificar_dicionario.py`, relativo à raiz desta skill. Saída: 0 sem achado, 1 com achado, 2 entrada inválida.
Nos comandos, `<skill>` é a raiz da skill e `<pasta-do-alvo>` é o destino declarado pelo adaptador.

```bash
python3 <skill>/scripts/verificar_dicionario.py formato <pasta-do-alvo>/dicionario_tabelas.md --padrao-versao '<regex de título do adaptador>'
python3 <skill>/scripts/verificar_dicionario.py formato <pasta-do-alvo>/dicionario_colunas.md --checar-ordem --padrao-pk '<padrão do adaptador>' --padrao-versao '<regex de título do adaptador>'
python3 <skill>/scripts/verificar_dicionario.py tabelas-colunas --tabelas <pasta-do-alvo>/dicionario_tabelas.md --colunas <pasta-do-alvo>/dicionario_colunas.md
python3 <skill>/scripts/verificar_dicionario.py changelog <pasta-do-alvo> --padrao-versao '<regex de changelog do adaptador>' --ordem-versoes '<mais-recente,...,mais-antiga>'
python3 <skill>/scripts/verificar_dicionario.py diff --antigo <snapshot-anterior>/dicionario_colunas.md --novo <pasta-do-alvo>/dicionario_colunas.md --json
python3 -m unittest discover -s <skill>/scripts -p 'test_*.py'
```

Rode `python3 -m unittest discover -s <skill>/scripts -p 'test_*.py'` somente depois de alterar `verificar_dicionario.py`. Essa suíte valida a ferramenta em si, não o dicionário de um alvo; não faz parte da verificação rotineira de `formato`, `tabelas-colunas`, `changelog` ou `diff`.
Passe `--padrao-pk`, `--padrao-versao` e `--ordem-versoes` somente quando o adaptador declarar os respectivos valores. Não presuma convenções de outra família técnica.
Rode `tabelas-colunas` quando o dicionário for escrito ou verificado. Antes de atualizar `dicionario_colunas.md`, preserve um snapshot temporário do estado anterior; gere o relatório com esse snapshot em `--antigo` e o arquivo atualizado em `--novo`, nunca com o mesmo arquivo nos dois argumentos.
O verificador lê somente Markdown: A8 continua sendo medido por comparação com a fonte estrutural. Trate código 2 como entrada inválida, nunca como divergência de conteúdo.

## Gates

Bloqueie somente o fato ou artefato afetado quando faltar adaptador para escrita, a versão continuar indeterminada, fontes estruturais divergirem, o alcance for insuficiente ou algum termo da fórmula obrigatória permanecer sem evidência. Continue com os demais objetos e reporte cada lacuna ou conflito.

A entrega exige A1 a A10 registrados, A8 conferido por leitura quando houver dicionário, checks automatizados aplicáveis com código 0 e checks manuais restantes aprovados. `dicionario_tabelas.md`, `dicionario_colunas.md` e `CHANGELOG.md` não podem conter metodologia, origem técnica, nome de classe ou norma.
