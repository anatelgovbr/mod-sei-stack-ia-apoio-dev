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

## Fluxo base observado

1. validar banco suportado
2. validar versao minima do framework
3. testar permissao DDL com tabela temporaria (`sei_teste`)
4. obter parametro de versao
5. executar `switch` com `fallthrough`
6. finalizar com log de sucesso

## Bloqueios estruturais

- Bloquear se o script for gerado em `InfraScriptVersao` como classe base sem autorizacao explicita.
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

## Sequence

- preferencia: `BancoSEI::getInstance()->criarSequencialNativa('seq_<tabela>', 1)`
- se o script-alvo ja usar branching por SGBD para sequence, preserve esse estilo
- nao crie sequence para tabela N:N com PK composta

## Seeds e parametros

- prefira RN/DTO/BD do core e do modulo para seed inicial
- use `InfraParametroBD` ou RN correspondente para atualizar versao e parametros
- evite `INSERT` ou `UPDATE` bruto quando a camada de negocio ja existir
- em `instalarv100()`, o padrao principal aceita insercao inicial explicita em `infra_parametro`, conforme o modulo IA
- em upgrades posteriores, so use helper local de atualizacao de versao se ele existir e estiver alinhado ao script de referencia

## Validacoes especificas do SEI

- e aceitavel validar o modulo em `ConfiguracaoSEI` e `class_exists(*Integracao)` no bootstrap final
- nao mova esse padrao para scripts SIP

## Riscos conhecidos

- nao reproduza chamadas legadas como `tipoNumero(2)` ou `tipoNumeroGrande(20)` sem confirmar assinatura do core
- nao misture recursos SIP, menus ou perfis no script SEI
- nao deixe efeitos colaterais demorados dentro da transacao principal

## Exemplo de helper util

- `fixIndices(InfraMetaBD $objInfraMetaBD, $arrTabelas)` chamando `processarIndicesChavesEstrangeiras()` e um bom padrao para upgrades corretivos
