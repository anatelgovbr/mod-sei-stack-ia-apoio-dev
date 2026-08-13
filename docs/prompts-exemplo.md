# Prompts de Exemplo para Desenvolvedores

## Introdução

Use este arquivo como ponto de partida para conversar com a ferramenta.

Todo trecho entre `<` e `>` (ex.: `<sistema ou módulo>`, `<descreva a demanda>`) é um parâmetro de exemplo: substitua pela informação real referente à ação que você quer executar antes de enviar o prompt.

Escreva em linguagem natural e adapte os exemplos ao seu caso.

Antes de enviar o pedido:

- informe: `<sistema ou módulo>`
- diga se você quer só análise ou se já pode implementar
- descreva o comportamento esperado, não só o problema atual
- se houver erro, cole a mensagem e os passos para reproduzir
- se houver impacto em banco, menu, permissão ou release, diga isso no pedido
- se a regra de negócio não estiver documentada no repositório, escreva a regra no próprio prompt
- não precisa citar skills internas nem detalhes da stack de IA

Se surgir dúvida sobre regra do projeto, consulte `AGENTS.md`, a documentação do módulo e os documentos em `docs/`.

## Dicas Rápidas

- Se você quiser só leitura e análise, use o agente ou modo de planejamento da própria ferramenta, geralmente identificado como `plan`: ele já responde só com leitura e análise, sem alterar arquivo algum.
- Se você quiser implementação direta, diga: `pode implementar`.
- Se a regra de negócio não estiver documentada no repositório, escreva a regra no próprio prompt.
- Se houver decisão arquitetural sensível, peça primeiro uma análise de impacto.
- Se a demanda envolver tabela, coluna, modelo de dados, camada de acesso a dados, regra de negócio ou script, mencione isso explicitamente.
- Se quiser aprender com a resposta, peça: `explique também o raciocínio e os trade-offs`.

## Análise e Planejamento

### Só análise, sem alterar arquivos

**Prompt:**

```text
Analise <sistema ou módulo> sem alterar arquivos ainda.

Objetivo:
- entender <problema, dúvida ou risco>

Quero que você:
- identifique os arquivos mais relevantes
- explique a causa provável do problema
- aponte riscos, dúvidas e dependências
- proponha a melhor abordagem antes de implementar
```

### Pedir plano antes de implementar

**Prompt:**

```text
Quero implementar uma mudança em <sistema ou módulo>, mas não execute nada ainda.

Mudança desejada:
- <descreva a demanda>

Antes de alterar arquivos:
- analise o impacto
- identifique os arquivos envolvidos
- diga se há impacto em banco, permissão, menu ou release
- proponha um plano em etapas pequenas
- aguarde minha aprovação para implementar
```

## Correção de Bugs

### Investigar e corrigir bug

**Prompt:**

```text
Investigue e corrija um problema em <sistema ou módulo>.

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

## Implementação de Funcionalidades

### Criar ou ajustar menu e página

**Prompt:**

```text
Adicione ou ajuste um item de menu e a página/ação correspondente em <sistema ou módulo>.

Objetivo:
- ação: <nome da ação>
- finalidade: <o que a tela faz>
- quem pode acessar: <perfil, permissão ou tipo de usuário>

Entradas e comportamento:
- parâmetros de entrada: <lista ou "nenhum">
- comportamento esperado: <resultado da ação>
- deve aparecer de forma condicional na UI? <sim/não>

No final:
- valide permissão de acesso, proteção da ação contra chamada direta e entrada HTTP
- informe se houve impacto em menu, permissão ou release
```

### Criar ou ajustar entidade / CRUD

**Prompt:**

```text
Implemente ou ajuste uma entidade em <sistema ou módulo>.

Contexto:
- entidade: <nome>
- objetivo: <o que representa no negócio>
- campos principais: <lista de campos>
- relacionamentos: <FKs, N:N, lookups, etc.>
- precisa de páginas? <sim/não>
- precisa de script de release? <quais sistemas ou lados afetados, ou nenhum>

Preferência:
- usar gerador CRUD? <sim/não>
- se sim, eu quero que você explicite o contrato necessário antes de gerar

