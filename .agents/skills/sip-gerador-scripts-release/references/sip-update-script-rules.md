# Regras Especificas para Script de Release SIP

## Escopo

Esta referencia cobre apenas `fontes/sei/src/main/php/sip/scripts/*`.

## Estrutura do script

- `require_once dirname(__FILE__) . '/../web/Sip.php';`
- familia estrutural principal no repositorio: classe `*AtualizadorSipRN` estendendo `InfraRN`
- variante estrutural existente no repositorio: adaptador com `InfraScriptVersao` delegando para uma RN de atualizacao do modulo
- propriedades para versao atual, nome do modulo, nome do parametro e historico de versoes
- `inicializarObjInfraIBanco()` retornando `BancoSip::getInstance()`
- `inicializar()`, `logar()` e `finalizar()` no corpo da classe
- `atualizarVersaoConectado()` como fluxo principal
- `switch` com `fallthrough` para chamar `instalarv*()`
- `instalarv*()` incremental por versao
- helper local no proprio script para recurso, item de menu, vinculos de perfil e auditoria, salvo referencia estrutural diferente aprovada
- bootstrap final compativel com a familia estrutural escolhida

## Referencias principais

- Padrao principal: `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_ia.php`
- Referencia secundaria: `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_relacionamento_institucional.php`
- Variante consolidada: `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_pen.php`
- Se o desenvolvedor apontar outra referencia, ela substitui o padrao principal para a estrutura do arquivo.

## Escolha da familia estrutural

- Se o modulo-alvo ja possui script SIP, preservar a familia estrutural existente.
- Para script novo sem historico, preferir a familia `*AtualizadorSipRN extends InfraRN`.
- Nao forcar migracao entre familias estruturais sem necessidade real ou pedido explicito do desenvolvedor.

## Fluxo base observado

1. validar banco suportado
2. validar versao minima do framework
3. testar permissao DDL com tabela temporaria (`sip_teste`)
4. obter parametro de versao
5. executar `switch` com `fallthrough`
6. finalizar com log de sucesso

## Literais obrigatorios do lado SIP

- sistema `SEI`
- menu `Principal`
- item de menu pai com o mesmo rotulo da referencia estrutural escolhida, inclusive acentuacao quando houver
- perfis-base `Administrador` e `Basico` quando aplicavel

## Bloqueios estruturais

- Bloquear se a familia estrutural consolidada do modulo-alvo for trocada sem desvio aprovado explicitamente.
- Bloquear se faltar `atualizarVersaoConectado()`.
- Bloquear se faltar `switch` incremental com `fallthrough`.
- Bloquear se faltar qualquer um dos metadados de versao do modulo.
- Bloquear se recursos, perfis, menu e item de menu forem criados sem lookup previo.
- Bloquear se o bootstrap final do arquivo divergir da referencia escolhida sem desvio aprovado.
- Bloquear se houver chamada a metodo/helper sem implementacao visivel no proprio arquivo, na classe pai ou no core confirmado.

## Responsabilidades centrais

- localizar o sistema `SEI` no banco SIP
- localizar perfis-base, como `Basico` e `Administrador`
- localizar menu `Principal` e o item de menu pai com o mesmo rotulo da referencia estrutural escolhida quando necessario
- criar recursos
- criar itens de menu
- criar relacoes perfil-recurso e perfil-item-menu
- remover ou desativar recursos, itens e relacoes quando a release exigir manutencao controlada
- tratar auditoria e replicacao

## Helpers observados no script de referencia

- `adicionarRecursoPerfil(...)`: consulta, cria recurso se ausente e cria vinculo de perfil se necessario
- `adicionarItemMenu(...)`: consulta, cria item se ausente e cria relacoes de perfil se necessario
- `_cadastrarAuditoria(...)`: cria ou consulta regra, vincula recursos e replica a regra
- `removerRecursoPerfil(...)`, `desativarRecurso(...)`, `removerRecurso(...)`: padroes reais de manutencao observados em scripts historicos do repositorio

## Regras operacionais

- use RN/DTO do SIP antes de qualquer SQL direto
- consulte antes de cadastrar qualquer recurso, item de menu ou relacao
- em manutencao, consulte antes de remover, desativar ou excluir qualquer recurso, item de menu ou relacao
- use SQL direto em auditoria apenas como fallback controlado, e sempre com checagem de existencia ou justificativa clara
- nao transporte checagens de `ConfiguracaoSEI` ou `class_exists(*Integracao)` para o bootstrap SIP

## Parametros e versao

- o parametro de versao deve ser lido e atualizado no banco SIP
- o `switch` deve permanecer incremental, com `fallthrough`
- em `instalarv100()`, o padrao principal aceita insercao inicial explicita em `infra_parametro`, conforme o modulo IA
- em upgrades posteriores, so use helper local de atualizacao de versao se ele existir e estiver alinhado ao script de referencia

## Riscos conhecidos

- criar recursos ou menus duplicados por falta de consulta previa
- esquecer de replicar a regra de auditoria ao final
- misturar responsabilidade de DDL do SEI dentro do script SIP
