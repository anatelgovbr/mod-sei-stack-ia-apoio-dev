# Overlay de módulo: PEN

Overlay exclusivo de PEN, Tramita GOV.BR ou `sei/web/modulos/pen/`. Herda `padrao.md` e substitui somente os itens abaixo.

## Fontes e conflito de versão

Busque integração e scripts PEN em `sei/scripts/` e `sip/scripts/`; inclua os candidatos `sip_atualizar_versao_modulo_pen.php`, `mod-pen/sip_atualizar_versao_modulo_pen.php` e `mod-pen/sei_atualizar_versao_modulo_pen.php`. Compare todas as linhas encontradas. Sem precedência declarada para versões ou estruturas divergentes, reporte cada leitura e bloqueie escrita até o desenvolvedor escolher a linha vigente.

## Gramática e extração

- O script SEI usa `switch` com queda intencional e chamadas `instalarV...()` com `V` maiúsculo.
- Preserve todo sufixo de pré-release encontrado no `case`.
- `versao_0_0_0` pertence ao controlador de compatibilidade e não substitui o `switch` estrutural.
- Este overlay amplia a gramática comum para sufixo de pré-release: use `^v[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$` no `formato` e `^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$` no `changelog`. Ordene pelo fluxo e pelo histórico do script, com cada pré-release antes da versão final correspondente.

## API estrutural PEN

`fontes/sei/src/main/php/sei/web/modulos/pen/bd/PenMetaBD.php` é definição estrutural aplicável obrigatória apenas neste alvo. Reconheça `criarTabela`, `removerTabela`, `adicionarValorPadraoParaColuna`, `adicionarChaveUnica`, renomeações de tabela e coluna, `NNULLO` e `SNULLO`, além das operações herdadas de `InfraMetaBD`.

Quando encontrado, trate `InfraSequencia::criarSequencia` como criação de sequência somente no bloco em que ocorrer. Não promova `PenMetaBD` nem suas convenções para outros adaptadores.

## Camadas e busca

Inclua `bd/PenMetaBD.php` na definição estrutural, não em consulta e projeção. `bd/PenParametroBD.php` e demais BD entram em consulta apenas quando contiverem leitura. Exclua `vendor/` e `composer.json` da evidência semântica, salvo referência direta do código do módulo.

## Bloqueios adicionais

- Linhas de script duplicadas ou versões divergentes: bloqueie escrita e validações dependentes da versão até decisão de precedência; permita verificação parcial no alcance comprovado.
- Determine baseline e alcance somente após escolher a linha vigente.