No final:
- informe os arquivos alterados
- valide modelagem, naming, transação e impacto de release
```

### Operação de API ou WebService

**Prompt:**

```text
Implemente ou ajuste uma operação de API ou WebService em <sistema ou módulo>.

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

## Release e Migração

### Ajustar release ou migração

**Prompt:**

```text
Atualize o release de <sistema ou módulo>.

Mudança:
- versão atual: <x.y.z>
- versão alvo: <x.y.z>
- impacto: <quais sistemas ou lados afetados>

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

## Revisão Técnica

### Revisão técnica ou validação de módulo

**Prompt:**

```text
Faça uma revisão técnica de <sistema ou módulo>.

Quero que você revise:
- estrutura por camadas
- permissões e proteção das ações contra chamada direta
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

## Dicionário de Dados

`dicionario_tabelas.md` e `dicionario_colunas.md` mantêm as descrições semânticas; `CHANGELOG.md` mantém o changelog estrutural. A skill `dicionario-dados-db-scan-codebase-docs` investiga a codebase, os scripts de banco e a documentação disponível para produzir esses artefatos, e reporta proveniência, confiança, conflitos e lacunas ao desenvolvedor durante a execução, sem gravar arquivo dedicado ao relatório.

Os exemplos a seguir funcionam para qualquer sistema ou módulo já reconhecido neste repositório e também para um que ainda não tenha adaptador configurado: basta substituir `<sistema ou módulo>` pelo nome dele. Não é preciso citar nomes internos da skill, adaptadores, critérios de qualidade ou comandos de verificação: informe apenas o que você já sabe, e o que puder ser descoberto no código a skill descobre sozinha.

Adaptador é o arquivo que ensina a skill a reconhecer, localizar e versionar um sistema ou módulo específico: onde fica a fonte estrutural, como a versão é identificada, como buscar no código e como publicar as descrições. Ele fica em `adapters/<família>/<caminho-do-adaptador>.md` e é listado em `registro-adaptadores.md`, ambos na raiz da skill `dicionario-dados-db-scan-codebase-docs`. Você não precisa escrever esse arquivo manualmente: se o sistema ou módulo ainda não tiver adaptador, basta autorizar a criação no próprio prompt, como no exemplo "Criar o adaptador de um sistema ou módulo novo" a seguir. A criação do adaptador sempre acontece dentro de um pedido de criação (ou atualização) do dicionário, nunca como um passo isolado: com a autorização, a skill investiga a codebase, pergunta somente pelas convenções que não conseguir inferir, cria o adaptador completo, o registra e segue direto para gerar o dicionário.

### Criar o adaptador de um sistema ou módulo novo

Use este prompt para o primeiro contato com um sistema ou módulo que a skill ainda não reconhece. A criação do adaptador acontece junto com a geração do dicionário, dentro do mesmo pedido. Informe as convenções que você já souber para reduzir as perguntas que a skill vai precisar fazer; o que você não souber, a skill tenta inferir da codebase antes de perguntar.

**Prompt:**

```text
Crie o adaptador de <sistema ou módulo> nesta skill. Investigue a codebase, crie o adaptador completo e registre-o; na sequência, gere também o dicionário de dados e o changelog estrutural completos.

O que eu já sei sobre ele (use para reduzir perguntas, mas confirme contra o código):
- pistas que identificam este sistema ou módulo (nome, caminhos, prefixo de tabela, pasta de documentação): <se souber>
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber>
- codificação, camadas e onde buscar no código: <se souber>
- títulos e pasta de destino dos dicionários: <se souber>
- particularidades ou exceções conhecidas: <se houver>

Pergunte objetivamente só sobre o que não puder ser inferido nem foi informado acima.
```

### Criar o dicionário de dados de um projeto novo

Use este prompt na primeira vez que for gerar o dicionário de um sistema ou módulo, mesmo que ele ainda não seja reconhecido por nenhum adaptador da skill.

**Prompt:**

```text
Crie o dicionário de dados e o changelog estrutural de <sistema ou módulo>.

Investigue a codebase para identificar a fonte estrutural (scripts de instalação, migrations, schemas ou DDLs), a convenção de versionamento e onde ficam as regras de negócio. Aproveite também qualquer documentação já existente no repositório.

Se nenhum adaptador desta skill ainda reconhecer este sistema ou módulo, você está autorizado a criar e registrar um antes de continuar.
```

