# Exemplos de contrato JSON

Estes arquivos mostram o formato aceito pelo `generate_from_contrato.py`.

O contrato JSON e um artefato interno da IA. Os exemplos existem
apenas para o desenvolvedor montar um JSON compativel e informar o arquivo no
prompt quando quiser pular parte da fase de perguntas.

## Como usar

1. Copie um dos exemplos em `examples/`.
2. Ajuste nomes fisicos, comentarios, labels e relacionamentos para a entidade
   real.
3. Informe o caminho do JSON no prompt ou cole o conteudo para a IA validar e
   usar internamente.
4. Quando houver feature ativa em fluxo Spec Kit, o contrato final deve ser
   salvo em `specs/<feature>/crud-contratos/<tabela>.json`.
5. Fora do Spec Kit, o contrato pode ficar em
   `tmp/crud-contratos/<tabela>.json`.

## Arquivos disponiveis

- `contrato-entidade-minimo.json`: entidade standalone minima, sem FK e sem
  exclusao logica.
- `contrato-entidade-com-fk.json`: entidade simples com PK nativa, FK e
  exclusao logica (`sin_ativo`).
- `contrato-relacao-nn.json`: relacao N:N com PK composta e
  `relacionamentosNn`.

## Quando usar cada exemplo

| Arquivo | Use quando | Cobertura |
| ------- | ---------- | --------- |
| `contrato-entidade-minimo.json` | A entidade nao tem FK e nao usa exclusao logica | PK nativa + campos simples |
| `contrato-entidade-com-fk.json` | A entidade depende de outra tabela e usa `sin_ativo` | PK nativa + FK + `relacionamentos` + `ui` |
| `contrato-relacao-nn.json` | A entidade e uma tabela de relacao entre duas tabelas | PK composta + `relacionamentos` + `relacionamentosNn` |

## Regras importantes

- `entidade.campoPrincipal` deve apontar para uma coluna existente.
- CRUD simples: a PK deve se chamar `id_<tabela>`.
- N:N: a tabela deve seguir `md_<sigla>_rel_<a>_<b>` e
  `regrasGeracao.campoSinAtivo` deve ser `null`.
- Toda tabela e toda coluna precisam de `comentario`.
- Se houver FK, use `relacionamentos` para mapear `coluna`, `tabelaReferencia`
  e `campoExibicao`.
- Para N:N, mantenha `relacionamentos` e `relacionamentosNn` alinhados: o gerador
  usa `relacionamentos` para retornar/exibir nomes relacionados e
  `relacionamentosNn` para montar filtros e selects.
- Entidades com `sin_ativo` geram INT filtrando ativos por padrao e incluindo o
  item selecionado mesmo inativo.

## Exemplo de prompt

```text
Use o contrato em .agents/skills/sei-gerador-crud/examples/contrato-entidade-minimo.json
como base, ajuste para a tabela md_ri_classificacao e gere o CRUD no modulo alvo.
```
