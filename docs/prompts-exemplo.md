# Prompts de Exemplo para Desenvolvedores

## Sumário

- [Introdução](#introdução)
- [Templates de Prompts para Utilizar em Casos Reais no SEI](#templates-de-prompts-para-utilizar-em-casos-reais-no-sei)
  - [Pré-requisitos de Automação de Navegador (Playwright e Selenium)](#pré-requisitos-de-automação-de-navegador-playwright-e-selenium)
  - [Correção de Bugs](#correção-de-bugs)
    - [Investigar e corrigir bug](#investigar-e-corrigir-bug)
    - [Investigar e corrigir bug com auxílio do Playwright](#investigar-e-corrigir-bug-com-auxílio-do-playwright)
    - [Investigar e corrigir bug com auxílio do Selenium](#investigar-e-corrigir-bug-com-auxílio-do-selenium)
  - [Fluxo Speckit para Funcionalidade Nova](#fluxo-speckit-para-funcionalidade-nova)
    - [Fluxo padrão](#fluxo-padrão)
    - [Fluxo alternativo (com passos opcionais)](#fluxo-alternativo-com-passos-opcionais)
  - [Ajustes Pontuais](#ajustes-pontuais)
    - [Ajuste pontual de menu ou página existente](#ajuste-pontual-de-menu-ou-página-existente)
    - [Ajuste pontual de entidade existente](#ajuste-pontual-de-entidade-existente)
    - [Ajuste pontual de operação de API ou WebService existente](#ajuste-pontual-de-operação-de-api-ou-webservice-existente)
  - [Revisão Técnica e Segurança](#revisão-técnica-e-segurança)
    - [Revisão técnica completa de módulo](#revisão-técnica-completa-de-módulo)
    - [Revisão técnica de uma dimensão específica](#revisão-técnica-de-uma-dimensão-específica)
    - [Verificar um guardrail específico, sem orquestrador](#verificar-um-guardrail-específico-sem-orquestrador)
    - [Auditoria exclusiva de segurança e vulnerabilidade](#auditoria-exclusiva-de-segurança-e-vulnerabilidade)
    - [Code review de mudanças commitadas](#code-review-de-mudanças-commitadas)
    - [Depois da revisão: marcar ou planejar a correção](#depois-da-revisão-marcar-ou-planejar-a-correção)
  - [Dicionário de Dados](#dicionário-de-dados)
    - [Criar o adaptador de um módulo novo](#criar-o-adaptador-de-um-módulo-novo)
    - [Criar o dicionário de dados de um módulo novo](#criar-o-dicionário-de-dados-de-um-módulo-novo)
    - [Criar o dicionário com vários materiais complementares](#criar-o-dicionário-com-vários-materiais-complementares)
    - [Atualizar um dicionário já existente](#atualizar-um-dicionário-já-existente)
    - [Revisar a qualidade de um dicionário existente](#revisar-a-qualidade-de-um-dicionário-existente)
    - [Gerar prints de tela como insumo complementar](#gerar-prints-de-tela-como-insumo-complementar)

---

## Introdução

Este arquivo reúne prompts prontos para uso real no SEI. Não são ilustrações genéricas: são templates reais para adaptar ao seu caso e enviar.

O `AGENTS.md` já é carregado em toda sessão neste repositório e concentra boa parte das orientações do projeto: os prompts abaixo não repetem o que já está lá.
Repita uma orientação do `AGENTS.md` dentro de um prompt só quando quiser reforçar um ponto MUITO crítico, para reduzir o risco de alucinação nesse ponto específico.

Todo trecho entre `<` e `>` é um parâmetro: substitua pela informação real antes de enviar. Use `<módulo>` quando o alvo é um módulo inteiro (SEI ou SIP) e `<módulo ou arquivo>` quando o alvo pode ser mais específico, como um único arquivo. Exemplo: `<módulo>` vira `licitacao`; `<módulo ou arquivo>` vira `licitacao/rn/LicitacaoRN.php`.

Campo marcado como `<se souber>` ou `<opcional>` que você não tiver como preencher: apague a linha, mas nunca deixe o texto entre `<` e `>` dentro do prompt enviado. Não escreva "não sei" no lugar do campo: se você não sabe, a linha não deveria estar lá.

Nenhum prompt deste arquivo precisa ser enviado igual ao template: eles foram escritos para servir a mais de um módulo e arquivo, e você nem sempre vai ter todo dado ou arquivo disponível na hora. Linha que não se aplica ao seu caso, apague; mande só o que você realmente tem. Quanto mais informação e validação você conseguir dar junto do prompt, mais assertivo o agente tende a ser, mas isso não é obrigatório: o dia a dia tem muitos contextos diferentes, e um prompt mais enxuto também funciona.

Antes de colar mensagem de erro, print de tela ou qualquer evidência bruta em um prompt, nunca inclua, se forem de ambiente de produção:

- senha ou qualquer outra credencial
- dado pessoal (CPF, nome completo, e-mail, endereço)
- segredo (token, chave de API, connection string)

Troque cada um desses valores por um texto genérico, mantendo claro o que está errado.
Em ambiente de teste ou desenvolvimento, pode colar sem trocar nada.

Se a regra de negócio não estiver documentada no repositório, escreva a regra no próprio prompt.

Todo prompt deste arquivo é só o ponto de partida da sessão, não uma interação única: depois do resultado, continue na mesma janela para ajustar, aprofundar ou corrigir o que vier.
Se quiser guardar o conteúdo da sessão (achados, relatório, decisão), peça ao agente para salvar em um `.md` na pasta `specs/`, que é local e não versionada.

---

## Templates de Prompts para Utilizar em Casos Reais no SEI

### Pré-requisitos de Automação de Navegador (Playwright e Selenium)

Consulte esta seção antes de usar qualquer prompt deste arquivo que peça Playwright ou Selenium. Os prompts que usam uma dessas ferramentas apontam para cá em vez de repetir o conteúdo.

Qualquer prompt com automação de navegador exige o ambiente de desenvolvimento do SEI rodando localmente (`README.md`, seção "Ambiente de Desenvolvimento"). Se o alvo for um módulo específico, confirme que ele está ativo nesse ambiente antes de usar o prompt: veja o array `Modulos` em `fontes/sei/src/main/php/sei/config/ConfiguracaoSEI.php`. Se não estiver ativo, peça para o agente ativá-lo (edição local, sem comitar) antes de continuar; não deixe editar sem essa confirmação.

**Playwright:** não vem configurado neste repositório. Você precisa trazer a própria automação de navegador (ex.: a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble`) e confirmar que a ferramenta de IA da sua sessão consegue executá-la. Qualquer ajuste de configuração feito só para habilitá-la é local e não deve ser comitado.

**Selenium:** diferente do Playwright, já vem configurado via Docker em `fontes/sei/ops_sei-docker/tests/` (container `selenium/standalone-chrome` e runner pytest); veja `fontes/sei/ops_sei-docker/README.md` para o comando de execução. A suíte de exemplo ali (login, criação de processo, logout) serve de referência para adaptar a outros cenários. Funciona só em Linux quando o ambiente usa localhost.

### Correção de Bugs

#### Investigar e corrigir bug

Use este prompt como ponto de partida para qualquer bug.
Quanto mais insumos você informar (print, mensagem de erro, chamado, suspeita de causa), menor a investigação exploratória e mais assertiva a correção.

**Prompt:**

```text
Objetivo: analisar e montar um plano de correção para <descreva o defeito em uma frase>, em <módulo ou arquivo>.

Fora de escopo: refatorar código adjacente, renomear método ou arquivo, alterar comportamento de outras funcionalidades da mesma tela.

Fatos verificados:
- comportamento atual: <descreva o erro, com os dados reais usados>
- comportamento esperado: <descreva o correto>
- frequência: <sempre reproduz, intermitente, só em certas condições>
- ambiente onde ocorre: <desenvolvimento, homologação, produção>
- perfil ou usuário afetado: <perfil, permissão ou tipo de usuário>
- mensagem de erro: <cole aqui, se existir, com segredo e dado pessoal mascarados>
- print de tela: <anexe o arquivo de imagem, se existir>

Como reproduzir:
1. <passo 1>
2. <passo 2>
3. <passo 3>

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- desde quando ocorre: <sempre ocorreu, ou começou após uma mudança específica, ex.: "não ocorria na versão 5.1 do módulo, passou a ocorrer na 5.2">
- arquivos ou classes suspeitas: <se já tiver uma suspeita, ex.: "deve estar na BD, no método que monta o filtro">
- mudança recente relacionada: <commit, PR ou release que pode ter causado, se souber, ex.: "a mesma atualização que trocou o componente de data">
- relato do usuário: <cole aqui o texto que ele reportou, ex.: "a listagem está trazendo processo de fevereiro mesmo eu filtrando só janeiro">

Critério de aceite:
1. Sucesso: <entrada concreta e resultado esperado após a correção>
2. Validação: <condição limite e comportamento esperado>
3. Regressão: <o que já funciona nessa tela ou fluxo e precisa continuar funcionando>

Impacto: <negócio, segurança, usabilidade, regressão>

Protocolo de execução:
1. Investigue e apresente a causa raiz com evidência em arquivo e linha, com o plano de correção. Aguarde meu OK antes de editar qualquer coisa.
2. Só então implemente e valide.

Comece a resposta final pela causa raiz confirmada, com evidência em arquivo e linha. Justifique sua resposta.
```

**Exemplo preenchido:** use este padrão de preenchimento para qualquer outro prompt deste arquivo.

```text
Objetivo: analisar e montar um plano de correção para o filtro de período da listagem de licitações, que ignora a data final, em licitacao/pagina/licitacao_lista.php.

Fora de escopo: refatorar código adjacente, renomear método ou arquivo, alterar comportamento dos demais filtros da tela.

Fatos verificados:
- comportamento atual: ao informar data inicial 01/01/2026 e data final 31/01/2026 no filtro da listagem, a data final é ignorada e aparecem registros criados em fevereiro de 2026
- comportamento esperado: a listagem deve mostrar somente registros dentro do período informado, respeitando data inicial e final
- frequência: sempre reproduz quando os dois campos de data são preenchidos
- ambiente onde ocorre: homologação
- perfil ou usuário afetado: qualquer perfil com acesso à listagem
- mensagem de erro: nenhuma, o filtro só não funciona
- print de tela: enviado junto com esta mensagem

Como reproduzir:
1. Abrir a listagem de licitações
2. Preencher data inicial 01/01/2026 e data final 31/01/2026
3. Clicar em filtrar

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- desde quando ocorre: não ocorria na versão 5.1 do módulo, passou a ocorrer depois da atualização para a 5.2
- arquivos ou classes suspeitas: a query do filtro deve estar em bd/LicitacaoBD.php, no método que monta a cláusula WHERE do período
- mudança recente relacionada: meu palpite é a troca do componente de data no filtro, feita na mesma atualização para a 5.2
- relato do usuário: "a listagem de licitações está trazendo processo de fevereiro mesmo eu filtrando só janeiro"

Critério de aceite:
1. Sucesso: com data inicial 01/01/2026 e final 31/01/2026, a listagem retorna somente registros do intervalo, incluindo os criados exatamente em 01/01/2026 e em 31/01/2026
2. Validação: com apenas uma das duas datas preenchida, o filtro aplica só o limite informado e não lança erro
3. Regressão: os demais filtros da listagem continuam funcionando isolados e combinados com o filtro de período

Impacto: usabilidade, usuário vê dados fora do período pedido

Protocolo de execução:
1. Investigue e apresente a causa raiz com evidência em arquivo e linha, com o plano de correção. Aguarde meu OK antes de editar qualquer coisa.
2. Só então implemente e valide.

Comece a resposta final pela causa raiz confirmada, com evidência em arquivo e linha. Justifique sua resposta.
```

#### Investigar e corrigir bug com auxílio do Playwright

Use esta variação quando o bug for difícil de reproduzir só pela descrição, ou quando você quiser confirmação visual do antes e do depois da correção.

Pré-requisito: veja "Pré-requisitos de Automação de Navegador (Playwright e Selenium)", bloco Playwright, no início deste arquivo.

**Prompt:**

```text
Objetivo: analisar e montar um plano de correção para <descreva o defeito em uma frase>, em <módulo ou arquivo>, usando Playwright para reproduzir o bug e validar a correção visualmente.

Fora de escopo: refatorar código adjacente, comitar qualquer ajuste de configuração feito só para habilitar a automação de navegador.

Fatos verificados:
- comportamento atual: <descreva o erro, com os dados reais usados>
- comportamento esperado: <descreva o correto>
- frequência: <sempre reproduz, intermitente, só em certas condições>
- mensagem de erro: <cole aqui, se existir, com segredo e dado pessoal mascarados>
- print de tela anterior: <anexe o arquivo de imagem, se existir>

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- desde quando ocorre: <sempre ocorreu, ou começou após uma mudança específica, ex.: "não ocorria na versão 5.1 do módulo, passou a ocorrer na 5.2">
- arquivos ou classes suspeitas: <se já tiver uma suspeita, ex.: "deve estar na BD, no método que monta o filtro">
- relato do usuário: <cole aqui o texto que ele reportou, ex.: "a listagem está trazendo processo de fevereiro mesmo eu filtrando só janeiro">

Critério de aceite:
1. Sucesso: <entrada concreta e resultado esperado, verificável na tela>
2. Validação: <condição limite e comportamento esperado>
3. Regressão: <o que já funciona nesse fluxo e precisa continuar funcionando>

Acesso ao ambiente de teste:
- endereço: <URL do ambiente de teste, ex.: http://localhost:8000/sei>
- autenticação: use as credenciais de teste já documentadas em `README.md` (usuário `teste`); se precisar de outro perfil, peça a credencial no momento do uso

Passos:
1. Use a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble` (baixe se ainda não tiver localmente) para navegar até <tela ou fluxo onde o bug ocorre>. Se precisar de um estado específico na base (registro, status, permissão) para reproduzir, verifique e prepare você mesmo antes de reproduzir o problema.
2. Capture um print do estado com o bug (antes da correção) e salve em <pasta de destino>.
3. Apresente a causa raiz com evidência em arquivo e linha, com o plano de correção, e aguarde meu OK.
4. Corrija a causa raiz em <módulo ou arquivo>.
5. Repita a navegação e capture um novo print confirmando cada critério de aceite, salvando na mesma pasta.

Referencie os prints de antes e depois como evidência de cada critério de aceite verificado por tela. Justifique sua resposta.
```

#### Investigar e corrigir bug com auxílio do Selenium

Use esta variação quando quiser reproduzir e validar o bug via Selenium em vez de Playwright. A lógica é a mesma: reproduzir o bug, corrigir e validar visualmente o antes e o depois.

Pré-requisito: veja "Pré-requisitos de Automação de Navegador (Playwright e Selenium)", bloco Selenium, no início deste arquivo.

**Prompt:**

```text
Objetivo: analisar e montar um plano de correção para <descreva o defeito em uma frase>, em <módulo ou arquivo>, usando Selenium para reproduzir o bug e validar a correção visualmente.

Fora de escopo: refatorar código adjacente, comitar qualquer ajuste de configuração feito só para habilitar a automação de navegador, alterar `test_suiteBasics.py` (crie uma cópia adaptada em vez de editar o script de referência).

Fatos verificados:
- comportamento atual: <descreva o erro, com os dados reais usados>
- comportamento esperado: <descreva o correto>
- frequência: <sempre reproduz, intermitente, só em certas condições>
- mensagem de erro: <cole aqui, se existir, com segredo e dado pessoal mascarados>
- print de tela anterior: <anexe o arquivo de imagem, se existir>

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- desde quando ocorre: <sempre ocorreu, ou começou após uma mudança específica, ex.: "não ocorria na versão 5.1 do módulo, passou a ocorrer na 5.2">
- arquivos ou classes suspeitas: <se já tiver uma suspeita, ex.: "deve estar na BD, no método que monta o filtro">
- relato do usuário: <cole aqui o texto que ele reportou, ex.: "a listagem está trazendo processo de fevereiro mesmo eu filtrando só janeiro">

Critério de aceite:
1. Sucesso: <entrada concreta e resultado esperado, verificável na tela>
2. Validação: <condição limite e comportamento esperado>
3. Regressão: <o que já funciona nesse fluxo e precisa continuar funcionando>

Acesso ao ambiente de teste:
- endereço: <URL do ambiente de teste, ex.: http://localhost:8000/sei>
- autenticação: use as credenciais de teste já documentadas em `README.md` (usuário `teste`); se precisar de outro perfil, peça a credencial no momento do uso
- driver e navegador: container `selenium/standalone-chrome` já configurado em `fontes/sei/ops_sei-docker/tests/` (comandos em `fontes/sei/ops_sei-docker/tests/Makefile`, alvo `test_selenium_basico1`)

Passos:
1. Copie `fontes/sei/ops_sei-docker/tests/Selenium/PythonExported/test_suiteBasics.py` para um script novo e adapte para reproduzir o bug em <tela ou fluxo onde o bug ocorre>, reaproveitando o container Selenium já configurado. Capture um print do estado com o bug (antes da correção) em <pasta de destino>.
2. Apresente a causa raiz com evidência em arquivo e linha, com o plano de correção, e aguarde meu OK.
3. Corrija a causa raiz em <módulo ou arquivo>.
4. Repita a navegação e capture um novo print confirmando cada critério de aceite, salvando na mesma pasta.

Referencie os prints de antes e depois como evidência de cada critério de aceite verificado por tela. Justifique sua resposta.
```

### Fluxo Speckit para Funcionalidade Nova

Use o fluxo Speckit sempre que a demanda criar algo que ainda não existe: nova funcionalidade, nova entidade CRUD completa, novo menu e página, nova operação de API ou WebService, ou release com DDL novo. O Speckit já orquestra as skills pertinentes (verificação de página, RN, banco de dados, controladores, geração de scripts de release, etc.) ao longo das fases, então não repita esse trabalho em um prompt avulso. Para uma mudança pontual em algo que já existe, veja a seção Ajustes Pontuais a seguir.

Quanto mais detalhado o pedido em `/speckit.specify`, melhor a especificação gerada. Descreva contexto, comportamento esperado e critério de aceite em linguagem de negócio; deixe stack técnica, classe e padrão de implementação para o `/speckit.plan`, que é a fase certa para essa decisão.

O exemplo abaixo usa como demanda "adicionar um filtro de período (data inicial e data final) na listagem de um módulo"; troque pelo objetivo real antes de enviar.

#### Fluxo padrão

Especificar, planejar, decompor em tarefas e implementar, nessa ordem.

**1. Especificar:**

```text
/speckit.specify

Quero <descreva a funcionalidade nova em uma frase, ex.: "adicionar um filtro de período (data inicial e data final) na listagem"> de <módulo>.

Contexto:
- quem usa: <perfil ou permissão>
- comportamento esperado: <resultado esperado, ex.: "a listagem mostra somente os registros criados dentro do período informado">
- fora de escopo: <o que essa funcionalidade não faz>

Critério de aceite inicial:
1. Sucesso: <entrada concreta e resultado esperado>
2. Validação: <condição limite e comportamento esperado>

Fatos verificados:
- regra de negócio confirmada: <se houver, ex.: "só usuários com perfil Administrador podem ver processos sigilosos no filtro">
- tela ou fluxo semelhante que serve de referência: <se houver, ex.: "o filtro de período da tela de processos já faz isso, usar de referência">

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- impacto suposto em permissão, menu ou release: <se souber, ex.: "não deve exigir permissão nova, é só um filtro a mais na tela existente">

Justifique sua resposta.
```

**2. Planejar:**

```text
/speckit.plan

No módulo <módulo>, use `PaginaSEI::POST/GET` com normalização de tipo para os <novos parâmetros da funcionalidade, ex.: parâmetros de filtro de período>. Reaproveite tela, RN ou padrão semelhante já existente no módulo antes de propor algo novo.

No plano, declare explicitamente: impacto em script de release SEI e SIP, impacto em recurso e perfil SIP, e impacto em estrutura de banco. Se algum desses impactos existir, marque-o como ponto de parada para minha decisão antes da implementação.

Justifique sua resposta.
```

**3. Decompor em tarefas:** a decomposição usa a spec e o plano já aprovados nas fases anteriores; não precisa de argumento adicional.

```text
/speckit.tasks
```

**4. Implementar:** executa as tarefas geradas; não precisa de argumento adicional.

```text
/speckit.implement
```

#### Fluxo alternativo (com passos opcionais)

Mesmo fluxo, com três passos opcionais inseridos: clarificar dúvidas antes de planejar, gerar um checklist de requisitos sensíveis antes de decompor, e analisar consistência antes de implementar.

**1. Especificar:** igual ao fluxo padrão.

**2. Clarificar:** use quando a spec tiver ambiguidade; a skill faz até 5 perguntas objetivas e grava as respostas na própria spec. Não precisa de argumento adicional.

```text
/speckit.clarify
```

**3. Planejar:** igual ao fluxo padrão.

**4. Gerar checklist:** use quando o domínio for sensível, como permissão, auditoria ou modelagem de dados, e você quiser validar a qualidade dos requisitos antes de decompor em tarefas.

```text
/speckit.checklist

Gere um checklist para validar os requisitos de permissão e auditoria de <funcionalidade, ex.: filtro de período> antes de implementar.

Justifique sua resposta.
```

**5. Decompor em tarefas:** igual ao fluxo padrão.

**6. Analisar:** checa a consistência entre spec, plano e tarefas antes de implementar. Não precisa de argumento adicional.

```text
/speckit.analyze
```

**7. Implementar:** igual ao fluxo padrão.

### Ajustes Pontuais

Use estes prompts para uma mudança pequena em algo que já existe, não para criar algo novo. Linha de corte: se a mudança cabe em uma frase e não cria tela, menu, permissão ou operação novos, é ajuste pontual, mesmo que inclua uma coluna ou campo novo em uma entidade já existente. Se a demanda cria menu, entidade, operação ou release novos, ou se o ajuste puxa mudança em cascata (nova tela, nova permissão, novo fluxo), use o fluxo Speckit da seção anterior em vez destes.

Exemplo de ajuste pontual: adicionar um campo de observação em uma entidade já existente. Exemplo de funcionalidade nova: criar uma tela de aprovação com um fluxo de permissão que ainda não existe.

#### Ajuste pontual de menu ou página existente

**Prompt:**

```text
Objetivo: <descreva o ajuste em uma frase> em <módulo ou arquivo>.

Fora de escopo: refatorar código adjacente, criar CSS ou JS novo quando já existir equivalente no módulo, alterar outras ações da mesma tela.

Fatos verificados:
- comportamento atual, observado por mim: <descreva>
- comportamento desejado: <descreva>
- perfil ou permissão envolvida: <se você confirmou qual é>

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- página ou fluxo semelhante que serve de referência: <se houver, ex.: "a tela de configuração de outro módulo já tem um botão parecido">
- recurso SIP que eu acredito ser o correspondente: <se souber, ex.: "md_abc_editar">

Critério de aceite:
1. Sucesso: <perfil, entrada concreta e resultado esperado na tela>
2. Permissão: usuário sem o recurso SIP correspondente não acessa a ação, nem pela interface nem por chamada direta à URL com link não assinado
3. Regressão: <o que já funciona nessa tela e precisa continuar funcionando>

Protocolo de execução:
1. Leia por completo os arquivos envolvidos e apresente o plano do ajuste.
2. Aguarde meu OK.
3. Implemente e valide.

Ao final, informe se houve impacto em menu, permissão ou release, e cite o arquivo e a linha onde `validarLink`, `validarPermissao` e `assinarLink` cobrem a ação alterada. Justifique sua resposta.
```

#### Ajuste pontual de entidade existente

**Prompt:**

```text
Objetivo: <descreva o ajuste em uma frase> na entidade <nome> em <módulo ou arquivo>.

Fora de escopo: refatorar código adjacente, renomear coluna ou entidade existente, criar script de release novo quando o módulo já tiver script mapeado em `.agents/references/mapa-modulos-scripts.md`.

Fatos verificados:
- entidade e tabela: <nome>
- o que muda: <novo campo, validação ou comportamento>
- motivo: <por que a mudança é necessária>
- campos afetados e tipo esperado: <se você confirmou>

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- quem consome essa entidade hoje: <telas, RN, API, se souber, ex.: "só a tela de cadastro e o relatório mensal">
- impacto suposto em release: <se souber, ex.: "só coluna nova, não deve exigir migração de dado existente">

Critério de aceite:
1. Sucesso: <operação concreta, com dado de entrada, e resultado esperado no banco e na tela>
2. Validação: <valor nulo, limite de tamanho ou violação de restrição, e comportamento esperado>
3. Regressão: <o que já funciona com essa entidade e precisa continuar funcionando>

Antes de implementar:
- consulte `docs/dicionario_dados/<módulo>/dicionario_tabelas.md` e `dicionario_colunas.md` para a semântica já registrada da tabela e das colunas envolvidas
- se a tabela ou a coluna estiver ausente do dicionário, ou divergente do código, avise antes de prosseguir

Protocolo de execução:
1. Leia por completo os arquivos envolvidos, consulte o dicionário e apresente o plano do ajuste, já declarando o impacto em release.
2. Aguarde meu OK.
3. Implemente e valide.

Ao final, informe: nomes de tabela e coluna dentro do limite de 26 caracteres e nomes de índice, FK e sequence dentro de 30; se a entidade pertence a um módulo mapeado em `.agents/references/mapa-modulos-scripts.md`, o estado da atualização dos scripts SEI/SIP de release e da sincronização de versão; e se o dicionário de dados precisa ser atualizado depois desta mudança. Justifique sua resposta.
```

#### Ajuste pontual de operação de API ou WebService existente

**Prompt:**

```text
Objetivo: <descreva o ajuste em uma frase> na operação <nome> em <módulo ou arquivo>.

Fora de escopo: quebrar contrato existente de entrada ou saída sem me avisar, trocar classe da API oficial por objeto interno, refatorar código adjacente.

Fatos verificados:
- operação: <nome>
- o que muda: <novo parâmetro, nova validação ou correção de comportamento>
- contrato atual: <classe `Entrada*API` / `Saida*API` ou catálogo de referência, se você confirmou>
- consumidores conhecidos da operação: <se você confirmou quais são>

Hipóteses não confirmadas: trate como pista, confirme no código e me avise se refutar.
- impacto suposto em quem consome: <descreva>
- outros pontos do módulo que talvez usem a mesma operação: <se souber, ex.: "o relatório de exportação chama o mesmo método internamente">

Critério de aceite:
1. Sucesso: <payload de entrada concreto e payload de saída esperado>
2. Validação: <entrada inválida, campo ausente ou sem autorização, e erro esperado>
3. Compatibilidade: consumidores existentes continuam funcionando sem alteração, ou a quebra é declarada explicitamente na entrega

Protocolo de execução:
1. Leia por completo a operação e seus pontos de chamada e apresente o plano do ajuste, já declarando se há quebra de contrato.
2. Aguarde meu OK.
3. Implemente e valide.

Ao final, descreva: o fluxo da operação após a mudança, como entrada e saída são validadas, e a autorização aplicada por ação ou serviço no controlador correspondente. Justifique sua resposta.
```

### Revisão Técnica e Segurança

#### Revisão técnica completa de módulo

Use quando quiser pegar legado e débito técnico de vários tipos de uma vez: padrões de codificação, vulnerabilidade e segurança, modelagem de banco, conformidade com a API de módulos e impacto de release. O relatório final é a soma dos relatórios das skills de gate acionadas por `sei-revisao-tecnica`, não uma análise nova por cima delas. Se já tiver uma suspeita de onde o problema está, preencha o campo "Suspeita específica": ajuda a skill priorizar a investigação sem deixar de cobrir o resto do escopo.

**Prompt:**

```text
Use a skill `sei-revisao-tecnica` para fazer uma revisão técnica de <módulo ou arquivo>.

Suspeita específica: <preencha se já tiver uma, ou apague a linha>

Use o formato de relatório padrão da skill, com a seção de segunda passada preenchida (executada e o que mudou de classificação, ou "nenhuma mudança") e os candidatos a tarefas ordenados da maior para a menor prioridade, como próximo passo sugerido a partir de cada achado. Detalhe também as lacunas de teste ou validação encontradas.

Não altere nenhum arquivo, ref, tarefa ou issue durante a revisão. Justifique sua resposta.
```

**Exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para fazer uma revisão técnica de fontes/sei/src/main/php/sei/web/modulos/peticionamento/.

Use o formato de relatório padrão da skill, com a seção de segunda passada preenchida (executada e o que mudou de classificação, ou "nenhuma mudança") e os candidatos a tarefas ordenados da maior para a menor prioridade, como próximo passo sugerido a partir de cada achado. Detalhe também as lacunas de teste ou validação encontradas.

Não altere nenhum arquivo, ref, tarefa ou issue durante a revisão. Justifique sua resposta.
```

#### Revisão técnica de uma dimensão específica

Use quando quiser restringir a revisão a uma única dimensão técnica, em vez de rodar a completa. Se já tiver uma suspeita de onde o problema está dentro dessa dimensão, preencha o campo "Suspeita específica": ajuda a skill priorizar a investigação sem deixar de cobrir o resto do escopo.

**Prompt:**

```text
Use a skill `sei-revisao-tecnica` para revisar exclusivamente <dimensão técnica, ex.: transação e auditoria, permissões, entrada e saída HTTP> em <módulo ou arquivo>.

Restrinja o relatório a essa dimensão: omita achados de outras dimensões, salvo quando forem evidência direta de um problema concreto na dimensão revisada.

Suspeita específica: <preencha se já tiver uma, ou apague a linha>

Use o formato de relatório padrão da skill, mantendo apenas as seções pertinentes à dimensão revisada, com a seção de segunda passada preenchida (executada e o que mudou de classificação, ou "nenhuma mudança") e os candidatos a tarefas ordenados da maior para a menor prioridade.

Não altere nenhum arquivo, ref, tarefa ou issue durante a revisão. Justifique sua resposta.
```

**Exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para revisar exclusivamente transação e efeitos colaterais em fontes/sei/src/main/php/sei/web/modulos/peticionamento/rn/MdPetIntEmailNotificacaoRN.php.

Restrinja o relatório a essa dimensão: omita achados de outras dimensões, salvo quando forem evidência direta de um problema concreto na dimensão revisada.

Use o formato de relatório padrão da skill, mantendo apenas as seções pertinentes à dimensão revisada, com a seção de segunda passada preenchida (executada e o que mudou de classificação, ou "nenhuma mudança") e os candidatos a tarefas ordenados da maior para a menor prioridade.

Não altere nenhum arquivo, ref, tarefa ou issue durante a revisão. Justifique sua resposta.
```

#### Verificar um guardrail específico, sem orquestrador

Use estes prompts quando já souber qual artefato mudou e quiser o veredito de um gate específico, sem passar pelas doze dimensões do `sei-revisao-tecnica`. Troque `<arquivo ou diretório>` pelo artefato exato.

**Página:**

```text
Use a skill `sei-verificacao-pagina` para verificar <arquivo de página>.

Reporte o veredito de cada guardrail aplicável (PASS, WARN ou BLOCK), com arquivo e linha de evidência para cada um.

Não altere nenhum arquivo durante a verificação. Justifique sua resposta.
```

**RN:**

```text
Use a skill `sei-verificacao-rn` para verificar <arquivo ou diretório rn/>.

Reporte o veredito de cada guardrail aplicável (PASS, WARN ou BLOCK), com arquivo e linha de evidência para cada um.

Não altere nenhum arquivo durante a verificação. Justifique sua resposta.
```

**Banco de dados:**

```text
Use a skill `sei-verificacao-banco-dados` para verificar <DTO, BD, diretório de módulo ou script DDL>, no modo <adhoc, pre_generate, audit ou release_check>.

Reporte o veredito de cada entidade (PASS, WARN ou BLOCK), com arquivo e linha de evidência para cada erro ou aviso.

Não altere nenhum arquivo durante a verificação. Justifique sua resposta.
```

**Controladores:**

```text
Use a skill `sei-verificacao-controladores` para verificar <arquivo *Integracao.php>.

Reporte o veredito de cada guardrail aplicável (PASS, WARN ou BLOCK), com arquivo e linha de evidência para cada um.

Não altere nenhum arquivo durante a verificação. Justifique sua resposta.
```

**Tarefa:**

```text
Use a skill `sei-verificacao-tarefa` para verificar <script de tarefa ou diretório scripts/>.

Reporte o veredito de cada guardrail aplicável (PASS, WARN ou BLOCK), com arquivo e linha de evidência para cada um.

Não altere nenhum arquivo durante a verificação. Justifique sua resposta.
```

#### Auditoria exclusiva de segurança e vulnerabilidade

Use quando quiser uma auditoria restrita à dimensão Segurança, com a matriz V01-V10 e o checklist C1-C10 aplicados integralmente. Se já tiver uma suspeita de vetor específico, preencha o campo "Suspeita específica": ajuda a skill priorizar a investigação sem deixar de cobrir o resto do escopo.

**Prompt:**

```text
Use a skill `sei-revisao-tecnica` para uma auditoria exclusiva de segurança e vulnerabilidade do módulo <indicar aqui o módulo que você quer analisar>, em modo de revisão de módulo completo.

Restrinja o relatório à dimensão Segurança: omita achados de qualidade, manutenibilidade, desempenho, estilo, duplicação, cobertura de testes ou funcionalidade, salvo quando forem evidência direta de uma vulnerabilidade concreta.

Suspeita específica: <preencha se já tiver uma, ou apague a linha>

Aplique integralmente a matriz V01-V10 (`.agents/security/matriz-vulnerabilidades-sei.md`) e o checklist C1-C10 (`.agents/checklists/checklist-seguranca.md`). Inclua como achado confirmado somente o que resistir à segunda passada anti-falso-positivo da skill com fluxo explorável demonstrado; achado `incerto` ou sem evidência de exploração fica registrado como `incerto`, nunca como vulnerabilidade confirmada. Não rebaixe a severidade de um achado confirmado para facilitar o parecer.

Inicie a resposta com o título exato:
# Relatório de Problemas Concretos de Segurança e Vulnerabilidade

Em seguida, use o formato de relatório padrão da skill, mantendo apenas as seções pertinentes à dimensão Segurança, com a seção de segunda passada preenchida (executada e o que mudou de classificação, ou "nenhuma mudança") e os candidatos a tarefas ordenados da maior para a menor prioridade.

Não altere nenhum arquivo, ref, tarefa ou issue durante a revisão. Justifique sua resposta.
```

**Exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para uma auditoria exclusiva de segurança e vulnerabilidade do módulo fontes/sei/src/main/php/sei/web/modulos/peticionamento/, em modo de revisão de módulo completo.

Restrinja o relatório à dimensão Segurança: omita achados de qualidade, manutenibilidade, desempenho, estilo, duplicação, cobertura de testes ou funcionalidade, salvo quando forem evidência direta de uma vulnerabilidade concreta.

Aplique integralmente a matriz V01-V10 (`.agents/security/matriz-vulnerabilidades-sei.md`) e o checklist C1-C10 (`.agents/checklists/checklist-seguranca.md`). Inclua como achado confirmado somente o que resistir à segunda passada anti-falso-positivo da skill com fluxo explorável demonstrado; achado `incerto` ou sem evidência de exploração fica registrado como `incerto`, nunca como vulnerabilidade confirmada. Não rebaixe a severidade de um achado confirmado para facilitar o parecer.

Inicie a resposta com o título exato:
# Relatório de Problemas Concretos de Segurança e Vulnerabilidade

Em seguida, use o formato de relatório padrão da skill, mantendo apenas as seções pertinentes à dimensão Segurança, com a seção de segunda passada preenchida (executada e o que mudou de classificação, ou "nenhuma mudança") e os candidatos a tarefas ordenados da maior para a menor prioridade.

Não altere nenhum arquivo, ref, tarefa ou issue durante a revisão. Justifique sua resposta.
```

#### Code review de mudanças commitadas

Exige um ponto fixo Git válido (commit, branch ou tag) e `HEAD` já commitado; worktree sem commit não serve de entrada para este prompt. Rode uma vez por merge, sobre o diff acumulado da branch contra a base, não a cada commit individual.

**Prompt:**

```text
Use a skill `code-review` para revisar as mudanças commitadas desde <branch ou merge request, comparado com a base>.

Contexto:
- escopo da mudança: <resumo>
- pontos de atenção conhecidos: <opcional>

Execute somente Standards por meio de `sei-revisao-tecnica`.
Não procure nem avalie spec, requisito ou issue nesta versão.

Não altere arquivos, refs, tarefas ou issues. Preserve o parecer técnico emitido por `sei-revisao-tecnica`. Justifique sua resposta.
```

**Exemplo preenchido:**

```text
Use a skill `code-review` para revisar as mudanças commitadas desde origin/fix_intimacao_lote_timeout, comparado com a base master.

Contexto:
- escopo da mudança: correção do botão de responder intimação em fontes/sei/src/main/php/sei/web/modulos/peticionamento/PeticionamentoIntegracao.php e rn/MdPetIntRelDestinatarioRN.php, para calcular a situação por intimação em vez de agregada por protocolo, corrigindo o caso de procurador especial com múltiplas empresas

Não altere arquivos, refs, tarefas ou issues. Justifique sua resposta.
```

#### Depois da revisão: marcar ou planejar a correção

Os dois prompts abaixo são continuação da mesma conversa, logo depois que uma revisão, auditoria ou code review acima já respondeu com o relatório: não cole nem repita os achados, o agente já tem o relatório na tela. Escolha um dos dois caminhos; nenhum dos dois corrige nada sozinho.

**Marcar TODO: a partir de um relatório de revisão**

Use quando quiser só registrar a dívida no código, sem planejar a correção agora.

```text
Marque com TODO: os achados WARN e o passivo preexistente do relatório que você acabou de me entregar, um comentário por achado, na linha do próprio achado, neste formato:

// TODO: <descrição objetiva em uma linha>

Aplique achado por achado, com minha confirmação antes de cada um. Nunca marque achado classificado como BLOCK; esses exigem correção, não marcação.

Não corrija a causa de nenhum achado nesta etapa, só marque.

Justifique sua resposta.
```

**Transformar achados em especificação e tarefas**

Use quando tiver vários achados para coordenar e quiser uma lista de tarefas rastreável, para corrigir depois (em outra sessão, ou por outra pessoa) ou agora mesmo.

```text
Transforme os achados do relatório que você acabou de me entregar para <módulo ou arquivo> em uma especificação de correção e uma lista de tarefas.

Para cada achado, gere uma tarefa com: título objetivo, arquivo e linha, ação mínima, critério de aceite (o gate ou controle volta a passar) e dependência entre tarefas, se houver. Ordene as tarefas da maior para a menor prioridade (BLOCK primeiro, depois WARN).

Salve a especificação e a lista de tarefas em um `.md` na pasta `specs/`.

Pare aqui. Se eu pedir para implementar agora, use o Ajuste pontual ou o Investigar e corrigir bug correspondente para cada tarefa, achado por achado, com minha confirmação antes de cada um.

Justifique sua resposta.
```

### Dicionário de Dados

`dicionario_tabelas.md` e `dicionario_colunas.md` mantêm as descrições semânticas; `CHANGELOG.md` mantém o changelog estrutural. A skill `dicionario-dados-db-scan-codebase-docs` investiga a codebase, os scripts de banco e a documentação disponível para produzir esses artefatos, e reporta proveniência, confiança, conflitos e lacunas ao desenvolvedor durante a execução, sem gravar arquivo dedicado ao relatório.

Os exemplos a seguir funcionam para qualquer módulo já reconhecido neste repositório, inclusive o núcleo SEI ou SIP quando for o alvo. Para um módulo que ainda não tenha adaptador, crie o adaptador primeiro (exemplo "Criar o adaptador de um módulo novo" logo abaixo) antes de usar os demais exemplos desta seção. Cite a skill `dicionario-dados-db-scan-codebase-docs` pelo nome no prompt, como nos demais exemplos deste arquivo. Não é preciso citar o adaptador do módulo: uma vez criado e registrado, a skill já sabe localizá-lo sozinha. Também não é preciso citar critérios de qualidade ou comandos de verificação internos à skill; o que puder ser descoberto no código, a skill descobre sozinha.

Adaptador é o arquivo que ensina a skill a reconhecer, localizar e versionar um módulo específico: onde fica a fonte estrutural, como a versão é identificada, como buscar no código e como publicar as descrições. Ele fica em `adapters/<família>/<caminho-do-adaptador>.md` e é listado em `registro-adaptadores.md`, ambos na raiz da skill `dicionario-dados-db-scan-codebase-docs`. Você não precisa escrever esse arquivo manualmente: use o prompt "Criar o adaptador de um módulo novo" a seguir para criar e registrar o adaptador antes de gerar o dicionário.

#### Criar o adaptador de um módulo novo

Use este prompt para o primeiro contato com um módulo que a skill ainda não reconhece, quando quiser criar só o adaptador agora e gerar o dicionário depois, em um pedido separado (exemplo "Criar o dicionário de dados de um módulo novo" a seguir). Informe as convenções que você já souber para reduzir as perguntas que a skill vai precisar fazer; o que você não souber, a skill tenta inferir da codebase antes de perguntar.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador de <módulo>. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.

O que eu já sei sobre ele:
- pistas que identificam este módulo (nome, caminhos, prefixo de tabela, pasta de documentação): <se souber, ex.: "prefixo md_abc_, tabelas em fontes/sei/.../modulos/abc/dto/">
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber, ex.: "sei_atualizar_versao_modulo_abc.php">
- codificação, camadas e onde buscar no código: <se souber, ex.: "ISO-8859-1, camadas dto/rn/bd padrão InfraPHP">
- títulos e pasta de destino dos dicionários: <se souber, ex.: "docs/dicionario_dados/abc/">
- particularidades ou exceções conhecidas: <se houver, ex.: "módulo tem tabela compartilhada com outro módulo, não duplicar no dicionário">

Trate os itens acima como pista, não como conclusão: confirme cada um contra a codebase e me avise se algum divergir.

Pergunte objetivamente só sobre o que não puder ser inferido nem foi informado acima. Justifique sua resposta.
```

#### Criar o dicionário de dados de um módulo novo

Use este prompt na primeira vez que for gerar o dicionário de um módulo, depois que o módulo já tiver um adaptador (crie primeiro com "Criar o adaptador de um módulo novo", se ainda não existir).

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural de <módulo>.

Investigue a codebase para identificar a fonte estrutural (scripts de instalação, migrations, schemas ou DDLs), a convenção de versionamento e onde ficam as regras de negócio. Aproveite também qualquer documentação já existente no repositório.

Ao final, informe explicitamente: as tabelas ou colunas cuja semântica você não conseguiu confirmar na codebase, e o que faltou para confirmá-las. Justifique sua resposta.
```

#### Criar o dicionário com vários materiais complementares

Use quando tiver mais de um material de apoio para o mesmo módulo, por exemplo vários arquivos anexados de uma vez, e quiser que a skill dê atenção especial a um deles sem deixar de confirmar tudo contra a codebase.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural de <módulo>.

Considere como material complementar todos os arquivos anexados em <nome da pasta ou do conjunto de anexos>.

Dê atenção especial ao arquivo <nome do arquivo mais relevante, ex.: script ou lista de comandos de DDL>, mas confirme tudo contra o código e o esquema real antes de publicar qualquer descrição.

Ao final, informe explicitamente onde o material complementar divergiu do código, e qual das duas fontes você adotou em cada divergência. Justifique sua resposta.
```

#### Atualizar um dicionário já existente

Use quando o dicionário já existir e você quiser atualizá-lo depois de mudanças no módulo ou após uma nova versão.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados de <módulo> para o estado mais recente da codebase.

Já existem os arquivos de dicionário de dados (e o changelog, se houver). Compare com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando o restante como está.

Se você souber a versão-alvo, os commits ou as migrations específicas da mudança, pode indicar; caso contrário, identifique o escopo pela própria codebase.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente. Justifique sua resposta.
```

#### Revisar a qualidade de um dicionário existente

Use quando quiser avaliar a qualidade e a consistência de um dicionário já existente, sem modificá-lo.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados de <módulo>, sem alterar nenhum arquivo.

Aponte descrições incompletas, inconsistentes, genéricas ou desatualizadas em relação à estrutura real, e liste claramente qualquer lacuna que impeça considerar a documentação completa. Justifique sua resposta.
```

#### Gerar prints de tela como insumo complementar

Use este exemplo quando já existir um ambiente de teste do módulo disponível (subido localmente ou acessível) antes de rodar o prompt. Os prints gerados aqui podem ser apontados como material complementar no exemplo "Criar o dicionário com vários materiais complementares".

Pré-requisito: veja "Pré-requisitos de Automação de Navegador (Playwright e Selenium)", bloco Playwright, no início deste arquivo.

**Prompt:**

```text
Gere os prints de tela de <módulo> para servir de insumo complementar ao
dicionário de dados (skill `dicionario-dados-db-scan-codebase-docs`).

O ambiente de teste de <módulo> já está disponível em <endereço ou instrução
para subir o ambiente>. Para autenticar, leia a credencial de <variável de ambiente
ou arquivo local não versionado>; se não houver, peça a credencial no momento do uso.
Nunca use credencial de produção.

Use a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble`
(baixe se ainda não tiver localmente) para rodar um script de automação que:

1. Verifique se <módulo> já está ativo nessa instância de teste, consultando
   o array `Modulos` em `fontes/sei/src/main/php/sei/config/ConfiguracaoSEI.php`.
   Se não estiver ativo, pergunte se devo ativá-lo (edição local, sem comitar) antes
   de continuar; não edite sem essa confirmação.
2. Faça login no ambiente de teste.
3. Navegue por todas as telas relevantes de <módulo>, criando os dados de
   teste (seeds) necessários para preencher cada tela.
4. Capture um print de cada tela relevante (listagem, formulário vazio, formulário
   preenchido, modal, estado intermediário).
5. Salve os PNGs em <pasta de destino>/<nome-do-modulo>/screenshots/, organizados
   por subpasta.
6. Exporte os seeds/dados de teste usados no passo 3 (SQL de insert ou passo a passo
   reprodutível) em <pasta de destino>/<nome-do-modulo>/seeds/, para reaproveitar
   em futuras implementações sem recriar a massa de teste do zero.

Ao final, liste as telas que não conseguiu capturar e o motivo. Justifique sua resposta.
```
