# Adaptador: módulo customizado do SEI ou do SIP

Família InfraPHP. Aplique `../convencoes-infraphp.md`. Julgar usa `../julgar.md`.

Este arquivo define a regra comum. Carregue um arquivo de `modulos/` somente quando o alvo corresponder à seleção declarada em "Overlays".

## Reconhecimento

Nome explícito do módulo, raiz em `sei/web/modulos/` ou `sip/web/modulos/`, e pasta correspondente em `docs/dicionario_dados/` são evidências diretas. Prefixo `md_*` ou nome isolado de tabela é provisório; discrimine a propriedade nos scripts, DTOs e caminhos.

## Fonte estrutural

Use `.agents/references/mapa-modulos-scripts.md` apenas para localizar candidatos. Abra e confirme fisicamente os scripts dos lados SEI e SIP; os arquivos encontrados, não o mapa, são a fonte estrutural.

Padrões de localização frequentes:

- `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_<modulo>.php`;
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_<modulo>.php`.

Se o mapa não trouxer o módulo, busque nome da integração, parâmetro de versão e prefixo das tabelas nos dois diretórios de scripts. Não conclua ausência por um único padrão de nome.

## Versionamento

Regra comum de renderização de versão-alvo (`vM.m.p` nos dicionários, regex de `formato`/`changelog`) fica em `../convencoes-infraphp.md`.

### Gramática comum

Nos scripts que a implementam, `$historicoVersoes` ordena versões, o `switch` sobre o parâmetro instalado liga cada `case 'M.m.p'` ao próximo `instalarv...()`, e o fluxo sem `break` acumula atualizações. O nome comprimido `instalarv<dígitos>` não decide sozinho onde separar major, minor e patch: use o `case` chamador e a atualização interna do parâmetro. `$nmVersao`, quando existir, é apenas confirmação adicional; sua ausência não autoriza inferência pelo nome do método.

Scripts baseados em `setArrVersoes`, curingas, letras maiúsculas ou sufixos de pré-release exigem overlay ou decisão explícita antes da extração. Nesta gramática, ordene pelo histórico efetivamente usado pelo script, nunca por comparação textual.

### Identificadores e âncoras

- Âncora primária: versão literal no `case` mais a chamada de instalação seguinte.
- Âncora de ordenação: lista ou mapa de versões efetivamente usado pelo script.
- Âncora de alvo: método público de instância `getVersao()` da classe `*Integracao.php`.
- Âncora estrutural inicial: caminho executado quando o parâmetro de versão está ausente.

### Extração por versão

Resolva primeiro a lista ou o mapa e o `case` que chama cada método. Delimite o método por contagem de chaves, preserve a ordem e a queda intencional do `switch`, e siga apenas auxiliares realmente chamados. Extraia SEI e SIP separadamente; combine somente efeitos estruturais compatíveis. Bloco sem DDL não cria entrada estrutural.

### Baseline e alcance

Não há cobertura completa presumida para todo módulo. Para cada alvo, prove o baseline verificando se o primeiro caminho executável a partir da ausência de versão cria todas as estruturas iniciais e se não há fonte anterior ausente. Declare o alcance somente entre versões comprovadas pelos scripts encontrados.

Sem essa prova, permita apenas atualização ou verificação no intervalo comprovado e bloqueie criação ou reconstrução integral.

### Versão-alvo

Leia o retorno do método de instância `<Modulo>Integracao::getVersao()` no código, sem invocá-lo estaticamente. Compare com todo marcador corrente dos scripts SEI e SIP; não escolha uma fonte por convenção.

## Títulos

- Dicionários: preserve o H1 comum existente quando o alvo já estiver documentado. Em alvo novo, use `Dicionário de Dados do Módulo <nome oficial>`, com o nome comprovado por `getNome()` ou documentação local; se o nome oficial já começar com "Módulo", não repita o prefixo.
- `CHANGELOG.md`: preserve o H1 existente. Em alvo novo, use `Changelog do Módulo <nome oficial>`, com a mesma regra de não repetir "Módulo" quando o nome oficial já começar assim.
- Relatório de atualização: aplique o template de `../convencoes-infraphp.md` com o nome exato da pasta confirmada em `docs/dicionario_dados/` como slug.

Divergência de nomes entre integração, documentação e artefatos existentes exige confirmação.

## Camadas semânticas

Inventarie as raízes SEI/SIP e classifique os artefatos existentes pelo mapa de `../convencoes-infraphp.md`: scripts; `README.md` e documentos; `dto/`, `rn/`, `bd/`, `int/`, `api/`, `ws/`, páginas, `js/`, relatórios e testes. Ausência comprovada é `inaplicável`; candidato remoto declarado pelo overlay é `externo sujeito a autorização`. Exclua dependências e manifestos sem referência direta do módulo.

## Estratégia de busca

Área de busca:

- `fontes/sei/src/main/php/sei/web/modulos/<caminho-do-modulo>/`;
- `fontes/sei/src/main/php/sip/web/modulos/<caminho-do-modulo>/`, quando existir;
- scripts estruturais confirmados nos dois lados;
- documentos locais declarados pelo inventário ou overlay.

Aplique "Técnicas de busca" de `../convencoes-infraphp.md`. Acumule estrutura em ordem e confira cada objeto contra DTO e BD. Um arquivo `bd/` sem consulta de leitura pode ser definição estrutural ou utilitário; classifique pelo conteúdo.

## Particularidades

- A raiz publicada em `docs/dicionario_dados/` pode não coincidir com o nome físico do módulo. Confirme o destino existente ou peça decisão; não crie correspondência por semelhança.
- O lado SIP pode conter apenas recursos e menus ou também DDL. Inspecione-o em toda versão.
- Fonte externa não é estrutural e não resolve conflito entre scripts locais.

## Overlays

| Alvo reconhecido | Overlay exclusivo |
|---|---|
| PEN, Tramita GOV.BR, `modulos/pen/` | `pen.md` |

Não carregue esse overlay para outro módulo.

## Validações

- Confirme scripts SEI e SIP, baseline, alcance e versão-alvo para o módulo selecionado.
- Registre somente camadas encontradas, ausências que afetem a fórmula e candidatos externos.
- Compare fonte estrutural com DTO e BD no escopo tocado.
- Rode os validadores gerais com o padrão de identificação e objetos técnicos do alvo.

## Bloqueios

- Módulo sem fonte estrutural versionada localizável: bloqueie.
- Baseline não comprovado: bloqueie criação e reconstrução integral; limite atualização e verificação ao alcance comprovado.
- Versão-alvo ausente ou fontes divergentes: bloqueie escrita e validações dependentes da versão; permita verificação parcial no alcance comprovado, reporte todas as leituras e não invente precedência.
- Gramática fora da regra comum sem overlay: bloqueie e peça decisão.
- Destino ou propriedade da tabela ambíguos: bloqueie até confirmação.
- Fonte externa necessária: aplique a política de execução e aguarde autorização explícita.

## Destino

- Dicionários e `CHANGELOG.md`: pasta existente confirmada em `docs/dicionario_dados/<alvo>/`; em alvo novo, confirme `<alvo>` antes de escrever.
