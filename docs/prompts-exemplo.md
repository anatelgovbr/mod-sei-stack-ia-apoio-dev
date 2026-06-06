# Prompts de Exemplo para Desenvolvedores

Use este arquivo como ponto de partida para conversar com a ferramenta.

Escreva em linguagem natural e adapte os exemplos ao seu caso.

Antes de enviar o pedido:

- informe o módulo: `<instituicao>/<modulo>`
- diga se você quer só análise ou se já pode implementar
- descreva o comportamento esperado, não só o problema atual
- se houver erro, cole a mensagem e os passos para reproduzir
- se houver impacto em banco, menu, permissão ou release, diga isso no pedido
- se a regra de negócio não estiver em `PRD.md`, escreva a regra no próprio prompt
- não precisa citar skills internas nem detalhes da stack de IA

Se surgir dúvida sobre regra do projeto, consulte `AGENTS.md` e `PRD.md`.

## Exemplo 1: Só análise, sem alterar arquivos

```text
Analise o módulo <instituicao>/<modulo> sem alterar arquivos ainda.

Objetivo:
- entender <problema, dúvida ou risco>

Quero que você:
- identifique os arquivos mais relevantes
- explique a causa provável do problema
- aponte riscos, dúvidas e dependências
- proponha a melhor abordagem antes de implementar
```

## Exemplo 2: Investigar e corrigir bug

```text
Investigue e corrija um problema no módulo <instituicao>/<modulo>.

Problema:
- comportamento atual: <descreva o erro>
- comportamento esperado: <descreva o correto>

Como reproduzir:
1. <passo 1>
2. <passo 2>
3. <passo 3>

Contexto adicional:
- mensagem de erro: <cole aqui, se existir>
- arquivos suspeitos: <opcional>
- impacto: <negócio, segurança, usabilidade, regressão, etc.>

No final:
- explique a causa raiz
- descreva o que foi alterado
- informe como você validou a correção
```

## Exemplo 3: Criar ou ajustar menu e página

```text
Adicione ou ajuste um item de menu e a página/ação correspondente no módulo <instituicao>/<modulo>.

Objetivo:
- ação: <nome da ação>
- finalidade: <o que a tela faz>
- quem pode acessar: <perfil, permissão ou tipo de usuário>

Entradas e comportamento:
- parâmetros de entrada: <lista ou "nenhum">
- comportamento esperado: <resultado da ação>
- deve aparecer de forma condicional na UI? <sim/não>

No final:
- valide permissão, link assinado e entrada HTTP
- informe se houve impacto em menu, recurso SIP ou release
```

## Exemplo 4: Criar ou ajustar entidade / CRUD

```text
Implemente ou ajuste uma entidade no módulo <instituicao>/<modulo>.

Contexto:
- entidade: <nome>
- objetivo: <o que representa no negócio>
- campos principais: <lista de campos>
- relacionamentos: <FKs, N:N, lookups, etc.>
- precisa de páginas? <sim/não>
- precisa de script de release? <SEI, SIP, ambos ou nenhum>

Preferência:
- usar gerador CRUD? <sim/não>
- se sim, eu quero que você explicite o contrato necessário antes de gerar

No final:
- informe os arquivos alterados
- valide modelagem, naming, transação e impacto de release
```

## Exemplo 5: Ajustar release ou migração

```text
Atualize o release do módulo <instituicao>/<modulo>.

Mudança:
- versão atual: <x.y.z>
- versão alvo: <x.y.z>
- impacto: <SEI, SIP ou ambos>

Alterações esperadas:
- DDL: <tabelas, colunas, índices, FKs, sequences>
- seeds ou parâmetros: <quais>
- recursos, perfis ou menus: <quais>
- observações de compatibilidade: <se houver>

No final:
- valide compatibilidade multi-SGBD
- confirme sincronismo de versão
- descreva riscos e checklist de validação
```

## Exemplo 6: Operação de API ou WebService

```text
Implemente ou ajuste uma operação de API ou WebService no módulo <instituicao>/<modulo>.

Objetivo:
- operação: <nome>
- finalidade: <o que a operação faz>
- entrada esperada: <parâmetros>
- saída esperada: <estrutura ou efeito esperado>

Regras:
- permissões envolvidas: <quais>
- validações obrigatórias: <quais>
- tratamento de erro esperado: <quais casos>

No final:
- explique o fluxo da operação
- informe como a entrada e a saída foram validadas
- descreva como você testou
```

## Exemplo 7: Revisão técnica ou validação de módulo

```text
Faça uma revisão técnica do módulo <instituicao>/<modulo>.

Quero que você revise:
- estrutura por camadas
- permissões e links assinados
- entrada e saída HTTP
- transação e efeitos colaterais
- modelagem de dados
- impacto de release
- riscos de segurança

Entregue:
- achados por prioridade
- arquivos e trechos relevantes
- correções recomendadas
- lacunas de teste ou validação
```

## Exemplo 8: Pedir plano antes de implementar

```text
Quero implementar uma mudança no módulo <instituicao>/<modulo>, mas não execute nada ainda.

Mudança desejada:
- <descreva a demanda>

Antes de alterar arquivos:
- analise o impacto
- identifique os arquivos envolvidos
- diga se há impacto em banco, permissão, menu ou release
- proponha um plano em etapas pequenas
- aguarde minha aprovação para implementar
```

## Dicas rápidas

- Se você quiser só leitura e análise, diga: `não altere arquivos ainda`.
- Se você quiser implementação direta, diga: `pode implementar`.
- Se a regra de negócio não estiver em `PRD.md`, escreva a regra no próprio prompt.
- Se houver decisão arquitetural sensível, peça primeiro uma análise de impacto.
- Se a demanda envolver tabela, coluna, DTO, BD, RN ou script, mencione isso explicitamente.
- Se quiser aprender com a resposta, peça: `explique também o raciocínio e os trade-offs`.
