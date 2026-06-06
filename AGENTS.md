# Diretrizes de Desenvolvimento - SEI

## Contexto

Repositorio de customizacoes e modulos SEI/SIP com release versionado e padroes InfraPHP. Trate o projeto como sistema administrativo legado com requisitos de auditoria, permissao e compatibilidade de release.

## Dependências Técnicas do Projeto

- **PHP 8.2** — encoding ISO-8859-1 (Latin-1)
- Extensões PHP previstas no manual de instalação do SEI
- Módulos SEI / SIP
- InfraPHP (DTO, RN, BD, páginas)
- Bootstrap 5.3.1
- jQuery 3.7.0
- jQuery UI 1.13.2

## Escopo e Limites de Escrita

**Permitido:**
- `fontes/sei/src/main/php/sei/web/modulos/**`
- `fontes/sei/src/main/php/sei/scripts/**`
- `fontes/sei/src/main/php/sip/scripts/**`
- `specs/**`
- `.agents/**`

**Proibido sem autorização:**
- `fontes/sei/src/main/php/sei/web/**` fora de `modulos/`
- `fontes/sei/src/main/php/sip/web/**`
- `infra/**`

Mudança no core exige proposta documentada — sem patch direto.

## Hierarquia de Autoridade

- Em Fluxo Direto, siga este arquivo.
- Em Spec Kit, siga `constitution.md` para regras de fase e bloqueio.
- Se houver conflito entre documentos, pare e peca decisao do desenvolvedor.

## Guardrails Universais

- **Permissão/link assinado**: `validarLink` + `validarPermissao` em toda ação; `verificarPermissao` em UI condicional; `assinarLink` em links de ação
- **SIP**: recursos `md_<sigla>_<recurso>`; perfis `MD_<sigla>_<recurso>`
- **Transação**: escrita relevante exige `BancoSEI` ou `InfraRN *Controlado`
- **Efeitos colaterais**: e-mail, Solr e integrações externas devem ocorrer após o commit; nunca dentro da transação crítica
- **Andamentos**: usar `id_tarefa_modulo`; `id_tarefa < 1000` reservado (exceto `ID_TAREFA=65` com atributo `DESCRICAO`)
- **API**: preferir `Entrada*API` / `Saida*API` / `SeiRN`; evitar objetos internos
- **Entrada HTTP**: proibido `$_REQUEST`; usar `PaginaSEI::POST/GET` com normalização de tipo (`int`, `int[]`, enum)
- **Camadas de módulo**: `dto/`, `rn/`, `bd/`, `int/`, paginas, `css/`, `js/`, `svg/`, `imagens/`, `menu/`. SEI estende `SeiIntegracao`; `SipIntegracao` só quando houver suporte explícito no contexto SIP. Não extrapolar regras de ativação do SEI para scripts SIP
- **Assets**: se `css/` ou `js/` já existirem, editar; nunca criar novos
- **Core**: `ConfiguracaoSEI.php` é somente referência; não editar
- **Gabaritos**: referência mínima `abc/exemplo`; referência robusta `trf4/julgamento`
- **CRUD com impacto de release**: quando a demanda envolver novo DTO, nova tabela, nova entidade CRUD base, alteracao de colunas de DTO existente em modulo mapeado em `.agents/references/mapa-modulos-scripts.md`, avise explicitamente o desenvolvedor que a entrega tambem exige atualizacao dos scripts SEI/SIP do modulo, com sincronizacao de versao em `*Integracao.php` quando aplicavel.
- **Gerador de CRUD**: use `sei-gerador-crud` apenas com escolha explícita do desenvolvedor. Se usado, a skill propria cobre a fase de release. Se nao usado, roteie release para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release`.

### Padrão Transacional Obrigatório

Se a operação mistura persistência com efeitos colaterais, separe em duas etapas: o método `*Controlado` faz apenas a gravação em banco; indexação, e-mail e integrações externas disparam somente após o commit.

```php
protected function gerarProcedimentoControlado($arrParametros)
{
    FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(true);
    $retorno = $this->gerarProcedimentoInterno($arrParametros);

    FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(false);
    FeedSEIProtocolos::getInstance()->indexarFeeds();

    try {
        $rn = new MdAbcEmailNotificacaoRN();
        $rn->notificar($retorno['parametrosEmail']);
    } catch (Exception $e) {}

    return $retorno['parametrosRecibo'];
}

