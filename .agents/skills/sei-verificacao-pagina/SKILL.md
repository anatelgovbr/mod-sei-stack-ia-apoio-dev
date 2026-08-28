---
name: sei-verificacao-pagina
description: >
  Skill padrao de validacao para paginas PHP SEI/SIP. Audita controles de
  pagina documentados no manual do SEI e guardrails locais do projeto:
  `validarLink`, `validarPermissao`, `assinarLink`, `verificarPermissao`,
  `PaginaSEI::tratarHTML`, compatibilidade de encoding com `.gitattributes` e
  heuristicas complementares de entrada/saida HTTP. Gate obrigatorio para
  qualquer pagina `*_lista.php` ou `*_cadastro.php`.

  Use quando:
  - nova pagina PHP criada ou alterada no modulo
  - code review de paginas existentes
  - gate automatico disparado por `sei-guardrails-modulo`
---

# sei-verificacao-pagina

## Escopo Padrao

- paginas `*_lista.php`, `*_cadastro.php`, `controlador.php`, `index.php`
- link assinado e permissao em pagina
- entrada HTTP e saida HTML no contexto da pagina
- compatibilidade de encoding do arquivo PHP

## Regras SEI Explicitas (bloqueantes)

| ID | Regra | Severidade | Base |
|---|---|---|---|
| P1 | `validarLink()` presente na entrada da pagina | **Erro** | `references/padroes-seguranca.md` |
| P2 | `validarPermissao()` presente na entrada da pagina | **Erro** | `references/padroes-seguranca.md` |
| P3 | arquivo sem BOM e compativel com conversao Latin-1 | **Erro** | `AGENTS.md` + `.gitattributes` |
| P4 | links de acao em HTML/JS usam `assinarLink()` | **Erro** | `references/padroes-seguranca.md` |

## Guardrails Locais do Projeto

| ID | Regra | Severidade | Base |
|---|---|---|---|
| P5 | uso confirmado de `$_REQUEST` em pagina | **Erro** | `AGENTS.md` + G5 |
| P6 | `$_GET`/`$_POST` diretos exigem normalizacao explicita | **Erro** em pagina nova, **Aviso** em preexistente | `AGENTS.md` + G5 |
| P7 | UI condicional usa `verificarPermissao()` quando aplicavel | **Aviso** | `references/padroes-seguranca.md` |
| P8 | saida HTML dinamica usa `PaginaSEI::tratarHTML()` ou tratamento documentado | **Erro** em pagina nova, **Aviso** em preexistente | `references/padroes-seguranca.md` + G7 |
| P9 | fonte dinamica alcanca `innerHTML` / `document.write` sem tratamento | **Erro** | hardening web complementar + G7 |
| P10 | mutacao de estado confirmada via GET | **Erro** | hardening complementar + G9 |

P6 e P8 pesam conforme o contexto da acao, informado por `--pagina`:

| Contexto | Quando usar | Efeito em P6 e P8 |
|---|---|---|
| `nova` | a pagina esta sendo criada nesta mudanca | Erro, bloqueia |
| `existente` | a pagina ja existia e esta sendo alterada | Aviso, nao bloqueia |
| flag ausente | contexto da acao nao informado na chamada | equivale a `existente` |

P1 e P2 devem cobrir cada acao e ocorrer nessa ordem. Uma validacao global antes
do `switch` cobre todas as acoes; quando ela nao existe, o auditor verifica cada
`case` que puder extrair. P4 examina todos os links de acao encontrados.

P7 permanece contextual. Em P9, um sink sem fluxo dinamico confirmado gera
`WARN`; fonte dinamica ligada ao sink gera `BLOCK`.

## Referencias Autoritativas

- `references/padroes-seguranca.md` (cobre P1-P10; curado dos cap. 3, 4 e 9 do manual)
- `AGENTS.md`

## Exemplo Aderente ao Manual

```php
try {
    SessaoSEI::getInstance()->validarLink();
    $strAcao = PaginaSEI::GET('acao');
    SessaoSEI::getInstance()->validarPermissao($strAcao);

    if (SessaoSEI::getInstance()->verificarPermissao('md_abc_acao')) {
        $strLink = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_acao');
    }
} catch (Exception $e) {
    PaginaSEI::getInstance()->processarExcecao($e);
}
```

## Como Rodar

Rode sempre sobre as paginas no escopo da acao, nunca sobre a arvore inteira.

```bash
# pagina sendo criada nesta mudanca
python3 audit.py --input md_abc_item_lista.php --pagina nova --format markdown

# pagina que ja existia e esta sendo alterada
python3 audit.py --input md_abc_item_lista.php --pagina existente --format markdown

# varias paginas do mesmo escopo, separadas por virgula
python3 audit.py --input md_abc_item_lista.php,md_abc_item_cadastro.php --pagina existente

# retrato de um modulo inteiro, quando a demanda for revisao e nao alteracao
python3 audit.py --input fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/ --pagina existente
```

Para o retrato de cobertura, rode o auditor no escopo que interessa e leia o resumo.
Nao gravar contagem nesta skill.

## Exit Codes (`--exit-code`)

| Code | Significado |
|---|---|
| 0 | PASS, com ao menos uma pagina analisada |
| 1 | WARN |
| 2 | BLOCK, inclusive entrada inexistente, incompatível, vazia ou sem extracao |

---

## Testes

```bash
cd .agents/skills/sei-verificacao-pagina && python3 -m unittest test_audit
```

10 testes sobre `audit.py`. O arquivo e independente de proposito: nao importa helper de
outra skill nem de pasta compartilhada. A duplicacao de andaime e o preco de a skill
poder ser levada inteira para outro lugar.

Dois deles garantem **fail closed**: entrada inexistente, incompativel, vazia, ou
elegivel da qual o parser nada extraiu, tem de devolver BLOCK. Detector falha verde, e
sem essa garantia o auditor passa por cima do que nao conseguiu ler e ninguem percebe.

O resto se divide em dois grupos. Um fixa que cada regra realmente barra, com o codigo
de saida e a linha certa. O outro impede falso positivo, e cada um desses e um caso que
ja aconteceu. Falso positivo importa porque auditor que grita a toa e desligado pela
equipe, e ai o gate para de proteger tudo, nao so o caso barulhento.

Quatro testes estao com `@unittest.expectedFailure`. Nao estao quebrados: descrevem
capacidade que este `audit.py` nunca implementou, embora a tabela de regras acima a
descreva. Sao P1, P2 e P4 precisando varrer comentario sem estragar string literal,
iterar todo link de acao em vez do primeiro, exigir guard antes da acao e reconhecer
`assinarLink()` quebrado em varias linhas. Ficam marcados para a suite ser sinal em vez
de vermelho permanente; se alguem implementar, o unittest reporta `unexpected success`
e o marcador sai junto.

`test_page_p6_and_p8_severity_follows_action_context` fixa as duas severidades de P6 e
P8 e o padrao aplicado quando a flag nao vem.
