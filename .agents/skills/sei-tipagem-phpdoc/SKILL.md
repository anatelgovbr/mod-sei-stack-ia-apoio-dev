---
name: sei-tipagem-phpdoc
description: >
  Tipagem PHP, type hints, PHPDoc, docblock, propriedades tipadas e
  modernizacao de assinaturas em classes e scripts SEI/SIP. Use quando o
  desenvolvedor pedir explicitamente para tipar codigo PHP existente,
  adicionar descricao breve aos metodos, ou modernizar assinaturas sem
  refatorar paginas procedurais. Nao usar por roteamento automatico.
---

# sei-tipagem-phpdoc

Skill para aplicar tipagem segura e PHPDoc breve em codigo PHP do repositorio.

## Acionamento

Esta skill e opt-in.
So deve ser usada quando o desenvolvedor pedir explicitamente tipagem,
`type hints`, `PHPDoc`, `docblocks`, propriedades tipadas ou modernizacao de
assinaturas.

Nao e gate obrigatorio e nao deve ser acionada por heuristica ampla.

## Fonte de verdade

- `AGENTS.md`
- `.agents/references/padrao-codificacao-php.md`
- `.agents/references/roteamento-de-skills.md`
- `fontes/sei/src/main/php/infra/infra_php/` quando a compatibilidade com o core estiver ambigua — ler o arquivo pai diretamente

## Quando usar

- Pedido explicito para adicionar `type hints`, `tipagem`, `phpdoc`, `docblock`
  ou `propriedades tipadas`
- Modernizacao pontual de assinaturas sem mudanca de comportamento
- Classes `*Integracao.php`, `*RN.php`, `*DTO.php`, `*BD.php`
- Scripts de instalacao/atualizacao em `sei/scripts/*` e `sip/scripts/*`

## Quando nao usar

- Demandas em que a mudanca principal e de comportamento, release, evento,
  operacao, pagina, menu ou modelagem; nesses casos, usar a skill padrao da
  demanda e tratar esta skill como complementar apenas se houver tipagem
  envolvida
- Demandas gerais de manutencao em que o desenvolvedor nao pediu tipagem de
  forma explicita
- Paginas procedurais `*_lista.php` e `*_cadastro.php` por padrao
- Refatoracao estrutural apenas para forcar tipagem
- Adicao de `declare(strict_types=1)` sem solicitacao explicita do desenvolvedor

## Objetivo

Aplicar tipagem e documentacao minima com o menor diff correto, preservando os
contratos herdados do core e a estrutura vigente do artefato.

## Fluxo

1. Confirmar escopo dos arquivos alvo.
2. Identificar a hierarquia antes de editar:
   - `SeiIntegracao`
   - `InfraRN`
   - `InfraDTO`
   - classe pai concreta ou interface relevante
3. Classificar cada metodo antes da tipagem:
   - `private` / helper local
   - construtor
   - metodo publico/protegido sem override relevante
   - override de metodo do core
4. Aplicar tipagem segura.
5. Adicionar PHPDoc breve.
6. Rodar validacoes obrigatorias por artefato.

## Regras de tipagem

### 1. Prioridade de seguranca

Aplicar preferencialmente nesta ordem:

1. propriedades com atribuicoes estaveis
2. metodos `private` e helpers locais
3. construtores
4. metodos `public`/`protected` sem heranca sensivel
5. overrides do core, somente apos verificar compatibilidade

### 2. Overrides

- Sempre conferir a assinatura no arquivo pai antes de adicionar tipos.
- Nao estreitar parametros em override quando o pai estiver sem tipo ou usar
  contrato mais amplo.
- Tipos de retorno podem ser adicionados quando o contrato estiver claro e
  permanecer compativel com a heranca.
- Em duvida sobre compatibilidade, manter o parametro sem tipo e registrar isso
  no resultado.

### 3. Tipos preferidos

- Preferir tipos nativos: `string`, `int`, `bool`, `float`, `array`, `?Tipo`,
  `int|float`
- Tipar propriedades apenas quando o conjunto de atribuicoes for coerente ao
  longo do arquivo
- Para colecoes, usar `array` na assinatura e o tipo interno no PHPDoc

### 4. Fora de escopo padrao

- Nao extrair funcoes de paginas procedurais apenas para adicionar type hints
- Nao renomear metodos, mover blocos ou alterar fluxo funcional sem necessidade

## Regras de PHPDoc

- Comecar com uma frase curta explicando o que o metodo faz
- Incluir `@param`, `@return` e `@throws` quando agregarem contexto real
- Para arrays relevantes, documentar tipo interno: `string[]`, `FooDTO[]`
- Evitar comentarios redundantes ou mecanicos
- Em funcoes triviais, manter o bloco enxuto

## Regras por artefato

### `*Integracao.php`

- Priorizar tipos de retorno e propriedades tipadas
- Parametros de metodos herdados de `SeiIntegracao` so podem ser tipados apos
  confirmar compatibilidade com o pai
- Se houver metodos de controlador (`processarControladorAjax*`,
  `processarControladorWebServices`, `tratarLinkSemAssinatura`), acionar o gate
  `sei-verificacao-controladores`

### `*RN.php`

- Tipar helpers locais e CRUDs quando o contrato do metodo for claro
- Preservar a separacao entre RN e BD
- Se houver controle manual de transacao, nao alterar fluxo so por tipagem

### `*DTO.php`

- Tipar retorno de `getStrNomeTabela()` e `montar()` quando compativel
- Documentar arrays relevantes no PHPDoc

### `*BD.php`

- Tipar construtor e helpers locais sem alterar o comportamento da camada BD

### Scripts `sei/scripts/*` e `sip/scripts/*`

- Preservar a estrutura padrao do script de release
- Nao alterar bootstrap, `switch`, estrategia de versao, lookups ou helpers por
  motivo cosmetico
- Esta skill pode atuar em tipagem/PHPDoc desses scripts, mas a referencia
  estrutural continua sendo responsabilidade das skills de release

## Validacao obrigatoria

- `php -l` em todo arquivo PHP alterado
- `sei-testes-validacao` como complemento em qualquer entrega PHP
- `sei-verificacao-rn` para `*RN.php`
- `sei-verificacao-banco-dados` para `*BD.php`
- `sei-verificacao-controladores` quando houver controlador em `*Integracao.php`
- `sei-verificacao-pagina` apenas se o desenvolvedor autorizar tocar paginas
- `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` como gate
  complementar quando a tipagem for aplicada em scripts de release

## Saida esperada

- Arquivos com type hints seguros e PHPDoc breve
- Registro claro do que foi tipado
- Registro explicito do que ficou sem tipo por risco de compatibilidade com o core