### Criar o dicionário com vários materiais complementares

Use quando tiver mais de um material de apoio para o mesmo sistema ou módulo, por exemplo vários arquivos anexados de uma vez, e quiser que a skill dê atenção especial a um deles sem deixar de confirmar tudo contra a codebase.

**Prompt:**

```text
Crie o dicionário de dados e o changelog estrutural de <sistema ou módulo>.

Considere como material complementar todos os arquivos anexados em <nome da pasta ou do conjunto de anexos>.

Dê atenção especial ao arquivo <nome do arquivo mais relevante, ex.: script ou lista de comandos de DDL>, mas confirme tudo contra o código e o esquema real antes de publicar qualquer descrição. Se nenhum adaptador desta skill ainda reconhecer este sistema ou módulo, você está autorizado a criar e registrar um antes de continuar.
```

### Atualizar um dicionário já existente

Use quando o dicionário já existir e você quiser atualizá-lo depois de mudanças no sistema ou após uma nova versão.

**Prompt:**

```text
Atualize o dicionário de dados de <sistema ou módulo> para o estado mais recente da codebase.

Já existem os arquivos de dicionário de dados (e o changelog, se houver). Compare com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando o restante como está.

Se você souber a versão-alvo, os commits ou as migrations específicas da mudança, pode indicar; caso contrário, identifique o escopo pela própria codebase.
```

### Revisar a qualidade de um dicionário existente

Use quando quiser avaliar a qualidade e a consistência de um dicionário já existente, sem modificá-lo.

**Prompt:**

```text
Revise a qualidade e a consistência do dicionário de dados de <sistema ou módulo>, sem alterar nenhum arquivo.

Aponte descrições incompletas, inconsistentes, genéricas ou desatualizadas em relação à estrutura real, e liste claramente qualquer lacuna que impeça considerar a documentação completa.
```

### Gerar prints de tela como insumo complementar

Use este exemplo quando já existir um ambiente de teste do sistema ou módulo disponível (subido localmente ou acessível) antes de rodar o prompt. A automação de navegador não é padronizada no repositório; a ferramenta indicada é apenas um ponto de partida, não uma dependência já disponível em todo ambiente. Qualquer ajuste de configuração feito só para habilitá-lo nesse ambiente é local e não deve ser comitado. Os prints gerados aqui podem ser apontados como material complementar no exemplo "Criar o dicionário com material complementar".

**Prompt:**

```text
Gere os prints de tela de <sistema ou módulo> para servir de insumo complementar ao
dicionário de dados (skill dicionario-dados-db-scan-codebase-docs).

O ambiente de teste de <sistema ou módulo> já está disponível em <endereço ou instrução
para subir o ambiente>, com as credenciais <usuário/senha de teste>. Use <ferramenta de
automação de navegador, ex.: mcr.microsoft.com/playwright:v1.60.0-noble> (baixe a imagem
se ainda não tiver localmente) para rodar um script de automação que:

1. Verifique se <sistema ou módulo> já está ativo/instalado/configurado nessa instância
   de teste. Se não estiver, identifique o mecanismo de ativação e ative-o como ajuste
   local (não comitar), avisando explicitamente o desenvolvedor sobre esse ajuste.
2. Faça login no ambiente de teste.
3. Navegue por todas as telas relevantes de <sistema ou módulo>, criando os dados de
   teste (seeds) necessários para preencher cada tela.
4. Capture um print de cada tela relevante (listagem, formulário vazio, formulário
   preenchido, modal, estado intermediário).
5. Salve os PNGs em <pasta de destino>/<nome-do-sistema-ou-modulo>/screenshots/, organizados
   por subpasta.
6. Exporte os seeds/dados de teste usados no passo 3 (SQL de insert ou passo a passo
   reprodutível) em <pasta de destino>/<nome-do-sistema-ou-modulo>/seeds/, para reaproveitar
   em futuras implementações sem recriar a massa de teste do zero.
```

