# Andamentos (histórico) — regras para módulos

## Regras “hard”
- `id_tarefa < 1000` é reservado do SEI.
- Módulo só pode lançar tarefa reservada `ID_TAREFA=65` (texto livre via atributo `DESCRICAO`).
- Para portabilidade entre instalações, preferir `id_tarefa_modulo`:
  - até 50 chars, maiúsculo, prefixo `MD_<SIGLA>`
  - não pode haver duplicidade

## Variáveis no texto
- Texto pode conter `@VAR@`. O valor é preenchido por `AtributoAndamentoAPI` (`Nome`/`Valor`/`IdOrigem`).
- Há variáveis reservadas do sistema (ex.: `DOCUMENTO`, `PROCESSO`, `USUARIO`, `UNIDADE`, etc.). Preencher com cuidado.

## Cadastro de tarefa do módulo (quando necessário)
- Inserir registro em `tarefa` com `id_tarefa >= 1000`.
- Atualizar a sequência `seq_tarefa` conforme SGBD (MySQL/SQLServer/Oracle/PostgreSQL) se for “manual”.

> Para detalhes completos e exemplos, consulte o manual SEI‑Módulos v5.0 (seção Andamentos).
