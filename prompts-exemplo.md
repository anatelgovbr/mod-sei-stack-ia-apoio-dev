# Prompts de Exemplo para Usar no SEI

## Sumário

- [Introdução](#introdução)
- [Templates de Prompts para Utilizar em Casos Reais no SEI](#templates-de-prompts-para-utilizar-em-casos-reais-no-sei)
  - [Pré-requisitos de Automação de Navegador (Playwright e Selenium)](#pré-requisitos-de-automação-de-navegador-playwright-e-selenium)
  - [Loop de Verificação](#loop-de-verificação)
  - [Correção de Bugs](#correção-de-bugs)
    - [Investigar e corrigir bug](#investigar-e-corrigir-bug)
    - [Investigar e corrigir bug com auxílio do Playwright](#investigar-e-corrigir-bug-com-auxílio-do-playwright)
    - [Investigar e corrigir bug com auxílio do Selenium](#investigar-e-corrigir-bug-com-auxílio-do-selenium)
  - [Fluxo Speckit para Funcionalidade Nova](#fluxo-speckit-para-funcionalidade-nova)
    - [Fluxo padrão](#fluxo-padrão)
    - [Fluxo alternativo (com passos opcionais)](#fluxo-alternativo-com-passos-opcionais)
  - [Revisão Técnica (inclui Segurança e Vulnerabilidade)](#revisão-técnica-inclui-segurança-e-vulnerabilidade)
    - [Revisão Técnica de alterações](#revisão-técnica-de-alterações)
    - [Revisão Técnica de módulo ou arquivo](#revisão-técnica-de-módulo-ou-arquivo)
    - [Revisão Técnica de Dimensões Específicas](#revisão-técnica-de-dimensões-específicas)
    - [Variações de Saída da Revisão Técnica](#variações-de-saída-da-revisão-técnica)
      - [Revisão Técnica em PDF](#revisão-técnica-em-pdf)
      - [Gerar as issues ou tarefas técnicas](#gerar-as-issues-ou-tarefas-técnicas)
      - [Para uma revisão já entregue](#para-uma-revisão-já-entregue)
    - [Depois da revisão: marcar ou planejar a correção](#depois-da-revisão-marcar-ou-planejar-a-correção)
  - [Dicionário de Dados](#dicionário-de-dados)
    - [Criar o adaptador](#criar-o-adaptador)
    - [Criar o dicionário de dados](#criar-o-dicionário-de-dados)
    - [Atualizar o dicionário](#atualizar-o-dicionário)
    - [Revisar a qualidade do dicionário](#revisar-a-qualidade-do-dicionário)
    - [Gerar prints de tela como insumo complementar](#gerar-prints-de-tela-como-insumo-complementar)
  - [Modos Auxiliares (Skills Externas de Uso Geral)](#modos-auxiliares-skills-externas-de-uso-geral)
    - [Interrogar um plano ou um pedido utilizando o grill-me](#interrogar-um-plano-ou-um-pedido-utilizando-o-grill-me)
    - [Comprimir a resposta utilizando o caveman](#comprimir-a-resposta-utilizando-o-caveman)

---

## Introdução

Este arquivo reúne exemplos reais de prompts para usar no SEI. Escolha o que corresponde à sua necessidade, preencha os campos indicados e copie o bloco inteiro para a conversa com o agente.

O `AGENTS.md` é carregado em toda sessão deste repositório e concentra as regras do projeto, então os prompts abaixo não repetem o que já está lá. Repita uma orientação do `AGENTS.md` dentro de um prompt só quando quiser reforçar um ponto muito crítico, para reduzir o risco de o agente falhar justamente nesse ponto.

O `AGENTS.md` e as skills definem as regras de execução. Os prompts informam o objetivo, o alvo e as escolhas específicas de cada pedido, como revisar apenas um assunto ou aguardar sua aprovação antes de implementar.

Na revisão técnica, a skill já exige evidências e uma segunda verificação para descartar falsos positivos. Por isso, o prompt não precisa repetir essas etapas nem terminar com uma solicitação genérica de justificativa. Nos pedidos de investigação, os exemplos indicam quais evidências apresentar e como comunicar uma conclusão que ainda não foi confirmada. Fontes: `AGENTS.md`, seções "Guardrails Universais" e "Regras de Decisão"; `sei-revisao-tecnica/SKILL.md`, seção "Segunda passada obrigatória".

Nos blocos para copiar, os campos entre `<` e `>` são informações que você deve preencher. Estes são os campos que aparecem em mais de um prompt:

| Campo | O que preencher | Exemplo |
|---|---|---|
| `<nome do módulo>` | Só o nome do módulo | `peticionamento` |
| `<nome do sistema ou do módulo>` | O nome do módulo, do sistema inteiro ou da base de dados | `peticionamento` |
| `<caminho do módulo ou arquivo>` | A pasta do módulo ou um arquivo dentro dela | `fontes/sei/src/main/php/sei/web/modulos/peticionamento/` |
| `<caminho do arquivo>` | Um arquivo só | `fontes/sei/src/main/php/sei/web/modulos/litigioso/rn/MdLitLancamentoRN.php` |
| `<caminho da pasta ou do arquivo>` | Qualquer pasta ou arquivo, sem depender de módulo | `fontes/sei/src/main/php/sei/web/modulos/peticionamento/` |

Os demais campos aparecem em um prompt só e o próprio texto entre `<` e `>` diz o que preencher. Datas de relatórios, identificadores de achados e nomes de arquivos de saída são gerados pelo agente.

Se um campo disser "se souber", "se houver", "se existir", "se você confirmou" ou "opcional" e você não tiver a informação, apague a linha inteira. Substitua os demais campos antes de enviar e nunca envie um prompt com texto entre `<` e `>` ainda dentro dele. Quando faltar uma informação necessária, descreva o que você sabe; o agente pode investigar ou pedir o dado que falta.

Nenhum prompt precisa ser enviado igual ao template. Os templates servem a mais de um módulo e a mais de um arquivo, e você nem sempre vai ter todo dado disponível na hora. Apague a linha que não se aplica ao seu caso e mande só o que você tem de fato: quanto mais informação e validação você der, mais assertivo o agente tende a ser, mas um prompt enxuto também funciona.

Os exemplos preenchidos mostram como adaptar os modelos. Informe o que observou, o resultado esperado e as evidências disponíveis. Apresente suspeitas como hipóteses, para que o agente possa conferi-las.

Antes de enviar mensagens de erro, capturas de tela ou outros materiais, oculte estes valores reais, independentemente do ambiente:

- senha ou qualquer outra credencial
- dado pessoal (CPF, nome completo, e-mail, endereço)
- segredo (token, chave de API ou credencial na configuração de conexão)

Troque cada valor por um texto genérico, mantendo claro o que está errado. Ambientes de teste e desenvolvimento também podem conter credenciais válidas ou dados reais.

Se a regra de negócio não estiver documentada no repositório, escreva a regra no próprio prompt.

Todo prompt deste arquivo é só o ponto de partida da sessão, não uma interação única: depois do resultado, continue na mesma janela para ajustar, aprofundar ou corrigir o que vier. Se quiser guardar o conteúdo da sessão (achados, relatório, decisão), peça ao agente para salvar em um arquivo Markdown (`.md`) na pasta `specs/`, que é local e não versionada.

A última seção do arquivo, "Modos Auxiliares (Skills Externas de Uso Geral)", não tem prompt de demanda. Ela reúne dois modos opcionais que se combinam com qualquer prompt anterior, para comprimir a resposta ou para interrogar um plano ou um pedido antes de implementar.

---

## Templates de Prompts para Utilizar em Casos Reais no SEI

### Pré-requisitos de Automação de Navegador (Playwright e Selenium)

Consulte esta seção antes de usar qualquer prompt deste arquivo que peça Playwright ou Selenium. Os prompts que usam uma dessas ferramentas apontam para cá em vez de repetir o conteúdo.

Qualquer prompt com automação de navegador exige o ambiente de desenvolvimento do SEI rodando localmente (`README.md`, seção "Ambiente de Desenvolvimento"). Se o alvo for um módulo específico, confirme que ele está ativo nesse ambiente antes de usar o prompt: veja o array `Modulos` em `fontes/sei/src/main/php/sei/config/ConfiguracaoSEI.php`. Se o módulo não estiver ativo, peça ao agente que o ative (edição local, sem comitar) antes de continuar; não deixe o agente editar esse arquivo sem a sua confirmação.

**Playwright:** não vem configurado neste repositório. Você precisa trazer a sua própria automação de navegador, por exemplo a imagem Docker `mcr.microsoft.com/playwright` na tag que você for usar; os prompts deste arquivo usam a tag `v1.60.0-noble` como ilustração. Confirme que a ferramenta de IA da sua sessão consegue executá-la. Qualquer ajuste de configuração feito só para habilitá-la é local e não deve ser comitado.

**Selenium:** ao contrário do Playwright, já vem configurado via Docker em `fontes/sei/ops_sei-docker/tests/`, com o container `selenium/standalone-chrome` e um runner pytest. Para rodar a suíte de exemplo (login, criação de processo, logout), use `make test_selenium_basico1` dentro de `fontes/sei/ops_sei-docker/tests/`. Essa suíte serve de referência para você adaptá-la a outros cenários. Essa configuração funciona só em Linux, com o ambiente em localhost.

### Loop de Verificação

A skill `gauntlet-loop-forge` recebe um prompt que você já tem e devolve o mesmo prompt com a técnica de loop de verificação acrescentada. Ela só escreve o prompt e para: executar é um pedido separado, em uma janela nova.

Para agregar a técnica, acrescente esta linha ao início ou ao fim de qualquer prompt deste arquivo, antes de enviar:

```text
Use a skill `gauntlet-loop-forge` para acrescentar a técnica de loop ao prompt <acima/abaixo>.
```

Antes de acionar o loop, confirme que a tarefa é complexa ou que um erro nela é difícil de reverter. Em tarefa pequena e reversível, o loop custa mais do que resolve.

Onde o loop compensa:

| Demanda | Quando o loop compensa |
|---|---|
| Correção de bug | A correção muda comportamento em fluxo crítico, mexe em transação ou migra dado, e precisa preservar o que já funciona. |
| Pedido inicial e entregáveis do Speckit | O documento de uma fase é insumo de todas as fases seguintes, e o `/speckit-analyze` só roda depois do `/speckit-tasks`. |
| Revisão técnica e de segurança | O código vai para produção, trata dado pessoal ou já causou incidente. |

**Modelo para executar o prompt com loop:** prefira modelos intermediários e mais baratos. Exemplos em 2026: Luna e Terra (GPT), Haiku e Sonnet (Claude). Eles tendem a gastar menos tokens e, com o loop e os critérios bem definidos no prompt, entregam bom resultado. Modelos de topo, como Opus e Fable (Claude) ou Sol e Astra (GPT), tendem a alongar o loop, porque o mecanismo de execução do próprio modelo já repete e reverifica passos por conta própria, e o gasto de tokens cresce muito.

### Correção de Bugs

#### Investigar e corrigir bug

Use este prompt como ponto de partida para qualquer bug. Quanto mais insumos você informar (print, mensagem de erro, chamado, suspeita de causa), menor a investigação exploratória e mais assertiva a correção.

**Prompt:**

```text
Objetivo: investigar o defeito abaixo e apresentar o plano de correção. Depois do meu OK, implementar a correção.

Defeito: <descreva o defeito em uma frase>.
Local: <caminho do módulo ou arquivo>.

Fora de escopo: refatorar código adjacente, renomear método ou arquivo, alterar comportamento de outras funcionalidades da mesma tela.

Fatos verificados:
- comportamento atual: <descreva o erro com os valores necessários para reproduzi-lo, ocultando segredos e dados pessoais>
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

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- desde quando ocorre: <sempre ocorreu, ou começou após uma mudança específica, ex.: "não ocorria na versão 5.1 do módulo, passou a ocorrer na 5.2">
- arquivos ou classes suspeitas: <se já tiver uma suspeita, ex.: "deve estar na BD, no método que monta o filtro">
- mudança recente relacionada: <commit, PR ou release que pode ter causado, se souber, ex.: "a mesma atualização que trocou o componente de data">
- relato do usuário: <cole aqui o texto que ele reportou, ex.: "a listagem está trazendo processos de fevereiro mesmo eu filtrando só janeiro">

Critério de aceite:
1. Sucesso: <entrada concreta e resultado esperado após a correção>
2. Validação: <condição limite e comportamento esperado>
3. Regressão: <o que já funciona nessa tela ou fluxo e precisa continuar funcionando>

Impacto: <negócio, segurança, usabilidade, regressão>

Protocolo de execução:
1. Investigue o defeito. Se confirmar a causa, apresente as evidências (arquivo e linha) e o plano de correção; caso contrário, informe o que falta verificar. Aguarde meu OK antes de editar qualquer coisa.
2. Só então implemente e valide.
```

**Exemplo preenchido, filtro de período que ignora o intervalo:** use este padrão de preenchimento para qualquer outro prompt deste arquivo. O exemplo descreve um defeito hipotético em uma tela real do módulo `peticionamento`, para você ver o preenchimento com caminhos verdadeiros.

```text
Objetivo: investigar o defeito abaixo e apresentar o plano de correção. Depois do meu OK, implementar a correção.

Defeito: o filtro de período da listagem de indisponibilidades ignora o intervalo e retorna somente os registros com data exatamente igual à informada.
Local: fontes/sei/src/main/php/sei/web/modulos/peticionamento/md_pet_indisponibilidade_lista.php.

Fora de escopo: refatorar código adjacente, renomear método ou arquivo, alterar comportamento dos demais filtros da tela.

Fatos verificados:
- comportamento atual: com Início 01/01/2026 00:00 e Fim 31/01/2026 23:59, a listagem volta vazia, mesmo havendo indisponibilidades cadastradas dentro desse intervalo
- comportamento esperado: a listagem deve mostrar todas as indisponibilidades do intervalo informado, respeitando início e fim
- frequência: sempre reproduz quando os dois campos de data são preenchidos
- ambiente onde ocorre: homologação
- perfil ou usuário afetado: qualquer perfil com acesso à listagem de indisponibilidades
- mensagem de erro: nenhuma, o filtro só não funciona
- print de tela: enviado junto com esta mensagem

Como reproduzir:
1. Abrir a listagem de indisponibilidades do módulo Peticionamento
2. Preencher Início 01/01/2026 00:00 e Fim 31/01/2026 23:59
3. Clicar em pesquisar

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- desde quando ocorre: sempre ocorreu, ninguém do time lembra do filtro funcionando por intervalo
- arquivos ou classes suspeitas: os campos txtDtInicio e txtDtFim parecem ser aplicados como igualdade no DTO, e não como faixa de datas na BD do módulo
- relato do usuário: "filtrei o mês de janeiro e a tela não trouxe nenhuma indisponibilidade, mas elas aparecem na lista sem filtro"

Critério de aceite:
1. Sucesso: com Início 01/01/2026 00:00 e Fim 31/01/2026 23:59, a listagem mostra as indisponibilidades do intervalo, incluindo a que começa em 01/01/2026 e a que termina em 31/01/2026
2. Validação: com apenas um dos dois campos preenchido, o filtro aplica só o limite informado e não lança erro
3. Regressão: os demais filtros e a ordenação da listagem continuam funcionando isolados e combinados com o filtro de período

Impacto: usabilidade, o usuário conclui que não existe indisponibilidade no período consultado

Protocolo de execução:
1. Investigue o defeito. Se confirmar a causa, apresente as evidências (arquivo e linha) e o plano de correção; caso contrário, informe o que falta verificar. Aguarde meu OK antes de editar qualquer coisa.
2. Só então implemente e valide.
```

#### Investigar e corrigir bug com auxílio do Playwright

Use esta variação quando o bug for difícil de reproduzir só pela descrição, ou quando você quiser confirmação visual do antes e do depois da correção.

Pré-requisito: veja "Pré-requisitos de Automação de Navegador (Playwright e Selenium)", bloco Playwright, no início deste arquivo.

**Prompt:**

```text
Objetivo: investigar o defeito abaixo e apresentar o plano de correção. Depois do meu OK, implementar a correção. Use Playwright para reproduzir o bug e validar a correção visualmente.

Defeito: <descreva o defeito em uma frase>.
Local: <caminho do módulo ou arquivo>.

Fora de escopo: refatorar código adjacente, comitar qualquer ajuste de configuração feito só para habilitar a automação de navegador.

Fatos verificados:
- comportamento atual: <descreva o erro com os valores necessários para reproduzi-lo, ocultando segredos e dados pessoais>
- comportamento esperado: <descreva o correto>
- frequência: <sempre reproduz, intermitente, só em certas condições>
- mensagem de erro: <cole aqui, se existir, com segredo e dado pessoal mascarados>
- print de tela anterior: <anexe o arquivo de imagem, se existir>

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- desde quando ocorre: <sempre ocorreu, ou começou após uma mudança específica, ex.: "não ocorria na versão 5.1 do módulo, passou a ocorrer na 5.2">
- arquivos ou classes suspeitas: <se já tiver uma suspeita, ex.: "deve estar na BD, no método que monta o filtro">
- relato do usuário: <cole aqui o texto que ele reportou, ex.: "a listagem está trazendo processos de fevereiro mesmo eu filtrando só janeiro">

Critério de aceite:
1. Sucesso: <entrada concreta e resultado esperado, verificável na tela>
2. Validação: <condição limite e comportamento esperado>
3. Regressão: <o que já funciona nesse fluxo e precisa continuar funcionando>

Acesso ao ambiente de teste:
- endereço: <URL do ambiente de teste, ex.: http://localhost:8000/sei>
- autenticação: use as credenciais de teste já documentadas no `README.md` (usuário `teste`); se precisar de outro perfil, peça a credencial no momento do uso

Passos:
1. Use a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble` (baixe se ainda não tiver localmente) para abrir a seguinte tela ou fluxo: <tela ou fluxo onde o bug ocorre>. Se a reprodução exigir um estado específico na base (registro, status, permissão), prepare esse estado você mesmo antes de tentar reproduzir o problema.
2. Capture um print do estado com o bug, antes da correção, e salve em <pasta de destino>.
3. Apresente a causa, se confirmada, com evidências (arquivo e linha) e o plano de correção. Se a investigação for inconclusiva, informe o que falta verificar. Aguarde meu OK antes de corrigir.
4. Corrija a causa raiz no local informado acima.
5. Repita a navegação, capture um novo print de cada critério de aceite confirmado e salve os arquivos na mesma pasta.

Referencie os prints de antes e depois como evidência de cada critério de aceite verificado na tela.
```

**Exemplo preenchido, reproduzir o filtro de período com Playwright:**

```text
Objetivo: investigar o defeito abaixo e apresentar o plano de correção. Depois do meu OK, implementar a correção. Use Playwright para reproduzir o bug e validar a correção visualmente.

Defeito: o filtro de período da listagem de indisponibilidades ignora o intervalo e retorna somente os registros com data exatamente igual à informada.
Local: fontes/sei/src/main/php/sei/web/modulos/peticionamento/md_pet_indisponibilidade_lista.php.

Fora de escopo: refatorar código adjacente, comitar qualquer ajuste de configuração feito só para habilitar a automação de navegador.

Fatos verificados:
- comportamento atual: com Início 01/01/2026 00:00 e Fim 31/01/2026 23:59, a listagem volta vazia, mesmo havendo indisponibilidades cadastradas dentro desse intervalo
- comportamento esperado: a listagem deve mostrar todas as indisponibilidades do intervalo informado, respeitando início e fim
- frequência: sempre reproduz quando os dois campos de data são preenchidos

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- desde quando ocorre: sempre ocorreu, ninguém do time lembra do filtro funcionando por intervalo
- arquivos ou classes suspeitas: os campos txtDtInicio e txtDtFim parecem ser aplicados como igualdade no DTO, e não como faixa de datas na BD do módulo
- relato do usuário: "filtrei o mês de janeiro e a tela não trouxe nenhuma indisponibilidade, mas elas aparecem na lista sem filtro"

Critério de aceite:
1. Sucesso: com Início 01/01/2026 00:00 e Fim 31/01/2026 23:59, a listagem mostra as indisponibilidades do intervalo, incluindo a que começa em 01/01/2026 e a que termina em 31/01/2026
2. Validação: com apenas um dos dois campos preenchido, o filtro aplica só o limite informado e não lança erro
3. Regressão: os demais filtros e a ordenação da listagem continuam funcionando isolados e combinados com o filtro de período

Acesso ao ambiente de teste:
- endereço: http://localhost:8000/sei
- autenticação: use as credenciais de teste já documentadas no `README.md` (usuário `teste`); se precisar de outro perfil, peça a credencial no momento do uso

Passos:
1. Use a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble` (baixe se ainda não tiver localmente) para abrir a seguinte tela ou fluxo: Indisponibilidades do SEI, no menu do módulo Peticionamento. Se a reprodução exigir um estado específico na base (registro, status, permissão), prepare esse estado você mesmo antes de tentar reproduzir o problema.
2. Capture um print do estado com o bug, antes da correção, e salve em specs/bug-filtro-indisponibilidade/prints/.
3. Apresente a causa, se confirmada, com evidências (arquivo e linha) e o plano de correção. Se a investigação for inconclusiva, informe o que falta verificar. Aguarde meu OK antes de corrigir.
4. Corrija a causa raiz no local informado acima.
5. Repita a navegação, capture um novo print de cada critério de aceite confirmado e salve os arquivos na mesma pasta.

Referencie os prints de antes e depois como evidência de cada critério de aceite verificado na tela.
```

#### Investigar e corrigir bug com auxílio do Selenium

Use esta variação quando quiser reproduzir e validar o bug via Selenium em vez de Playwright. A lógica é a mesma: reproduzir o bug, corrigir e validar visualmente o antes e o depois.

Pré-requisito: veja "Pré-requisitos de Automação de Navegador (Playwright e Selenium)", bloco Selenium, no início deste arquivo.

**Prompt:**

```text
Objetivo: investigar o defeito abaixo e apresentar o plano de correção. Depois do meu OK, implementar a correção. Use Selenium para reproduzir o bug e validar a correção visualmente.

Defeito: <descreva o defeito em uma frase>.
Local: <caminho do módulo ou arquivo>.

Fora de escopo: refatorar código adjacente, comitar qualquer ajuste de configuração feito só para habilitar a automação de navegador, alterar `test_suiteBasics.py` (crie uma cópia adaptada em vez de editar o script de referência).

Fatos verificados:
- comportamento atual: <descreva o erro com os valores necessários para reproduzi-lo, ocultando segredos e dados pessoais>
- comportamento esperado: <descreva o correto>
- frequência: <sempre reproduz, intermitente, só em certas condições>
- mensagem de erro: <cole aqui, se existir, com segredo e dado pessoal mascarados>
- print de tela anterior: <anexe o arquivo de imagem, se existir>

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- desde quando ocorre: <sempre ocorreu, ou começou após uma mudança específica, ex.: "não ocorria na versão 5.1 do módulo, passou a ocorrer na 5.2">
- arquivos ou classes suspeitas: <se já tiver uma suspeita, ex.: "deve estar na BD, no método que monta o filtro">
- relato do usuário: <cole aqui o texto que ele reportou, ex.: "a listagem está trazendo processos de fevereiro mesmo eu filtrando só janeiro">

Critério de aceite:
1. Sucesso: <entrada concreta e resultado esperado, verificável na tela>
2. Validação: <condição limite e comportamento esperado>
3. Regressão: <o que já funciona nesse fluxo e precisa continuar funcionando>

Acesso ao ambiente de teste:
- endereço: <URL do ambiente de teste, ex.: http://localhost:8000/sei>
- autenticação: use as credenciais de teste já documentadas no `README.md` (usuário `teste`); se precisar de outro perfil, peça a credencial no momento do uso
- driver e navegador: container `selenium/standalone-chrome` já configurado em `fontes/sei/ops_sei-docker/tests/`, com os comandos no `Makefile` dessa mesma pasta

Passos:
1. Copie `fontes/sei/ops_sei-docker/tests/Selenium/PythonExported/test_suiteBasics.py` para um script novo, com nome diferente de `test_suiteBasics-executar.py`, e substitua os marcadores `<<PROTOCOLO>>`, `<<HOST>>` e `<<SENHA>>` pelos valores do ambiente de teste. Adapte-o para reproduzir o bug na seguinte tela ou fluxo: <tela ou fluxo onde o bug ocorre>.
2. Suba o container com o comando `CMDSELENIUMCHROMELOCAL` do `fontes/sei/ops_sei-docker/tests/Makefile` e rode o script novo com o comando `CMDSELENIUMTEST` do mesmo Makefile, trocando o nome do arquivo no `pytest`. Capture um print do estado com o bug, antes da correção, e salve em <pasta de destino>.
3. Apresente a causa, se confirmada, com evidências (arquivo e linha) e o plano de correção. Se a investigação for inconclusiva, informe o que falta verificar. Aguarde meu OK antes de corrigir.
4. Corrija a causa raiz no local informado acima.
5. Repita a navegação, capture um novo print de cada critério de aceite confirmado e salve os arquivos na mesma pasta.

Referencie os prints de antes e depois como evidência de cada critério de aceite verificado na tela.
```

**Exemplo preenchido, reproduzir o filtro de período com Selenium:**

```text
Objetivo: investigar o defeito abaixo e apresentar o plano de correção. Depois do meu OK, implementar a correção. Use Selenium para reproduzir o bug e validar a correção visualmente.

Defeito: o filtro de período da listagem de indisponibilidades ignora o intervalo e retorna somente os registros com data exatamente igual à informada.
Local: fontes/sei/src/main/php/sei/web/modulos/peticionamento/md_pet_indisponibilidade_lista.php.

Fora de escopo: refatorar código adjacente, comitar qualquer ajuste de configuração feito só para habilitar a automação de navegador, alterar `test_suiteBasics.py` (crie uma cópia adaptada em vez de editar o script de referência).

Fatos verificados:
- comportamento atual: com Início 01/01/2026 00:00 e Fim 31/01/2026 23:59, a listagem volta vazia, mesmo havendo indisponibilidades cadastradas dentro desse intervalo
- comportamento esperado: a listagem deve mostrar todas as indisponibilidades do intervalo informado, respeitando início e fim
- frequência: sempre reproduz quando os dois campos de data são preenchidos

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- desde quando ocorre: sempre ocorreu, ninguém do time lembra do filtro funcionando por intervalo
- arquivos ou classes suspeitas: os campos txtDtInicio e txtDtFim parecem ser aplicados como igualdade no DTO, e não como faixa de datas na BD do módulo
- relato do usuário: "filtrei o mês de janeiro e a tela não trouxe nenhuma indisponibilidade, mas elas aparecem na lista sem filtro"

Critério de aceite:
1. Sucesso: com Início 01/01/2026 00:00 e Fim 31/01/2026 23:59, a listagem mostra as indisponibilidades do intervalo, incluindo a que começa em 01/01/2026 e a que termina em 31/01/2026
2. Validação: com apenas um dos dois campos preenchido, o filtro aplica só o limite informado e não lança erro
3. Regressão: os demais filtros e a ordenação da listagem continuam funcionando isolados e combinados com o filtro de período

Acesso ao ambiente de teste:
- endereço: http://localhost:8000/sei
- autenticação: use as credenciais de teste já documentadas no `README.md` (usuário `teste`); se precisar de outro perfil, peça a credencial no momento do uso
- driver e navegador: container `selenium/standalone-chrome` já configurado em `fontes/sei/ops_sei-docker/tests/`, com os comandos no `Makefile` dessa mesma pasta

Passos:
1. Copie `fontes/sei/ops_sei-docker/tests/Selenium/PythonExported/test_suiteBasics.py` para um script novo, com nome diferente de `test_suiteBasics-executar.py`, e substitua os marcadores `<<PROTOCOLO>>`, `<<HOST>>` e `<<SENHA>>` pelos valores do ambiente de teste. Adapte-o para reproduzir o bug na seguinte tela ou fluxo: Indisponibilidades do SEI, no menu do módulo Peticionamento.
2. Suba o container com o comando `CMDSELENIUMCHROMELOCAL` do `fontes/sei/ops_sei-docker/tests/Makefile` e rode o script novo com o comando `CMDSELENIUMTEST` do mesmo Makefile, trocando o nome do arquivo no `pytest`. Capture um print do estado com o bug, antes da correção, e salve em specs/bug-filtro-indisponibilidade/prints/.
3. Apresente a causa, se confirmada, com evidências (arquivo e linha) e o plano de correção. Se a investigação for inconclusiva, informe o que falta verificar. Aguarde meu OK antes de corrigir.
4. Corrija a causa raiz no local informado acima.
5. Repita a navegação, capture um novo print de cada critério de aceite confirmado e salve os arquivos na mesma pasta.

Referencie os prints de antes e depois como evidência de cada critério de aceite verificado na tela.
```

### Fluxo Speckit para Funcionalidade Nova

Use o fluxo Speckit sempre que a demanda criar algo que ainda não existe: nova funcionalidade, nova entidade CRUD completa, novo menu e página, nova operação de API ou WebService, ou release com DDL novo.

Os gates técnicos do SEI (verificação de página, RN, banco de dados, controladores, tarefa e geração de scripts de release) vêm do `AGENTS.md`, seção "Roteamento", e valem em qualquer fase. Se quiser garantir que eles apareçam, peça os gates aplicáveis dentro do `/speckit-plan` e do `/speckit-implement`.

Se você tem a tarefa na cabeça e não sabe como escrever esse pedido, interrogue a ideia com o [grill-me](#interrogar-um-plano-ou-um-pedido-utilizando-o-grill-me) antes de a fase rodar, e peça no fim da entrevista o texto do pedido.

Quanto mais detalhado o pedido em `/speckit-specify`, melhor a especificação gerada. Descreva contexto, comportamento esperado e critério de aceite em linguagem de negócio; deixe stack técnica, classe e padrão de implementação para o `/speckit-plan`, que é a fase certa para essa decisão.

Os exemplos abaixo usam como demanda "uma tela de relatório das demandas institucionais agrupadas por tema, com filtro de período", no módulo `relacionamento-institucional`. Troque pelo objetivo real antes de enviar.

#### Fluxo padrão

Especificar, planejar, decompor em tarefas e implementar, nessa ordem.

**1. Especificar:**

```text
/speckit-specify

Quero <descreva a funcionalidade nova em uma frase>.

Módulo: <nome do módulo>.

Contexto:
- quem usa: <perfil ou permissão>
- comportamento esperado: <resultado esperado>
- fora de escopo: <o que essa funcionalidade não faz>

Critério de aceite inicial:
1. Sucesso: <entrada concreta e resultado esperado>
2. Validação: <condição limite e comportamento esperado>

Fatos verificados:
- regra de negócio confirmada: <se houver, ex.: "só usuários com perfil Administrador podem ver processos sigilosos no filtro">
- tela ou fluxo semelhante que serve de referência: <se houver, ex.: "a listagem de temas já resolve a leitura e a exibição">

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- impacto suposto em permissão, menu ou release: <se souber, ex.: "deve exigir recurso e item de menu novos no SIP, sem mudança de estrutura no banco">
```

**Exemplo preenchido, relatório de demandas por tema:**

```text
/speckit-specify

Quero uma tela de relatório das demandas institucionais agrupadas por tema, com filtro de período.

Módulo: relacionamento-institucional.

Contexto:
- quem usa: usuário com o perfil Administrador, que já acessa os cadastros do módulo
- comportamento esperado: a tela mostra a quantidade de demandas registradas por tema dentro do período informado, com link para abrir cada demanda
- fora de escopo: alterar o cadastro de demandas, criar tema ou subtema novo e exportar o resultado para outro formato

Critério de aceite inicial:
1. Sucesso: com o período de 01/01/2026 a 31/01/2026, a tela lista cada tema com a contagem de demandas registradas no intervalo
2. Validação: com um período sem demanda registrada, a tela informa que não há resultado e não apresenta erro

Fatos verificados:
- regra de negócio confirmada: uma demanda pode ter mais de um tema associado e deve ser contada uma vez em cada tema
- tela ou fluxo semelhante que serve de referência: a listagem de temas em md_ri_classificacao_tema_lista.php já resolve a leitura e a exibição dos temas

Hipóteses: investigue estas pistas no código e informe quais foram confirmadas, refutadas ou permaneceram sem confirmação.
- impacto suposto em permissão, menu ou release: tela nova deve exigir recurso e item de menu novos no SIP, sem mudança de estrutura no banco
```

**2. Planejar:**

```text
/speckit-plan

Use `PaginaSEI::POST/GET` com normalização de tipo nos parâmetros novos. Reaproveite tela, RN ou padrão semelhante já existente no módulo antes de propor algo novo.

Módulo: <nome do módulo>.
Parâmetros novos: <parâmetros da funcionalidade>.

No plano, declare explicitamente: impacto em script de release SEI e SIP, impacto em recurso e perfil SIP, e impacto em estrutura de banco. Se algum desses impactos existir, marque-o como ponto de parada para minha decisão antes da implementação.

Aplique também os gates por artefato do `AGENTS.md`, seção "Roteamento", aos artefatos previstos no plano.
```

**Exemplo preenchido, plano do relatório de demandas por tema:**

```text
/speckit-plan

Use `PaginaSEI::POST/GET` com normalização de tipo nos parâmetros novos. Reaproveite tela, RN ou padrão semelhante já existente no módulo antes de propor algo novo.

Módulo: relacionamento-institucional.
Parâmetros novos: data inicial, data final e identificador de tema do relatório.

No plano, declare explicitamente: impacto em script de release SEI e SIP, impacto em recurso e perfil SIP, e impacto em estrutura de banco. Se algum desses impactos existir, marque-o como ponto de parada para minha decisão antes da implementação.

Aplique também os gates por artefato do `AGENTS.md`, seção "Roteamento", aos artefatos previstos no plano.
```

**3. Decompor em tarefas:** a decomposição usa a spec e o plano já aprovados nas fases anteriores. Não precisa de argumento adicional, então o bloco abaixo já é o texto final para copiar.

```text
/speckit-tasks
```

**4. Implementar:** executa as tarefas geradas. Não precisa de argumento adicional, então o bloco abaixo já é o texto final para copiar.

```text
/speckit-implement
```

#### Fluxo alternativo (com passos opcionais)

Mesmo fluxo, com três passos opcionais inseridos: clarificar dúvidas antes de planejar, gerar um checklist de requisitos sensíveis antes de decompor, e analisar consistência antes de implementar.

**1. Especificar:** igual ao fluxo padrão.

**2. Clarificar:** use quando a spec tiver ambiguidade. A skill faz até 5 perguntas objetivas e grava as respostas na própria spec. Não precisa de argumento adicional, então o bloco abaixo já é o texto final para copiar.

```text
/speckit-clarify
```

**3. Planejar:** igual ao fluxo padrão.

**4. Gerar checklist:** use quando o domínio for sensível, como permissão, auditoria ou modelagem de dados, e você quiser validar a qualidade dos requisitos antes de decompor em tarefas.

```text
/speckit-checklist

Gere um checklist para validar os requisitos de permissão e auditoria antes de implementar.

Funcionalidade: <nome da funcionalidade>.
```

**Exemplo preenchido, checklist de permissão e auditoria:**

```text
/speckit-checklist

Gere um checklist para validar os requisitos de permissão e auditoria antes de implementar.

Funcionalidade: relatório de demandas institucionais por tema.
```

**5. Decompor em tarefas:** igual ao fluxo padrão.

**6. Analisar:** checa a consistência entre spec, plano e tarefas antes de implementar. Não precisa de argumento adicional, então o bloco abaixo já é o texto final para copiar.

```text
/speckit-analyze
```

**7. Implementar:** igual ao fluxo padrão.

### Revisão Técnica (inclui Segurança e Vulnerabilidade)

Use `sei-revisao-tecnica` para conferir os padrões técnicos do SEI em código já implementado: escopo, arquitetura, permissões, transação, controladores, entrada e saída, segurança, banco, release, integrações, qualidade e testes. A skill aciona as verificações de cada artefato encontrado, como página, RN, banco de dados, controladores e tarefa, e o relatório reúne o resultado dessas verificações. Ela não avalia requisito, regra de negócio nem especificação.

#### Revisão Técnica de alterações

Sempre que fizer alterações antes de realizar um merge para branches de ambiente utilize estes exemplos para garantir a qualidade da entrega.

| O que você quer revisar | O que escrever no lugar de `<o que revisar>` |
|---|---|
| Uma branch antes do merge | `da branch <nome da branch>, comparada com <branch ou commit de referência>` |
| Um commit | `do commit <identificador do commit>` |
| Mais de um commit | `dos commits <identificador 1> e <identificador 2>`, etc... |

**Prompt:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** <o que revisar>
```

Se quiser dar contexto ao agente, acrescente as duas linhas abaixo ao final do prompt. Elas são opcionais: apague a que você não tiver como preencher.

```text
Escopo da mudança: <resumo do que foi alterado>
Pontos de atenção conhecidos: <o que você já sabe que merece olhar>
```

As branches e os identificadores dos exemplos existem neste repositório. Troque pelos da sua mudança antes de enviar.

**Exemplo preenchido, avaliar o diff da branch antes do merge:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** da branch origin/pet_v4.6.6, comparada com origin/master
```

**Exemplo preenchido, um commit:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** do commit 8bf4ab729d
```

**Exemplo preenchido, mais de um commit:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** dos commits 29e8ee1308 e 19b852d280
```

**Exemplo preenchido, com o contexto opcional:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** do commit 8bf4ab729d

Escopo da mudança: o cadastro de controle do módulo litigioso passou a exigir dispositivo normativo ou conduta vinculada.
Pontos de atenção conhecidos: a validação entrou na RN e na página de cadastro, e quero saber se ela continua valendo em chamada direta pela URL.
```

#### Revisão Técnica de módulo ou arquivo

Use para levantar o estado atual do código que está no repositório, incluindo o passivo. Em um módulo, a revisão cobre todas as dimensões técnicas e também os scripts SEI e SIP de instalação e atualização mapeados para ele. Fonte: `sei-revisao-tecnica/SKILL.md`, seção "Escopo de modulo completo".

**Prompt para módulo inteiro:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica Completa** do módulo: <nome do módulo>
```

**Prompt para módulo inteiro, exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica Completa** do módulo: Peticionamento
```

**Prompt para arquivo:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica Completa** do arquivo: <caminho do arquivo>
```

**Prompt para arquivo, exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica Completa** do arquivo: fontes/sei/src/main/php/sei/web/modulos/litigioso/rn/MdLitLancamentoRN.php
```

#### Revisão Técnica de Dimensões Específicas

Use quando quiser limitar a revisão a uma ou mais dimensões. A tabela traduz o assunto para o nome exato da dimensão usada pela skill. Escreva o nome como está na coluna da direita. Fonte: `sei-revisao-tecnica/SKILL.md`, seção "Dimensões técnicas".

| Assunto | Dimensão para escrever no prompt |
|---|---|
| Caminhos de escrita permitidos e proteção do núcleo do SEI | `Escopo` |
| Separação de camadas, DTO entre camadas e reaproveitamento técnico | `Arquitetura` |
| Link assinado, permissão por ação, recurso SIP e auditoria na RN | `Permissões` |
| Consistência da gravação e efeitos disparados após o commit, como e-mail e chamada externa | `Transação` |
| Dispatch de Ajax e WebService e autorização por ação ou serviço | `Controladores` |
| Normalização da entrada HTTP, sanitização da saída e encoding | `Entrada/saída` |
| Vulnerabilidade explorável, segredo exposto e dado pessoal | `Segurança` |
| DTO, BD, DDL, consultas SQL, nomes e compatibilidade multi-SGBD | `Banco` |
| Scripts de instalação e atualização, versões, recursos e parâmetros | `Release` |
| API oficial do SEI, eventos, operações e contratos com outros sistemas | `Integrações` |
| Clareza, duplicação, acoplamento, complexidade e desempenho do código | `Qualidade` |
| Lint, checks locais e cobertura técnica do caminho alterado | `Testes` |

**Prompt:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** somente destas **Dimensões**: <dimensões escolhidas>
- Alvo: <caminho do módulo ou arquivo>
```

**Exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** somente destas **Dimensões**: Permissões e Transação
- Alvo: fontes/sei/src/main/php/sei/web/modulos/peticionamento/rn/MdPetIntEmailNotificacaoRN.php
```

**Exemplo preenchido:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** somente destas **Dimensões**: Segurança
- Alvo: fontes/sei/src/main/php/sei/web/modulos/peticionamento/
```

#### Variações de Saída da Revisão Técnica

Peça uma variação quando precisar de um arquivo para compartilhar o resultado ou para alimentar o acompanhamento do time. São duas saídas:

- **PDF**: documento com capa, resumo por severidade, gráficos, tabela de achados e recomendações priorizadas.
- **Texto de issues ou tarefas técnicas**: arquivo Markdown com um texto pronto por achado, para você colar na ferramenta que o time usa. Gerar esse texto não abre issue nem tarefa em lugar nenhum.

Cada trecho abaixo é autossuficiente: cole no final de qualquer prompt de revisão das subseções anteriores, separado por uma linha em branco. Você preenche só o alvo da revisão; o agente cuida de identificadores, datas e nomes de arquivo.

##### Revisão Técnica em PDF

Adicione este trecho ao final do prompt de revisão.

```text
Gere relatório em PDF desta revisão técnica com todos os achados.

Consolide antes os achados em `specs/relatorios/achados-<slug>-<AAAA-MM-DD-HHhMM>.json`, com mesmo carimbo gravado no campo `gerado_em`. Os números do relatório sairão desse arquivo preliminar: gráficos e tabela leem dele e nada é recalculado durante a geração da formatação final do relatório. Cada achado leva `id`, `dimensão`, `categoria`, `subtipo`, `severidade` (`critica`, `alta`, `media` ou `baixa`), `estado` (`CONFIRMED` ou `HYPOTHESIS`), `arquivo`, `linha_inicio`, `linha_fim`, `descricao`, `evidencia`, `impacto`, `sugestao_correcao`, `criterios_aceite`, `acionavel` e `grupo_issue`.
	- `categoria` é o nome da vulnerabilidade na nomenclatura internacional, em inglês, escolhido desta lista fechada: SQL Injection; Cross-Site Scripting (XSS); Broken Access Control; Broken Authentication; Sensitive Data Exposure; Security Misconfiguration; Vulnerable and Outdated Components; Information Disclosure; Unrestricted File Upload; Path Traversal; XML External Entity (XXE); Server-Side Request Forgery (SSRF); Cross-Site Request Forgery (CSRF); Command Injection; HTML Injection (Email); Insecure Deserialization; Open Redirect; Weak Cryptography; Insufficient Logging and Monitoring; Business Logic Flaw. Não invente categoria fora da lista; se nenhuma couber, use a mais próxima e explique no `subtipo`.
	- `subtipo` é a forma específica encontrada no código, em português (por exemplo: "comando de escrita sem parâmetro vinculado, exploração por consulta empilhada ou cega"; "consulta de leitura com resultado na tela"; "refletido em atributo HTML"; "armazenado"; "IDOR: identificador do registro vindo do cliente sem conferir o dono"; "credencial na URL").
	- O JSON traz também a lista `categorias`, com quantidade por categoria e por subtipo e os ids de cada um, que alimenta a tabela e o gráfico por categoria.
	- Mascare segredo real na evidência; nunca reproduza um segredo válido em texto claro. Mascare também login de pessoa física, CPF, e-mail pessoal e nome de servidor de banco. Achado que é hipótese continua marcado como hipótese.

Salve o PDF em `specs/relatorios/relatorio-<slug>-<AAAA-MM-DD-HHhMM>.pdf`, reaproveitando o carimbo do JSON. Conteúdo:
	- **Capa** com:
		- Título: **Revisão Técnica <"Completa"/escopo/"por Dimensões Específicas"> - <alvo da revisão técnica>**
		- Subtítulo em itálico: "Relatório de Revisão Estática e de Conformidade Técnica"
		- Tabela com cabeçalho na primeira coluna, com as seguintes linhas:
			- "Data da Execução": a data e hora da execução da revisão técnica em BRT;
			- "Alvo da Revisão Técnica": <alvo da revisão técnica> igual ao do título - **<se aplicável, Versão do alvo no formato vN.N.N>** (QUANDO módulo, consta na raiz da pasta do módulo em `*Integracao.php` > getVersao; QUANDO SEI, consta em SEI.php > SEI_VERSAO; QUANDO SIP; está em Sip.php > SIP_VERSAO);
			- "Commit de Referência": identificação do commit de referência conforme o alvo;
			- "Resultado Global": da revisão técnica executada como um todo.
		- "### Dimensões da Revisão Técnica": tabela com as colunas "Dimensão" transcrevendo o nome de cada dimensão abrangida pela revisão técnica executada; "Estado"; e "Cobertura" da dimensão.
		- "### Escopo da Revisão Técnica": informando a lista do que está "Incluído":`#059669` e a lista do que está "Excluído":`#B91C1C` do escopo da revisão técnica, em termos de pastas, arquivos, camadas, situações do ambiente computacional e outras circunstâncias do código, da execução ou do ambiente que contextualiza sobre o que e como foi executada a revisão técnica.
		- "### Nota Metodológica".
		- "### Como ler este relatório": tabela com as colunas "Termo" e "Significado", explicando em linguagem simples cada código usado no relatório: o identificador do achado; categoria e subtipo; os vetores da matriz de vulnerabilidades do SEI (V01 a V10); CWE; OWASP Top 10; os níveis de severidade; os estados do achado (CONFIRMED e HYPOTHESIS); as prioridades (P1, P2, P3, P4...); os estados de verificação (PASS, WARN, BLOCK, NOT_EXECUTED, NOT_APPLICABLE); e as técnicas de exploração citadas (por exemplo, consulta empilhada e injeção cega).
	- "## Resumo Executivo", com um texto de introdução no estilo de resumo geral da execução/achados; tabela centralizada com as colunas "Severidade" (com nome sobre chip colorido) e "Quantidade" com total de achados por Severidade, e última linha de total geral na mesma tabela com "Total" na coluna "Severidade" em negrito e alinhado à direita na célula e o número do total geral na célula da coluna "Quantidade".
		- "### Achados por Categoria de Vulnerabilidade": tabela com as colunas "Categoria" (nome em inglês, em negrito, uma vez por categoria); "Subtipo"; "Qtde."; e "Achados" (ids), com linha de total por categoria quando houver mais de um subtipo e linha de total geral ao fim, ordenada da categoria com mais achados para a com menos.
		- "### Distribuição Visual", com gráfico de rosca por Severidade, gráfico de barras por categoria de vulnerabilidade e gráfico de barras por dimensão, os dois últimos empilhados por Severidade com a paleta abaixo e com o total ao fim de cada barra.
		- "### Status de Verificação": tabela com as colunas "Gate"; "Estado"; e "Evidência".
	- "## Pontos Fortes": o que está protegido, com evidência - título curto de cada ponto forte na cor `#059669`.
	- "## Pontos Fracos": riscos centrais priorizados, com evidência - título curto de cada ponto fraco na cor `#B91C1C`.
	- "## Tabela de Achados", tabela ordenada por Severidade **dentro de cada dimensão**. Colunas: "ID", "Severidade" (com nome sobre chip colorido), "Categoria" (nome em inglês em negrito e, abaixo, o subtipo em português), "Arquivo:Linha-Linha" e "Descrição" (descrição curta; achado em hipótese recebe o prefixo `[HYPOTHESIS]`).
	- "## Recomendação de Ordem de Priorização": justificar as prioridades P1, em seguida apresentar tabela com as colunas: "Prioridade" (P1, P2, P3, P4...); "ID do Achado"; "Severidade" (com nome sobre chip colorido); "Categoria" (nome em inglês e subtipo); e "Ação Necessária";
	- "## Issues dos Achados": seguindo a ordem constante em "Recomendação de Ordem de Priorização", criar **para cada achado acionável** uma subseção com número da Issue e Título, seguida da linha "Achados cobertos" com o id e a categoria de cada achado.
		- Incluir o texto COMPLETO da Issue em Markdown dentro de um bloco delimitado pronto para copiar e colar (ex: entre --- ISSUE n --- e --- FIM ISSUE n ---). Cada Issue deve conter:
			- Título no formato "# [<categoria da vulnerabilidade em inglês>] <descrição curta do problema>";
			- "**Labels sugeridas:**": com lista de tags para indexar a issue;
			- "Problema": com descrição de cada achado coberto, precedida do id, do arquivo:linha-linha, da severidade, do estado e da categoria com subtipo;
			- "## Por que é explorável" se o achado envolver segurança/vulnerabilidade ou "## Por que é um problema" nos demais casos;
			- "## Evidência": informando **cada** arquivo:linha-linha e dentro de snippet o trecho de código correspondente ao problema, seguido do caminho do dado (da entrada até o ponto de uso, com arquivo:linha em cada salto) e das ocorrências adicionais;
			- "## Impacto";
			- "## Sugestão de Correção";
			- "## Critérios de Aceite" com checklist verificável.
		- Quando fizer sentido, agrupe achados **triviais** ou relacionados com a mesma causa numa Issue única.
	- **Atenção**:
		- Em todos os pontos do relatório QUANDO tratar de "Estado", ENTÃO escrever o texto no estilo de variável em inglês, em MAIÚSCULO e nunca use chip colorido nisso.
		- Em todos os pontos do relatório QUANDO tratar de "Severidade", ENTÃO utilizar apenas esses níveis e paleta de cor do chip colorido correspondente: "CRÍTICA":`#B91C1C`; "ALTA":`#EA580C`; "MÉDIA":`#D97706`; e "BAIXA":`#2563EB`.
		- Em todos os pontos do relatório QUANDO tratar de "Categoria", ENTÃO usar o nome em inglês da lista fechada acima, sempre acompanhado do subtipo em português onde houver espaço.
		- Em todo texto corrido (descrição, explorabilidade, impacto, sugestão, critérios, notas), na primeira menção de cada vetor da matriz de vulnerabilidades (V01 a V10) e de cada CWE, escreva o nome por extenso ao lado, entre parênteses. Um leitor sem familiaridade com os códigos precisa entender o achado sem consultar outra fonte.
		- Não inclua achados sobre a stack de agentes de IA (arquivos de configuração e skills dos agentes): ela não roda na aplicação. Registre a inspeção no "Status de Verificação" e no escopo excluído.
		- Não cite identificadores intermediários de trabalho (numeração provisória de agentes ou de rodadas) nem notas de bastidor entre agentes; o relatório usa somente os ids finais.

Use ambiente isolado, sem instalar nada globalmente: venv Python com reportlab e matplotlib. Deixe o script gerador em `specs/relatorios/gerar_relatorio-<slug>-<AAAA-MM-DD-HHhMM>.py`, recebendo o JSON como entrada, para permitir regenerar apenas o PDF sem repetir a revisão. Se o script já existir, reutilize em vez de reescrever. Página A4, margens de 2 cm, cabeçalho e rodapé com nome do relatório à esquerda e número da página à direita.

Antes de entregar, confirme que a contagem do JSON bate com os gráficos e com as tabelas (por severidade, por categoria, por dimensão, linhas da Tabela de Achados, linhas da priorização e blocos de issue). Antes de entregar, renderize temporariamente cada página do PDF como imagem para inspeção visual, sem rasterizar o PDF final. Confira se há texto cortado, tabelas que ultrapassam a largura da página, títulos separados de seus gráficos ou legendas ilegíveis, cabeçalho de grupo órfão no fim da página e página quase vazia sem motivo.
	- Garanta que nenhum segredo aparece em texto claro em nenhuma página. Corrija qualquer defeito antes de entregar.
	- NÃO cite o arquivo JSON em nenhuma parte do relatório.

Quando o conteúdo estiver preparado, antes de finalizar, execute uma revisão e pelo menos uma verificação independente de **correção gramatical e ortográfica em Português brasileiro** seguindo as 'Regras de Escrita' do AGENTS.md. Os nomes de categoria em inglês, os identificadores de código e os trechos de programa ficam fora da revisão gramatical.

É muito relevante para mim o batimento dos números computados dos achados com o constante no PDF; a estética do PDF; correção gramatical e ortográfica; e que na dimensão de Segurança tenha maior verificação que o problema é de fato explorável.
- Assim, dispare times de agentes de execução e de verificação correspondente sobre cada ponto relevante para mim, com um agente orquestrador e um agente final consolidador e verificador do todo antes da entrega final ao orquestrador.
	- Utilize no máximo três turnos de execução-verificação do que é relevante em qualquer parte da execução desta demanda.

Estude bem duas vezes o Dicionário de Dados correspondente para compreender bem o negócio, localizado nesse caminho: docs\dicionario_dados\<slug>\dicionario_colunas.md

FAÇA APENAS o solicitado; nada mais.

Entregue o relatório em PDF, a lista de achados no chat (uma tabela com id, severidade, estado, prioridade, categoria em inglês, **cada** arquivo:linha-linha e o número da issue que o cobre) e o caminho de todos os arquivos gerados.
```

**Exemplo preenchido, revisão de módulo com o trecho do PDF já colado:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica Completa** do módulo: ABC

Gere relatório em PDF desta revisão técnica com todos os achados.

Consolide antes os achados em `specs/relatorios/achados-<slug>-<AAAA-MM-DD-HHhMM>.json`, com mesmo carimbo gravado no campo `gerado_em`. Os números do relatório sairão desse arquivo preliminar: gráficos e tabela leem dele e nada é recalculado durante a geração da formatação final do relatório. Cada achado leva `id`, `dimensão`, `categoria`, `subtipo`, `severidade` (`critica`, `alta`, `media` ou `baixa`), `estado` (`CONFIRMED` ou `HYPOTHESIS`), `arquivo`, `linha_inicio`, `linha_fim`, `descricao`, `evidencia`, `impacto`, `sugestao_correcao`, `criterios_aceite`, `acionavel` e `grupo_issue`.
	- `categoria` é o nome da vulnerabilidade na nomenclatura internacional, em inglês, escolhido desta lista fechada: SQL Injection; Cross-Site Scripting (XSS); Broken Access Control; Broken Authentication; Sensitive Data Exposure; Security Misconfiguration; Vulnerable and Outdated Components; Information Disclosure; Unrestricted File Upload; Path Traversal; XML External Entity (XXE); Server-Side Request Forgery (SSRF); Cross-Site Request Forgery (CSRF); Command Injection; HTML Injection (Email); Insecure Deserialization; Open Redirect; Weak Cryptography; Insufficient Logging and Monitoring; Business Logic Flaw. Não invente categoria fora da lista; se nenhuma couber, use a mais próxima e explique no `subtipo`.
	- `subtipo` é a forma específica encontrada no código, em português (por exemplo: "comando de escrita sem parâmetro vinculado, exploração por consulta empilhada ou cega"; "consulta de leitura com resultado na tela"; "refletido em atributo HTML"; "armazenado"; "IDOR: identificador do registro vindo do cliente sem conferir o dono"; "credencial na URL").
	- O JSON traz também a lista `categorias`, com quantidade por categoria e por subtipo e os ids de cada um, que alimenta a tabela e o gráfico por categoria.
	- Mascare segredo real na evidência; nunca reproduza um segredo válido em texto claro. Mascare também login de pessoa física, CPF, e-mail pessoal e nome de servidor de banco. Achado que é hipótese continua marcado como hipótese.

Salve o PDF em `specs/relatorios/relatorio-<slug>-<AAAA-MM-DD-HHhMM>.pdf`, reaproveitando o carimbo do JSON. Conteúdo:
	- **Capa** com:
		- Título: **Revisão Técnica <"Completa"/escopo/"por Dimensões Específicas"> - <alvo da revisão técnica>**
		- Subtítulo em itálico: "Relatório de Revisão Estática e de Conformidade Técnica"
		- Tabela com cabeçalho na primeira coluna, com as seguintes linhas:
			- "Data da Execução": a data e hora da execução da revisão técnica em BRT;
			- "Alvo da Revisão Técnica": <alvo da revisão técnica> igual ao do título - **<se aplicável, Versão do alvo no formato vN.N.N>** (QUANDO módulo, consta na raiz da pasta do módulo em `*Integracao.php` > getVersao; QUANDO SEI, consta em SEI.php > SEI_VERSAO; QUANDO SIP; está em Sip.php > SIP_VERSAO);
			- "Commit de Referência": identificação do commit de referência conforme o alvo;
			- "Resultado Global": da revisão técnica executada como um todo.
		- "### Dimensões da Revisão Técnica": tabela com as colunas "Dimensão" transcrevendo o nome de cada dimensão abrangida pela revisão técnica executada; "Estado"; e "Cobertura" da dimensão.
		- "### Escopo da Revisão Técnica": informando a lista do que está "Incluído":`#059669` e a lista do que está "Excluído":`#B91C1C` do escopo da revisão técnica, em termos de pastas, arquivos, camadas, situações do ambiente computacional e outras circunstâncias do código, da execução ou do ambiente que contextualiza sobre o que e como foi executada a revisão técnica.
		- "### Nota Metodológica".
		- "### Como ler este relatório": tabela com as colunas "Termo" e "Significado", explicando em linguagem simples cada código usado no relatório: o identificador do achado; categoria e subtipo; os vetores da matriz de vulnerabilidades do SEI (V01 a V10); CWE; OWASP Top 10; os níveis de severidade; os estados do achado (CONFIRMED e HYPOTHESIS); as prioridades (P1, P2, P3, P4...); os estados de verificação (PASS, WARN, BLOCK, NOT_EXECUTED, NOT_APPLICABLE); e as técnicas de exploração citadas (por exemplo, consulta empilhada e injeção cega).
	- "## Resumo Executivo", com um texto de introdução no estilo de resumo geral da execução/achados; tabela centralizada com as colunas "Severidade" (com nome sobre chip colorido) e "Quantidade" com total de achados por Severidade, e última linha de total geral na mesma tabela com "Total" na coluna "Severidade" em negrito e alinhado à direita na célula e o número do total geral na célula da coluna "Quantidade".
		- "### Achados por Categoria de Vulnerabilidade": tabela com as colunas "Categoria" (nome em inglês, em negrito, uma vez por categoria); "Subtipo"; "Qtde."; e "Achados" (ids), com linha de total por categoria quando houver mais de um subtipo e linha de total geral ao fim, ordenada da categoria com mais achados para a com menos.
		- "### Distribuição Visual", com gráfico de rosca por Severidade, gráfico de barras por categoria de vulnerabilidade e gráfico de barras por dimensão, os dois últimos empilhados por Severidade com a paleta abaixo e com o total ao fim de cada barra.
		- "### Status de Verificação": tabela com as colunas "Gate"; "Estado"; e "Evidência".
	- "## Pontos Fortes": o que está protegido, com evidência - título curto de cada ponto forte na cor `#059669`.
	- "## Pontos Fracos": riscos centrais priorizados, com evidência - título curto de cada ponto fraco na cor `#B91C1C`.
	- "## Tabela de Achados", tabela ordenada por Severidade **dentro de cada dimensão**. Colunas: "ID", "Severidade" (com nome sobre chip colorido), "Categoria" (nome em inglês em negrito e, abaixo, o subtipo em português), "Arquivo:Linha-Linha" e "Descrição" (descrição curta; achado em hipótese recebe o prefixo `[HYPOTHESIS]`).
	- "## Recomendação de Ordem de Priorização": justificar as prioridades P1, em seguida apresentar tabela com as colunas: "Prioridade" (P1, P2, P3, P4...); "ID do Achado"; "Severidade" (com nome sobre chip colorido); "Categoria" (nome em inglês e subtipo); e "Ação Necessária";
	- "## Issues dos Achados": seguindo a ordem constante em "Recomendação de Ordem de Priorização", criar **para cada achado acionável** uma subseção com número da Issue e Título, seguida da linha "Achados cobertos" com o id e a categoria de cada achado.
		- Incluir o texto COMPLETO da Issue em Markdown dentro de um bloco delimitado pronto para copiar e colar (ex: entre --- ISSUE n --- e --- FIM ISSUE n ---). Cada Issue deve conter:
			- Título no formato "# [<categoria da vulnerabilidade em inglês>] <descrição curta do problema>";
			- "**Labels sugeridas:**": com lista de tags para indexar a issue;
			- "Problema": com descrição de cada achado coberto, precedida do id, do arquivo:linha-linha, da severidade, do estado e da categoria com subtipo;
			- "## Por que é explorável" se o achado envolver segurança/vulnerabilidade ou "## Por que é um problema" nos demais casos;
			- "## Evidência": informando **cada** arquivo:linha-linha e dentro de snippet o trecho de código correspondente ao problema, seguido do caminho do dado (da entrada até o ponto de uso, com arquivo:linha em cada salto) e das ocorrências adicionais;
			- "## Impacto";
			- "## Sugestão de Correção";
			- "## Critérios de Aceite" com checklist verificável.
		- Quando fizer sentido, agrupe achados **triviais** ou relacionados com a mesma causa numa Issue única.
	- **Atenção**:
		- Em todos os pontos do relatório QUANDO tratar de "Estado", ENTÃO escrever o texto no estilo de variável em inglês, em MAIÚSCULO e nunca use chip colorido nisso.
		- Em todos os pontos do relatório QUANDO tratar de "Severidade", ENTÃO utilizar apenas esses níveis e paleta de cor do chip colorido correspondente: "CRÍTICA":`#B91C1C`; "ALTA":`#EA580C`; "MÉDIA":`#D97706`; e "BAIXA":`#2563EB`.
		- Em todos os pontos do relatório QUANDO tratar de "Categoria", ENTÃO usar o nome em inglês da lista fechada acima, sempre acompanhado do subtipo em português onde houver espaço.
		- Em todo texto corrido (descrição, explorabilidade, impacto, sugestão, critérios, notas), na primeira menção de cada vetor da matriz de vulnerabilidades (V01 a V10) e de cada CWE, escreva o nome por extenso ao lado, entre parênteses. Um leitor sem familiaridade com os códigos precisa entender o achado sem consultar outra fonte.
		- Não inclua achados sobre a stack de agentes de IA (arquivos de configuração e skills dos agentes): ela não roda na aplicação. Registre a inspeção no "Status de Verificação" e no escopo excluído.
		- Não cite identificadores intermediários de trabalho (numeração provisória de agentes ou de rodadas) nem notas de bastidor entre agentes; o relatório usa somente os ids finais.

Use ambiente isolado, sem instalar nada globalmente: venv Python com reportlab e matplotlib. Deixe o script gerador em `specs/relatorios/gerar_relatorio-<slug>-<AAAA-MM-DD-HHhMM>.py`, recebendo o JSON como entrada, para permitir regenerar apenas o PDF sem repetir a revisão. Se o script já existir, reutilize em vez de reescrever. Página A4, margens de 2 cm, cabeçalho e rodapé com nome do relatório à esquerda e número da página à direita.

Antes de entregar, confirme que a contagem do JSON bate com os gráficos e com as tabelas (por severidade, por categoria, por dimensão, linhas da Tabela de Achados, linhas da priorização e blocos de issue). Antes de entregar, renderize temporariamente cada página do PDF como imagem para inspeção visual, sem rasterizar o PDF final. Confira se há texto cortado, tabelas que ultrapassam a largura da página, títulos separados de seus gráficos ou legendas ilegíveis, cabeçalho de grupo órfão no fim da página e página quase vazia sem motivo.
	- Garanta que nenhum segredo aparece em texto claro em nenhuma página. Corrija qualquer defeito antes de entregar.
	- NÃO cite o arquivo JSON em nenhuma parte do relatório.

Quando o conteúdo estiver preparado, antes de finalizar, execute uma revisão e pelo menos uma verificação independente de **correção gramatical e ortográfica em Português brasileiro** seguindo as 'Regras de Escrita' do AGENTS.md. Os nomes de categoria em inglês, os identificadores de código e os trechos de programa ficam fora da revisão gramatical.

É muito relevante para mim o batimento dos números computados dos achados com o constante no PDF; a estética do PDF; correção gramatical e ortográfica; e que na dimensão de Segurança tenha maior verificação que o problema é de fato explorável.
- Assim, dispare times de agentes de execução e de verificação correspondente sobre cada ponto relevante para mim, com um agente orquestrador e um agente final consolidador e verificador do todo antes da entrega final ao orquestrador.
	- Utilize no máximo três turnos de execução-verificação do que é relevante em qualquer parte da execução desta demanda.

Estude bem duas vezes o Dicionário de Dados correspondente para compreender bem o negócio, localizado nesse caminho: docs\dicionario_dados\<slug>\dicionario_colunas.md

FAÇA APENAS o solicitado; nada mais.

Entregue o relatório em PDF, a lista de achados no chat (uma tabela com id, severidade, estado, prioridade, categoria em inglês, **cada** arquivo:linha-linha e o número da issue que o cobre) e o caminho de todos os arquivos gerados.
```

##### Gerar as issues ou tarefas técnicas

Adicione este trecho ao final do prompt de revisão.

```text
Gere também o texto completo das issues desta revisão, prontas para copiar e colar. Não crie issue, tarefa ou PR em ferramenta nenhuma: apenas gere o conteúdo em Markdown.

Consolide antes os achados em `specs/relatorios/achados-<slug>-<AAAA-MM-DD-HHhMM>.json`, se ainda não existir, com `id`, `dimensão`, `categoria`, `subtipo`, `severidade` (`critica`, `alta`, `media` ou `baixa`), `estado` (`CONFIRMED` ou `HYPOTHESIS`), `arquivo`, `linha_inicio`, `linha_fim`, `descricao`, `evidencia`, `impacto`, `sugestao_correcao`, `criterios_aceite`, `acionavel` e `grupo_issue`. `categoria` é o nome da vulnerabilidade em inglês, escolhido desta lista fechada: SQL Injection; Cross-Site Scripting (XSS); Broken Access Control; Broken Authentication; Sensitive Data Exposure; Security Misconfiguration; Vulnerable and Outdated Components; Information Disclosure; Unrestricted File Upload; Path Traversal; XML External Entity (XXE); Server-Side Request Forgery (SSRF); Cross-Site Request Forgery (CSRF); Command Injection; HTML Injection (Email); Insecure Deserialization; Open Redirect; Weak Cryptography; Insufficient Logging and Monitoring; Business Logic Flaw; se nenhuma couber, use a mais próxima e explique no `subtipo`. `subtipo` é a forma específica encontrada no código, em português. Mascare segredo real na evidência.

Salve o resultado em `specs/relatorios/issues-<slug>-<AAAA-MM-DD-HHhMM>.md`, reaproveitando o carimbo do JSON. Para cada achado com `acionavel` verdadeiro, gere o texto de uma issue delimitado por `--- ISSUE <id> ---` e `--- FIM ISSUE <id> ---`, contendo:

- Título no formato `[<categoria da vulnerabilidade em inglês>] descrição curta do problema`.
- Labels sugeridas: a categoria e a severidade.
- O ID do achado, para rastreabilidade.
- Descrição do problema e por que ele importa.
- Evidência: arquivo:linha com o trecho de código, com segredo mascarado.
- Impacto.
- Sugestão de correção.
- Critérios de aceite, como checklist verificável.

Agrupe em uma única issue os achados correlatos que compartilhem o mesmo `grupo_issue`, para não gerar spam de issues, preservando todos os IDs e a severidade de cada um. Achado sem grupo vira issue própria.

Antes de entregar, confirme que toda issue referencia um ID válido, que nenhum segredo aparece em texto claro e que os achados do mesmo grupo viraram uma issue só, e não uma por achado.

Entregue o arquivo, a lista de issues no chat com quantas são e quais achados cada uma cobre, e o caminho do arquivo gerado.
```

Nos dois exemplos abaixo o trecho aparece abreviado, para não repetir o texto inteiro. Na hora de enviar, cole o trecho completo no lugar da linha entre `<` e `>`.

**Exemplo preenchido, revisão de commit com o bloco das tarefas técnicas:**

```text
Use a skill `sei-revisao-tecnica` para fazer **Revisão Técnica** do commit 8bf4ab729d

<cole aqui o trecho das issues, sem alterar nada>
```

**Exemplo preenchido, revisão de segurança com o bloco das tarefas técnicas:**

```text
Use a skill `owasp-playbook` para revisar a **Segurança** do módulo: Peticionamento

<cole aqui o trecho das issues, sem alterar nada>
```

##### Para uma revisão já entregue

Use na mesma conversa em que recebeu a revisão, quando decidir pelo arquivo só depois de ler o relatório. Troque `o PDF` por `o texto das issues` quando quiser a outra saída. O bloco abaixo não tem campo para preencher.

```text
Gere o PDF do relatório de revisão que você acabou de entregar, nos caminhos e no formato do trecho do PDF acima. Os números vêm do relatório que você entregou: não refaça a análise nem recalcule contagem, severidade ou resultado.
```
#### Depois da revisão: marcar ou planejar a correção

Os dois prompts abaixo são continuação da mesma conversa, logo depois que o agente entregou o relatório de uma das revisões desta seção. Não cole nem repita os achados: o agente já tem o relatório na conversa. Escolha um dos dois caminhos; nenhum dos dois corrige nada sozinho.

**Marcar TODO: a partir de um relatório de revisão**

Use quando quiser só registrar a dívida no código, sem planejar a correção agora. O bloco abaixo não tem campo para preencher, então já é o texto final para copiar.

```text
No relatório que você acabou de me entregar, pegue os achados WARN e o passivo preexistente e registre cada um em um comentário no código, junto ao local do achado, neste formato:

// TODO: <descrição objetiva em uma linha>

Aplique achado por achado, com minha confirmação antes de cada um. Nunca marque achados classificados como BLOCK; eles exigem correção, não marcação.

Não corrija a causa de nenhum achado nesta etapa, só marque.
```

**Transformar achados em especificação e tarefas**

Use quando tiver vários achados para coordenar e quiser uma lista de tarefas rastreável, para corrigir depois (em outra sessão, ou por outra pessoa) ou agora mesmo.

```text
Transforme em uma especificação de correção e uma lista de tarefas os achados do relatório que você acabou de me entregar.

Alvo do relatório: <caminho do módulo ou arquivo>.

Para cada achado, gere uma tarefa com: título objetivo, arquivo e linha, ação mínima, critério de aceite (o gate ou controle volta a passar) e dependência entre tarefas, se houver. Ordene as tarefas da maior para a menor prioridade (BLOCK primeiro, depois WARN).

Salve a especificação e a lista de tarefas em um arquivo Markdown (`.md`) na pasta `specs/`, que é local e não versionada.

Pare aqui. Se eu pedir para implementar agora, use o prompt "Investigar e corrigir bug" deste arquivo para cada tarefa, achado por achado, com minha confirmação antes de cada um.
```

**Exemplo preenchido, achados de um módulo:**

```text
Transforme em uma especificação de correção e uma lista de tarefas os achados do relatório que você acabou de me entregar.

Alvo do relatório: fontes/sei/src/main/php/sei/web/modulos/peticionamento/.

Para cada achado, gere uma tarefa com: título objetivo, arquivo e linha, ação mínima, critério de aceite (o gate ou controle volta a passar) e dependência entre tarefas, se houver. Ordene as tarefas da maior para a menor prioridade (BLOCK primeiro, depois WARN).

Salve a especificação e a lista de tarefas em um arquivo Markdown (`.md`) na pasta `specs/`, que é local e não versionada.

Pare aqui. Se eu pedir para implementar agora, use o prompt "Investigar e corrigir bug" deste arquivo para cada tarefa, achado por achado, com minha confirmação antes de cada um.
```

### Dicionário de Dados

A skill `dicionario-dados-db-scan-codebase-docs` investiga a codebase, os scripts de banco e qualquer documentação ou material complementar disponível para gerar e manter dicionários de dados. Ela nasceu de um [documento conceitual](../../.agents/skills/dicionario-dados-db-scan-codebase-docs/references/conceitos-e-instrucoes-tecnicas_descricao_tabelas_colunas.md) apoiado na família de normas ISO/IEC de qualidade de dados e metadados (ISO 8000-1, ISO/IEC 25012/25024 e ISO/IEC 11179). O alvo pode ser o sistema, um módulo, uma base de dados corporativa ou DW. Todo alvo reconhecido precisa de um adaptador registrado.

O adaptador é o arquivo que ensina a skill a localizar, investigar e versionar esse alvo: onde fica a fonte estrutural, qual fonte tem precedência quando houver mais de uma, como a versão é identificada e onde buscar no código. Ele fica em `adapters/<família>/<caminho-do-adaptador>.md`, listado em `registro-adaptadores.md`, ambos na raiz da skill. Use o prompt "Criar o adaptador" a seguir para criar e registrar o adaptador. Sem ele registrado, a skill se recusa a gerar o dicionário e aponta a lacuna.

A skill gera três artefatos de saída: `dicionario_tabelas.md` e `dicionario_colunas.md`, com as descrições semânticas, e `CHANGELOG.md`, com o changelog estrutural.

#### Criar o adaptador

Use este prompt no primeiro contato com um alvo que a skill ainda não reconhece, seja o sistema, um módulo ou uma base de dados corporativa. Ele cria só o adaptador. Gere o dicionário depois, em um pedido separado, com o prompt "Criar o dicionário de dados" a seguir. Informe as convenções que você já souber, para reduzir as perguntas que a skill vai precisar fazer. O que você não souber, ela tenta inferir da codebase antes de perguntar.

Para um módulo comum do SEI ou do SIP, a skill pode concluir que o adaptador padrão já cobre o alvo e apenas registrar o módulo, em vez de criar um arquivo novo. Isso não é falha do pedido.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador do alvo abaixo. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.
- Alvo: <nome do sistema ou do módulo>

O que eu já sei sobre ele:
- pistas que identificam este sistema ou módulo (nome, caminhos, prefixo de tabela, pasta de documentação, ou a própria codebase, se for o sistema inteiro): <se souber, ex.: "prefixo pedidos_, models em app/Models/Pedido.php, migrations em database/migrations/">
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber, ex.: "migrations em migrations/Version20240115120000.php">
- precedência entre fontes, se houver mais de uma fonte estrutural para a mesma informação: <qual prevalece, se souber, ex.: "migration mais recente prevalece sobre o schema.sql legado">
- codificação, camadas e onde buscar no código: <se souber, ex.: "camadas Entity/Repository/Controller">
- títulos e pasta de destino dos dicionários: <se souber, ex.: "docs/dicionario_dados/correios/">
- particularidades ou exceções conhecidas: <se houver, ex.: "módulo tem tabela compartilhada com outro módulo, não duplicar no dicionário">

Confira no código cada item que informei acima e me avise se encontrar divergência.

Pergunte objetivamente só sobre o que não puder ser inferido nem tiver sido informado acima.
```

**Exemplo preenchido, adaptador de um módulo do SEI:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador do alvo abaixo. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.
- Alvo: relacionamento-institucional

O que eu já sei sobre ele:
- pistas que identificam este sistema ou módulo: prefixo md_ri_, código em fontes/sei/src/main/php/sei/web/modulos/relacionamento-institucional/, com DTO em dto/ e repositório em bd/
- fonte estrutural e convenção de versionamento: scripts em fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_relacionamento_institucional.php e fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_relacionamento_institucional.php
- precedência entre fontes: a versão retornada por RelacionamentoInstitucionalIntegracao::getVersao() prevalece como versão-alvo
- codificação, camadas e onde buscar no código: PHP em ISO-8859-1, camadas dto/, rn/, bd/ e int/, com as páginas na raiz do módulo
- títulos e pasta de destino dos dicionários: docs/dicionario_dados/relacionamento-institucional/
- particularidades ou exceções conhecidas: o script SIP traz recursos e menus, e o script SEI concentra a estrutura de tabelas

Confira no código cada item que informei acima e me avise se encontrar divergência.

Pergunte objetivamente só sobre o que não puder ser inferido nem tiver sido informado acima.
```

#### Criar o dicionário de dados

Use este prompt na primeira vez que for gerar o dicionário de um sistema ou módulo, depois que ele já tiver um adaptador (crie primeiro com "Criar o adaptador", se ainda não existir). Anexar material complementar aumenta o contexto negocial disponível para a skill e tende a melhorar a qualidade do resultado. Pode ser qualquer formato: esquema de banco em outra ferramenta, dicionário anterior, prints de tela, manuais, vídeos ou transcrições. Cite os materiais que tiver e, se houver mais de um, indique qual é o material prioritário. A skill sempre confere as informações com base nas fontes estruturais disponíveis (codebase, esquema de banco ou DDL) antes de publicar qualquer descrição, com ou sem material complementar.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural do alvo abaixo.
- Alvo: <nome do sistema ou do módulo>

Investigue as fontes estruturais disponíveis (codebase, scripts de instalação, migrations, schemas ou DDLs) para identificar a convenção de versionamento e, quando houver codebase, onde ficam as regras de negócio. Aproveite também qualquer documentação já existente. Só publique uma descrição quando as evidências encontradas sustentarem a semântica dela; sem essa sustentação, marque a descrição como não confirmada.

Materiais complementares: <arquivos anexados, esquema em outro formato, dicionário anterior, capturas de tela, manuais, vídeos ou transcrições, se houver>.
Material prioritário: <arquivo ou material ao qual dar mais atenção, opcional>.

Confira as informações dos materiais com base na fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, informe explicitamente: 1) as tabelas ou colunas cuja semântica você não conseguiu confirmar nas fontes disponíveis; 2) o que faltou para confirmá-las; 3) os pontos em que algum material complementar divergiu da fonte estrutural, com a fonte que você adotou.
```

**Exemplo preenchido, primeiro dicionário de um módulo:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural do alvo abaixo.
- Alvo: relacionamento-institucional

Investigue as fontes estruturais disponíveis (codebase, scripts de instalação, migrations, schemas ou DDLs) para identificar a convenção de versionamento e, quando houver codebase, onde ficam as regras de negócio. Aproveite também qualquer documentação já existente. Só publique uma descrição quando as evidências encontradas sustentarem a semântica dela; sem essa sustentação, marque a descrição como não confirmada.

Materiais complementares: o README do módulo em fontes/sei/src/main/php/sei/web/modulos/relacionamento-institucional/README.md e os prints de tela em specs/dicionario-ri/relacionamento-institucional/screenshots/.
Material prioritário: o README do módulo em fontes/sei/src/main/php/sei/web/modulos/relacionamento-institucional/README.md.

Confira as informações dos materiais com base na fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, informe explicitamente: 1) as tabelas ou colunas cuja semântica você não conseguiu confirmar nas fontes disponíveis; 2) o que faltou para confirmá-las; 3) os pontos em que algum material complementar divergiu da fonte estrutural, com a fonte que você adotou.
```

#### Atualizar o dicionário

Use quando o dicionário já existir e você quiser sincronizá-lo com as mudanças estruturais do sistema ou do módulo (novas tabelas, colunas ou regras de negócio), inclusive depois de uma nova versão. Também serve para corrigir uma descrição anterior, mas só quando houver divergência estrutural ou domínio incompleto já confirmado, nunca por ajuste de estilo.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados conforme o estado mais recente das fontes disponíveis.
- Alvo: <nome do sistema ou do módulo>

Compare o dicionário de dados e o changelog já existentes com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando os demais conteúdos.

Referência da atualização: <versão, commits ou scripts de mudança, se souber>. Se eu não indicar a referência, identifique o escopo da diferença pelas próprias fontes estruturais.

Materiais complementares: <arquivos anexados, esquema em outro formato, dicionário anterior, capturas de tela, manuais, vídeos ou transcrições, se houver>.
Material prioritário: <arquivo ou material ao qual dar mais atenção, opcional>.

Confira as informações dos materiais com base na fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente.
```

**Exemplo preenchido, sincronizar com a versão mais recente:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados conforme o estado mais recente das fontes disponíveis.
- Alvo: peticionamento

Compare o dicionário de dados e o changelog já existentes com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando os demais conteúdos.

Referência da atualização: da versão registrada no dicionário atual para a versão retornada por PeticionamentoIntegracao::getVersao(), usando fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_peticionamento.php como fonte estrutural.

Confira as informações dos materiais com base na fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente.
```

#### Revisar a qualidade do dicionário

Use quando quiser avaliar se um dicionário já existente segue os critérios de qualidade e as convenções da própria skill (completude, consistência, terminologia, distinções documentadas), sem alterar arquivos. A revisão olha só o dicionário, mesmo que o código tenha mudado depois da última atualização.

**Prompt:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados do alvo abaixo, sem alterar nenhum arquivo.
- Alvo: <nome do sistema ou do módulo>

Classifique cada achado como problema de qualidade documental (descrição incompleta, inconsistente, genérica ou fora das convenções da skill) ou como lacuna (elemento sem descrição). Liste claramente qualquer lacuna que impeça considerar a documentação como completa.
```

**Exemplo preenchido, dicionário já publicado:**

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados do alvo abaixo, sem alterar nenhum arquivo.
- Alvo: litigioso

Classifique cada achado como problema de qualidade documental (descrição incompleta, inconsistente, genérica ou fora das convenções da skill) ou como lacuna (elemento sem descrição). Liste claramente qualquer lacuna que impeça considerar a documentação como completa.
```

#### Gerar prints de tela como insumo complementar

Use este exemplo quando o módulo já tiver um ambiente de teste no ar, local ou remoto, antes de rodar o prompt. Os prints gerados aqui podem ser apontados como material complementar no exemplo "Criar o dicionário de dados".

Pré-requisito: veja "Pré-requisitos de Automação de Navegador (Playwright e Selenium)", bloco Playwright, no início deste arquivo.

**Prompt:**

```text
Gere os prints de tela do módulo abaixo para servirem de insumo complementar ao dicionário de dados (skill `dicionario-dados-db-scan-codebase-docs`).

Módulo: <nome do módulo>.

O ambiente de teste já está disponível em <endereço ou instrução para subir o ambiente>. Para autenticar, leia a credencial na <variável de ambiente ou arquivo local não versionado>; se não houver, peça a credencial no momento do uso. Nunca use credencial de produção.

Use a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble` (baixe se ainda não tiver localmente) para rodar um script de automação que:

1. Verifique se o módulo já está ativo nessa instância de teste, consultando o array `Modulos` em `fontes/sei/src/main/php/sei/config/ConfiguracaoSEI.php`. Se não estiver ativo, peça minha autorização para ativá-lo (edição local, sem comitar) antes de continuar; não edite sem essa confirmação.
2. Faça login no ambiente de teste.
3. Navegue por todas as telas relevantes do módulo, criando os dados de teste (seeds) necessários para preencher cada tela.
4. Capture um print de cada tela relevante (listagem, formulário vazio, formulário preenchido, modal, estado intermediário).
5. Salve os PNGs em <pasta de destino>/screenshots/, organizados por subpasta.
6. Exporte os seeds e dados de teste usados no passo 3 (SQL de insert ou passo a passo reprodutível) em <pasta de destino>/seeds/, para reaproveitar em futuras implementações sem recriar a massa de teste do zero.

Ao final, liste as telas que não conseguiu capturar e o motivo de cada uma.
```

**Exemplo preenchido, prints de um módulo no ambiente local:**

```text
Gere os prints de tela do módulo abaixo para servirem de insumo complementar ao dicionário de dados (skill `dicionario-dados-db-scan-codebase-docs`).

Módulo: relacionamento-institucional.

O ambiente de teste já está disponível em http://localhost:8000/sei, com o Docker iniciado conforme o `README.md`. Para autenticar, leia a credencial no arquivo local não versionado fontes/sei/ops_sei-docker/.env; se não houver, peça a credencial no momento do uso. Nunca use credencial de produção.

Use a imagem Docker `mcr.microsoft.com/playwright:v1.60.0-noble` (baixe se ainda não tiver localmente) para rodar um script de automação que:

1. Verifique se o módulo já está ativo nessa instância de teste, consultando o array `Modulos` em `fontes/sei/src/main/php/sei/config/ConfiguracaoSEI.php`. Se não estiver ativo, peça minha autorização para ativá-lo (edição local, sem comitar) antes de continuar; não edite sem essa confirmação.
2. Faça login no ambiente de teste.
3. Navegue por todas as telas relevantes do módulo, criando os dados de teste (seeds) necessários para preencher cada tela.
4. Capture um print de cada tela relevante (listagem, formulário vazio, formulário preenchido, modal, estado intermediário).
5. Salve os PNGs em specs/dicionario-ri/relacionamento-institucional/screenshots/, organizados por subpasta.
6. Exporte os seeds e dados de teste usados no passo 3 (SQL de insert ou passo a passo reprodutível) em specs/dicionario-ri/relacionamento-institucional/seeds/, para reaproveitar em futuras implementações sem recriar a massa de teste do zero.

Ao final, liste as telas que não conseguiu capturar e o motivo de cada uma.
```

### Modos Auxiliares (Skills Externas de Uso Geral)

Esta seção é diferente das anteriores. As skills aqui não resolvem uma demanda de SEI: elas mudam o modo como o agente trabalha em qualquer prompt deste arquivo. O `caveman` muda como o agente escreve, e o `grill-me` muda como o agente entrevista você.

As duas são opcionais e nenhuma liga sozinha. O agente nunca aciona esses modos por conta própria: eles só entram se você os invocar.

Nenhum desses modos afrouxa o `AGENTS.md`. Permissão e link assinado, transação, auditoria, encoding e o `php -l` obrigatório continuam valendo integralmente. Se a instrução do modo colidir com uma regra do `AGENTS.md`, vale o `AGENTS.md`.

Envie o comando sozinho, em uma mensagem separada, antes do prompt real. O `caveman` continua ativo nas respostas seguintes até você desligá-lo ou até a sessão acabar. O `grill-me` vale só para a resposta que ele gera.

#### Interrogar um plano ou um pedido utilizando o grill-me

Use antes de aprovar um plano ou antes de escrever um pedido. São três momentos típicos: antes do `/speckit-specify`, quando a tarefa ainda está só na sua cabeça e você não sabe como escrever o pedido; entre o `/speckit-specify` e o `/speckit-plan`, para interrogar a especificação antes de aprová-la; e antes de dar o OK no protocolo de execução dos prompts deste arquivo. Quando a entrevista vier antes do `/speckit-specify`, peça no fim o texto do pedido da fase, pronto para colar. Comece em uma janela nova.

A entrevista vem em rodadas. Cada rodada traz as perguntas que já dá para responder agora, numeradas e com a resposta que o agente recomenda, e o agente espera as suas respostas antes de abrir a rodada seguinte. Quando a pergunta puder ser respondida lendo o código, o agente busca o dado em vez de perguntar. A entrevista acaba quando não sobra pergunta em aberto. Nada é gravado em arquivo: se quiser guardar o que ficou decidido, peça no fim da entrevista.

Não peça a entrevista nem descreva o formato das perguntas: a skill já cuida das duas coisas. Diga só três coisas: o que vai ser interrogado, a decisão que ainda está em aberto e o que mais preocupa você. Responder "tanto faz" ou concordar com tudo esvazia a entrevista: são as suas objeções que fazem o agente mudar de direção.

**Prompt:**

```text
/grill-me

<o plano, a spec ou a decisão a ser interrogada>

Ainda em aberto: <a decisão que você não tomou>

Me preocupa: <o que mais preocupa você>
```

**Exemplo preenchido, interrogar um plano do Speckit:**

```text
/grill-me

O plano gerado pelo /speckit-plan para o relatório de demandas por tema do módulo relacionamento-institucional.

Ainda em aberto: se o relatório entra como opção nova no menu do módulo ou como aba dentro da listagem de temas que já existe.

Me preocupa: recurso e perfil novos no SIP, desempenho da consulta quando um tema tem muitas demandas, e o que a tela mostra para demandas sem tema associado.
```

#### Comprimir a resposta utilizando o caveman

Use quando a sessão for gerar texto longo, como a revisão técnica de um módulo inteiro, e você quiser o conteúdo sem a prosa em volta. O `caveman` corta artigo, ressalva e frase de cortesia. Ele não corta conteúdo técnico: termo técnico, trecho de código, nome de classe ou de API e mensagem de erro saem literais, iguais ao modo normal. Código, mensagem de commit e descrição de PR também continuam em texto normal.

A skill tem seis níveis, e três servem para o trabalho neste repositório. O `lite` mantém frase completa e tira só o excesso. O `full` é o padrão e usa frase fragmentada. O `ultra` abrevia palavra de prosa (DB, config, req) e nunca abrevia nome de função, símbolo de código ou mensagem de erro. Os outros três (`wenyan-lite`, `wenyan-full` e `wenyan-ultra`) escrevem em chinês clássico e não têm uso aqui.

Na sequência, na mesma janela, envie o prompt real. Exemplo: envie `/caveman full` e depois o prompt de "Revisar um módulo ou um arquivo" deste arquivo, para receber o mesmo relatório sem o texto de apoio. Para voltar ao normal, envie `stop caveman`.

O bloco abaixo não tem campo para preencher, então já é o texto final para copiar.

```text
/caveman full
```
