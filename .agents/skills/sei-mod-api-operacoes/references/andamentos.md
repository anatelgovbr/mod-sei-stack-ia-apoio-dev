# Andamentos (histórico), regras para módulos

## Regras “hard”
- `id_tarefa` é numérico. Valores menores que 1000 são reservados do SEI.
- Módulo só pode lançar a exceção `id_tarefa=65` com o atributo `DESCRICAO`.
- `id_tarefa_modulo` é textual, tem até 50 caracteres e usa o prefixo `MD_<SIGLA>_`.
- `id_tarefa` e `id_tarefa_modulo` não podem ter duplicidade em suas dimensões.
- Para portabilidade entre instalações, prefira `id_tarefa_modulo` quando a operação aceitar esse contrato.

## Variáveis no texto
- Texto pode conter `@VAR@`. O valor é preenchido por `AtributoAndamentoAPI` (`Nome`/`Valor`/`IdOrigem`).
- Há variáveis reservadas do sistema (ex.: `DOCUMENTO`, `PROCESSO`, `USUARIO`, `UNIDADE`, etc.). Preencher com cuidado.

## Cadastro de tarefa do módulo (quando necessário)
- Inserir registro em `tarefa` com `id_tarefa >= 1000`.
- Atualizar a sequência `seq_tarefa` conforme SGBD (MySQL/SQLServer/Oracle/PostgreSQL) se for “manual”.

> Para detalhes completos e exemplos, consulte o manual SEI‑Módulos v5.0 (seção Andamentos).
