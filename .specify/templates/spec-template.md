# Especificacao de Feature: [NOME DA FEATURE]

**Branch da Feature**: `[###-nome-feature]`
**Criado em**: [DATA]
**Status**: Rascunho
**Entrada**: Descricao do usuario: "$ARGUMENTS"

**Nota**: Este template e copiado por `.specify/scripts/bash/create-new-feature.sh` e preenchido pelo comando `/speckit.specify` ativo.

## Contexto SEI

<!--
  Preencher com informacoes do modulo SEI afetado por esta feature.
  Quanto mais preciso aqui, menos ambiguidade no plan.
-->

- **Modulo/tela afetado**: `fontes/sei/src/main/php/sei/web/modulos/<modulo>/`
  <!-- Dois padroes validos:
       Modulo plano:          modulos/relacionamento-institucional/  |  modulos/ia/
       Modulo com namespace:  modulos/trf4/julgamento/  |  modulos/abc/exemplo/
       NUNCA o nome de uma entidade como subpasta — entidades nao possuem pasta propria.
       Todos os arquivos de uma entidade ficam em dto/, rn/, bd/, int/ do modulo.
       Se indefinido: aplicar o Protocolo de pergunta da constitution (modulo existente ou novo). -->
- **Menus/acoes envolvidas**: [ex.: menu "Solicitar Demanda", acao `listar`, `cadastrar`]
- **Perfil do usuario**: [ex.: servidor interno; usuario externo; ambos]
- **Regra de negocio central**: [descrever em 1-3 frases o que deve ocorrer]
- **Impacto em BD**: [novas tabelas/colunas? sim/nao — se sim, descrever brevemente]
- **Impacto em menus/recursos/perfis (SIP)**: [novo recurso? novo menu? novo perfil?]
- **Impacto em processo/documento/unidade**: [andamentos? tipo de documento? unidade?]
- **Impacto em indexacao/pesquisa**: [Solr/feed/reindexacao? sim/nao — se sim, descrever]

## Restricoes e Riscos Tecnicos

<!--
  Preencher apenas os itens relevantes para esta feature.
-->

- **Encoding**: arquivos PHP em ISO-8859-1 — garantir que editor/IDE esta configurado.
- **Multi-SGBD**: [impacta SQL direto? MySQL/PostgreSQL/Oracle/SQL Server?]
- **Transacoes**: [operacoes de escrita exigem BancoSEI ou InfraRN *Controlado?]
- **Compatibilidade SEI**: [versao minima do SEI necessaria, se aplicavel]
- **Efeitos colaterais**: [pode afetar outros modulos? eventos compartilhados?]

## Cenarios de Usuario e Testes *(obrigatorio)*

<!--
  IMPORTANTE: As historias de usuario devem ser PRIORIZADAS como jornadas de usuario
  ordenadas por importancia. Cada historia de usuario/jornada deve ser TESTAVEL DE FORMA
  INDEPENDENTE — ou seja, se voce implementar apenas UMA delas, ainda deve ter um MVP
  (Produto Minimo Viavel) que entrega valor.

  Atribuir prioridades (P1, P2, P3, etc.) a cada historia, onde P1 e a mais critica.
  Cada historia deve ser uma fatia de funcionalidade que pode ser:
  - Desenvolvida de forma independente
  - Testada de forma independente
  - Entregue de forma independente
  - Demonstrada para usuarios de forma independente
-->

### Historia de Usuario 1 - [Titulo Breve] (Prioridade: P1)

[Descrever esta jornada de usuario em linguagem clara]

**Por que esta prioridade**: [Explicar o valor e por que tem este nivel de prioridade]

**Teste Independente**: [Descrever como pode ser testada de forma independente — ex.: "Pode ser totalmente testada por [acao especifica] e entrega [valor especifico]"]

**Cenarios de Aceite**:

1. **Dado** [estado inicial], **Quando** [acao], **Entao** [resultado esperado]
2. **Dado** [estado inicial], **Quando** [acao], **Entao** [resultado esperado]

---