## Segurança e Vulnerabilidade

### Auditoria exclusiva de segurança e vulnerabilidade

**Prompt:**

```text
Faça uma auditoria exclusiva de segurança e vulnerabilidade do módulo <indicar aqui o módulo que você quer analisar>.

Use a skill `sei-code-review-security` como única orquestradora, no modo de revisão de módulo completo. Acione somente os gates subordinados aplicáveis aos artefatos encontrados e siga `AGENTS.md`, a matriz V01-V10, o checklist C1-C10 e o formato de saída predefinido pela skill.

Escopo:
- revise integralmente o módulo-alvo e a expansão de escopo prescrita pela skill, inclusive páginas, integrações, RN, DTO, BD, DDL e scripts SEI/SIP mapeados quando aplicáveis;
- avalie exclusivamente segurança e vulnerabilidades: não produza achados de qualidade, manutenibilidade, desempenho, estilo, duplicação, cobertura de testes ou funcionalidade, salvo quando forem evidência direta de uma vulnerabilidade concreta;
- use testes, validações locais e análise de fluxo de dados somente para confirmar ou refutar uma vulnerabilidade;
- respeite o limite da skill de não alterar código: não crie arquivos, não aplique patches, nem faça modificações temporárias ou definitivas. A entrega final é somente o relatório.

Confirmação dos achados:
- aplique integralmente os critérios de validação, a análise de fluxo de dados e a segunda passada anti-falso-positivo já previstos na skill;
- inclua como problema apenas vulnerabilidade confirmada pelos critérios da skill; não liste como vulnerabilidade hipótese inconclusiva, heurística isolada, ausência de ferramenta ou teste, `TODO:` preexistente, padrão sem fluxo explorável ou check aprovado;
- quando faltar evidência conclusiva, não a classifique como problema confirmado. Registre-a apenas como limitação ou necessidade de análise humana, conforme o formato da skill.

Priorização:
- mantenha a metodologia já definida no checklist de segurança e liste os problemas do mais prioritário para o menos prioritário: `BLOQUEANTE`, `ALTA`, `MEDIA`, `BAIXA`;
- não invente metodologia concorrente nem rebaixe a severidade para facilitar o veredito.

Relatório:
- inicie obrigatoriamente a resposta com o título exato:
   # Relatório de Problemas Concretos de Segurança e Vulnerabilidade
- após o título, use o formato de saída predefinido pela skill, preservando as seções pertinentes à auditoria: `Triagem`, `Resultados por gate`, `Bloqueantes`, `Riscos relevantes`, `Segurança`, `Impacto SEI`, `Recomendações` e `Veredito`;
- omita as seções ou análises sem relação direta com a segurança;
- mantenha os índices em `Bloqueantes` e `Riscos relevantes` na mesma ordem de prioridade da seção detalhada `Segurança`, sem duplicar a descrição completa;
- para cada problema confirmado, inclua uma única subseção detalhada em `Segurança`, com esta estrutura:

   ### [SEVERIDADE][origem] Título objetivo do problema
   **Problema e impacto:** explique a causa, o impacto e o cenário de exploração confirmado.

   **Referências técnicas e conceituais:** informe o vetor V01-V10, item C1-C10, gate ou regra aplicável e, quando diretamente pertinente, a referência de segurança reconhecida correspondente.

   **Evidências confirmadas:** informe o nome, caminho relativo e linhas de cada arquivo relevante; transcreva em bloco de código o trecho que demonstra a causa.

   **Explorabilidade e validação:** descreva o fluxo de dados, pré-condições, resultado da validação e por que a vulnerabilidade é concreta no contexto analisado.

   **Ajuste de código sugerido, não aplicado:** informe o arquivo e as linhas afetadas e transcreva em bloco de código a alteração mínima que elimina a causa, sem efetivá-la.

- em qualquer transcrição, preserve o contexto necessário à evidência; masque valores de segredos e dados pessoais reais sem ocultar a natureza da vulnerabilidade;
- não inclua recomendações genéricas: cada recomendação deve estar vinculada a um problema confirmado;
- se não houver problema confirmado, declare isso explicitamente no relatório e mantenha o veredito previsto pela skill.
```
