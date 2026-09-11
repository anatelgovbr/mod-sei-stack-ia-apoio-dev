# Contrato de adaptador

Autoridade sobre: inferência, seleção, registro e tratamento de alvo sem adaptador.

## 1. Seleção do adaptador

Infira o alvo antes de pedir confirmação. Combine, nesta ordem de utilidade, as pistas que estiverem disponíveis:

1. Contexto funcional e sistemas citados no pedido ou na conversa.
2. Caminho de arquivo, pasta de documentação, anexo ou artefato indicado.
3. Nome de tabela, prefixo, esquema, módulo e relações encontradas na codebase.
4. Fonte estrutural, definição de dados e versão descobertas durante a inspeção do repositório.

Compare o conjunto de pistas com `Reconhecimento` dos adaptadores registrados. Não exija que o usuário nomeie o alvo nem descarte uma inferência apenas porque uma pista isolada é insuficiente.

- Um único adaptador compatível: selecione-o e informe a inferência no resultado.
- Mais de um adaptador plausível: inspecione as fontes discriminantes declaradas por eles. Se a ambiguidade persistir, peça uma confirmação objetiva que apresente as alternativas e a evidência de cada uma.
- Nenhum adaptador compatível: aplique a [seção 3](#3-alvo-sem-adaptador).

Conflito encontrado depois da seleção não troca o adaptador; trate-o pelo processo semântico.

## 2. Registro

O registro de alvos reconhecidos fica em `../registro-adaptadores.md`, na raiz desta skill. Consulte-o para localizar o adaptador aplicável; se o alvo não constar, trate como alvo sem adaptador e aplique a [seção 3](#3-alvo-sem-adaptador).

Forma de uma linha de registro:

| Alvo | Arquivo | Família técnica |
|---|---|---|
| `<nome do sistema ou módulo reconhecido>` | `adapters/<família>/<caminho-do-adaptador>.md` | `<família tecnológica>` |

## 3. Alvo sem adaptador

A ausência de adaptador nunca autoriza presumir caminho, linguagem, persistência, codificação, versionamento, identificadores, âncoras, templates ou destino.

Em pedido de criação ou atualização:

1. Deixe dicionários, `CHANGELOG.md` e relatório de atualização por escrever.
2. Reporte o alvo inferido, as pistas usadas e as convenções ainda indeterminadas.
3. Pergunte se o usuário autoriza criar e registrar o adaptador. Sem autorização explícita, encerre sem escrita.
4. Com autorização, carregue `criacao-adaptador.md`, complete o contrato, registre o adaptador e retome o fluxo.

Em pedido de verificação, siga sem adaptador e sem tocar em arquivo. Compare apenas o que puder ser estabelecido sem convenções presumidas e reporte claramente:

- escopo que foi possível reconhecer;
- verificações executadas;
- lacunas causadas pela ausência do adaptador;
- conclusões que não puderam ser emitidas.

Insumos fornecidos não ampliam nem precisam integrar o adaptador. Qualquer outra leitura externa segue a política de execução de `../SKILL.md`.