### Historia de Usuario 2 - [Titulo Breve] (Prioridade: P2)

[Descrever esta jornada de usuario em linguagem clara]

**Por que esta prioridade**: [Explicar o valor e por que tem este nivel de prioridade]

**Teste Independente**: [Descrever como pode ser testada de forma independente]

**Cenarios de Aceite**:

1. **Dado** [estado inicial], **Quando** [acao], **Entao** [resultado esperado]

---

### Historia de Usuario 3 - [Titulo Breve] (Prioridade: P3)

[Descrever esta jornada de usuario em linguagem clara]

**Por que esta prioridade**: [Explicar o valor e por que tem este nivel de prioridade]

**Teste Independente**: [Descrever como pode ser testada de forma independente]

**Cenarios de Aceite**:

1. **Dado** [estado inicial], **Quando** [acao], **Entao** [resultado esperado]

---

[Adicionar mais historias de usuario conforme necessario, cada uma com prioridade atribuida]

### Casos de Borda

<!--
  ACAO NECESSARIA: O conteudo desta secao representa placeholders.
  Preencher com os casos de borda corretos.
-->

- O que acontece quando [condicao de contorno]?
- Como o sistema trata [cenario de erro]?

## Requisitos *(obrigatorio)*

<!--
  ACAO NECESSARIA: O conteudo desta secao representa placeholders.
  Preencher com os requisitos funcionais corretos.
-->

### Requisitos Funcionais

- **RF-001**: Sistema DEVE [capacidade especifica]
- **RF-002**: Sistema DEVE [capacidade especifica]
- **RF-003**: Usuario DEVE conseguir [interacao principal]
- **RF-004**: Sistema DEVE [requisito de dados]
- **RF-005**: Sistema DEVE [comportamento/seguranca]

*Exemplo de requisito pendente de clarificacao:*

- **RF-006**: Sistema DEVE [NECESSITA CLARIFICACAO: detalhe nao especificado]

### Guardrails SEI aplicaveis

<!--
  Marcar os guardrails relevantes para esta feature. Nao e necessario preencher
  todos — apenas os que tem impacto direto na especificacao.
-->

- [ ] Permissao/link assinado: `validarLink` + `validarPermissao` em toda acao
- [ ] `verificarPermissao` em renderizacao condicional de UI
- [ ] `assinarLink` em links de acao
- [ ] Recurso SIP criado: `md_<inst/mod>_<acao>`
- [ ] Perfil SIP criado/atualizado: `MD_<inst/mod>`
- [ ] Transacao necessaria (`BancoSEI` ou `InfraRN *Controlado`)
- [ ] `id_tarefa_modulo` para andamentos (nunca `id_tarefa < 1000`)
- [ ] Auditoria necessaria (`validarAuditarPermissao`)

### Entidades Principais *(incluir se a feature envolve dados)*

- **[Entidade 1]**: [o que representa, atributos principais, sem implementacao]
- **[Entidade 2]**: [o que representa, relacoes com outras entidades]

## Criterios de Sucesso *(obrigatorio)*

<!--
  ACAO NECESSARIA: Definir criterios de sucesso mensuraveis.
  Devem ser independentes de tecnologia e mensuraveis.
-->

### Resultados Mensuraveis

- **CS-001**: [Resultado mensuravel, ex.: "Usuario conclui cadastro em menos de 3 cliques"]
- **CS-002**: [Resultado mensuravel, ex.: "Acao retorna erro amigavel em caso de permissao negada"]
- **CS-003**: [Criterio de validacao tecnica, ex.: "php -l sem erros em todos os arquivos alterados"]

## Premissas

<!--
  ACAO NECESSARIA: O conteudo desta secao representa placeholders.
  Preencher com as premissas corretas baseadas em defaults razoaveis
  escolhidos quando a descricao da feature nao especificou certos detalhes.
-->

- [Premissa sobre o perfil do usuario]
- [Premissa sobre escopo: o que esta fora desta feature]
- [Dependencia de modulo ou servico existente]
- [Versao minima do SEI ou SIP assumida]
