# Registro de adaptadores

Consulte este registro para localizar alvos reconhecidos nesta instalação. A distribuição agnóstica começa sem adaptadores de sistemas; crie e registre os adaptadores no repositório de uso conforme o [contrato](references/contrato-de-adaptador.md).

| Alvo | Arquivo | Reconhecimento e alcance |
|---|---|---|
| Módulo SEI Apoio a Plano de Trabalho (APT) | [adapters/sei-modulo-apt.md](adapters/sei-modulo-apt.md) | Pasta `fontes/sei/src/main/php/sei/web/modulos/apoio-plano-trabalho/`, classe `MdAptIntegracao`, prefixo `md_apt_` e parâmetro `VERSAO_MODULO_APT`. Alcance: associação de documento modelo a item de etapa e geração de documento a partir do item |
| Núcleo do SEI para desenvolvimento de módulos | [adapters/sei-nucleo-desenvolvimento.md](adapters/sei-nucleo-desenvolvimento.md) | Classe `SeiIntegracao` e constante `SEI_VERSAO` em `fontes/sei/src/main/php/sei/web/`, classes de `sei/web/api/`, `SeiRN` e InfraPHP, fora de `sei/web/modulos/`. Alcance: manual de desenvolvimento de módulos SEI em `docs/manuais/sei/` |