protected function gerarProcedimentoInterno($arrParametros)
{
    // Apenas persistencia em banco; executado dentro da transacao.
}
```

Se e-mail ou indexação falharem dentro da transação, `cancelarTransacao()` pode desfazer silenciosamente a persistência crítica.

## Qualidade Mínima

- `php -l` em todo arquivo PHP alterado — sem erros
- **Encoding**: ISO-8859-1 (Latin-1). O blob final é normalizado por `.gitattributes`; validar compatibilidade com Latin-1, ausência de BOM e ausência de caracteres fora de Latin-1. Não salvar manualmente o blob em ISO-8859-1 quando a worktree estiver em UTF-8 sob controle do Git.
- **Sanitização**: sem concatenação insegura em HTML, JS, SQL e URLs
- **PHP moderno**: em código PHP novo ou alterado, usar `[]` em vez de `array()`
- **Tipagem/PHPDoc**: em código PHP novo ou alterado, preferir type hints seguros e PHPDoc breve nos métodos alterados, preservando compatibilidade com assinaturas herdadas
- **Auditoria**: preservar trilha em operações críticas; nunca logar segredos/PII
- **Ferramentas opcionais**: quando aplicável, rodar `composer test`, `phpcs` ou `phpstan`
- **Release/BD**: compatibilidade multi-SGBD; sincronismo de versão entre SEI, SIP e `*Integracao.php`

## Regras de Decisao

- Ao aplicar qualquer regra, citar o arquivo e a seção de origem
- Nunca inventar padrão não documentado neste repositório
- Em caso de conflito entre documentos: parar, identificar os dois documentos conflitantes e aguardar decisão do desenvolvedor antes de prosseguir
- Em caso de ambiguidade de contrato ou requisito: perguntar, nunca inferir

## Fontes de Contexto

- **PRD.md**: fonte de contexto funcional e regras de negócio. Consultar quando a tarefa depender de contexto de módulo, usuário, regra de domínio, fluxo funcional ou impacto de negócio. Se a regra de negócio não estiver em PRD.md, perguntar ao desenvolvedor.
- **docs/manual_desenvolvimento_md/**: manual oficial de desenvolvimento de módulos SEI (capítulos 2-10). Fonte primária para criação/ativação de módulo, InfraPHP, modelagem, codificação, gerador CRUD, classes API, eventos e operações.
- **skill-routing-and-contracts.md**: matriz de demanda, skill principal, skills complementares, contratos obrigatórios e gate de bloqueio.
- **implementation-gates.md**: gates de bloqueio para problemas técnicos críticos.
- **mapa-modulos-scripts.md**: mapeamento de módulo para scripts SEI/SIP — consultar quando houver impacto de release.
- **padrao-*.md**: padrões detalhados de codificação, modelagem de dados e scripts — consultar quando precisar de regra específica.

## Roteamento

1. **Classificar a demanda** pelo tipo usando a matriz em `.agents/references/skill-routing-and-contracts.md`
2. **Skill principal** responde pelo fluxo; **skills complementares** são gates obrigatórios
3. **Gates por artefato** — sempre acionar se o artefato existir na demanda:

   | Artefato | Skill de gate |
   |---|---|
   | Página PHP (`*_lista.php`, `*_cadastro.php`) | `sei-verificacao-pagina` |
   | Classe RN (`*RN.php`) | `sei-verificacao-rn` |
   | Classe BD (`*BD.php`) | `sei-verificacao-banco-dados` |
   | Script de tarefa (`*_tarefa.php`) | `sei-verificacao-tarefa` |
   | Controlador em `*Integracao.php` (Ajax/WS) | `sei-verificacao-controladores` |
| Demanda ambígua ou novo padrão | `sei-guardrails-modulo` |
   | Qualquer entrega PHP | `sei-testes-validacao` após implementação |

4. **Release**: se não usar `sei-gerador-crud`, rotear para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` conforme o lado afetado
