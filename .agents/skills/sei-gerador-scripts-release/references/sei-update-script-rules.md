# Regras Especificas para Script de Release SEI

## Escopo

Esta referencia cobre apenas `fontes/sei/src/main/php/sei/scripts/*`.

## Estrutura do script

- `require_once dirname(__FILE__) . '/../web/SEI.php';`
- classe `*AtualizadorSeiRN` estendendo `InfraRN`
- propriedades para versao atual, nome do modulo, nome do parametro e historico de versoes
- `inicializarObjInfraIBanco()` retornando `BancoSEI::getInstance()`
- `inicializar()`, `logar()` e `finalizar()` no corpo da classe
- `atualizarVersaoConectado()` como fluxo principal
- `switch` com `fallthrough` para chamar `instalarv*()`
- `instalarv*()` incremental por versao
- bootstrap final com `SessaoSEI::getInstance(false)`, `BancoSEI::getInstance()->setBolScript(true)`, validacao de configuracao do modulo, `class_exists(*Integracao)`, autenticacao via `InfraScriptVersao::solicitarAutenticacao()` e chamada a `atualizarVersao()`

## Referencias principais

- Padrao principal: `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_ia.php`
- Referencia secundaria: `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_relacionamento_institucional.php`
- Se o desenvolvedor apontar outra referencia, ela substitui o padrao principal para a estrutura do arquivo.

## Fluxo base

1. validar banco suportado
2. validar versao minima do framework
3. conferir `getVersao()` da classe de integracao contra `$versaoAtualDesteModulo`, com o trecho de `.agents/references/padrao-scripts-release.md`, secao "Classe de integração do módulo"
4. testar permissao DDL com tabela temporaria (`sei_teste`)
5. obter parametro de versao
6. executar `switch` com `fallthrough`
7. finalizar com log de sucesso

## Familia `InfraScriptVersao`

- Script existente que estende `InfraScriptVersao` preserva essa familia: metodos `versao_X_Y_Z` registrados em `setArrVersoes()` e `setStrClasseModulo()` apontando para a classe de integracao, como em `fontes/sei/src/main/php/sei/scripts/md_julgar_atualizacao_sei.php`.
- Nessa familia, as regras de DDL, sequence e seeds desta referencia continuam valendo; a estrutura do script, o fluxo base acima e os bloqueios estruturais abaixo valem para a familia `InfraRN`.

## Bloqueios estruturais

- Bloquear se script novo for gerado em `InfraScriptVersao` como classe base sem autorizacao explicita.
- Bloquear se faltar `atualizarVersaoConectado()`.
- Bloquear se faltar `switch` incremental com `fallthrough`.
- Bloquear se faltar qualquer um dos metadados de versao do modulo.
- Bloquear se o bootstrap final do arquivo divergir da referencia escolhida sem desvio aprovado.
- Bloquear se houver chamada a metodo/helper sem implementacao visivel no proprio arquivo, na classe pai ou no core confirmado.

## DDL

- `CREATE TABLE` pode ser SQL bruto
- tipos devem vir de `InfraMetaBD::tipo*()`
- PK via `adicionarChavePrimaria()`
- FK via `adicionarChaveEstrangeira()`
- indices adicionais via `criarIndice()`
- reconciliacao de legado via `processarIndicesChavesEstrangeiras()`
- `$objInfraMetaBD->setBolValidarIdentificador(true)` logo depois de criar a `InfraMetaBD`
- quarto parametro de `adicionarColuna` e `alterarColuna` em texto e em minusculas: `'null'` ou `'not null'`
- padroes multibanco de `.agents/references/padrao-scripts-release.md`: limite de cada `tipo*()`, tipo da coluna de FK, FK nas colunas da PK, indice unico, coluna `NOT NULL` em tabela com dados, alterar ou excluir coluna com FK ou indice, trocar tipo de coluna com dados, checagem de existencia e leitura e gravacao de dados no script

## Sequence

- criar com `BancoSEI::getInstance()->criarSequencialNativa('seq_<tabela>', 1)`, inclusive quando o script-alvo ja ramifica por banco para sequence
- remover e ajustar o proximo valor: `.agents/references/padrao-scripts-release.md`, secoes "Remover sequence" e "Ajustar o próximo valor de uma sequence"
- nao crie sequence para tabela N:N com PK composta

## Seeds e parametros

- prefira RN/DTO/BD do core e do modulo para seed inicial
- use `InfraParametroBD` ou RN correspondente para atualizar versao e parametros
- evite `INSERT` ou `UPDATE` bruto quando a camada de negocio ja existir
- parametro funcional, configurado pelo orgao: criar com o valor padrao so quando ele nao existe, com `isSetValor` e `setValor` da `InfraParametro` e as constantes da RN; detalhe em `.agents/references/padrao-classes-sistema-sei.md`, secao "InfraParametro"
- em `instalarv100()`, o padrao principal aceita insercao inicial explicita em `infra_parametro`, conforme o modulo IA
- em upgrades posteriores, so use helper local de atualizacao de versao se ele existir e estiver alinhado ao script de referencia

## Validacoes especificas do SEI

- e aceitavel validar o modulo em `ConfiguracaoSEI` e `class_exists(*Integracao)` no bootstrap final
- nao mova esse padrao para scripts SIP

## Riscos conhecidos

- `tipoNumero()` e `tipoNumeroGrande()` nao recebem parametro; gere a chamada sem argumento
- nao misture recursos SIP, menus ou perfis no script SEI
- nao deixe efeitos colaterais demorados dentro da transacao principal

## Exemplo de helper util

- `fixIndices(InfraMetaBD $objInfraMetaBD, $arrTabelas)` chamando `processarIndicesChavesEstrangeiras()` e um bom padrao para upgrades corretivos
