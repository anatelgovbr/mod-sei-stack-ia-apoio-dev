# Registro de adaptadores

Consulte este registro para localizar alvos reconhecidos nesta instalação. A distribuição agnóstica começa sem adaptadores de sistemas; crie e registre os adaptadores no repositório de uso conforme o [contrato](references/contrato-de-adaptador.md).

| Alvo | Arquivo | Reconhecimento e alcance |
|---|---|---|
| Módulo SEI Apoio a Plano de Trabalho (APT) | [adapters/sei-modulo-apt.md](adapters/sei-modulo-apt.md) | Pasta `fontes/sei/src/main/php/sei/web/modulos/apoio-plano-trabalho/`, classe `MdAptIntegracao`, prefixo `md_apt_` e parâmetro `VERSAO_MODULO_APT`. Alcance: associação de documento modelo a item de etapa e geração de documento a partir do item |
| Núcleo do SEI para desenvolvimento de módulos | [adapters/sei-nucleo-desenvolvimento.md](adapters/sei-nucleo-desenvolvimento.md) | Classe `SeiIntegracao` e constante `SEI_VERSAO` em `fontes/sei/src/main/php/sei/web/`, classes de `sei/web/api/`, `SeiRN` e InfraPHP, fora de `sei/web/modulos/`. Alcance: manual de desenvolvimento de módulos SEI em `docs/manuais/sei/` |
| Módulo SEI IA | [adapters/sei-modulo-ia.md](adapters/sei-modulo-ia.md) | Pasta `fontes/sei/src/main/php/sei/web/modulos/ia/`, classe `IaIntegracao`, prefixo `md_ia_` e parâmetro `VERSAO_MODULO_IA`. Alcance: Administração do módulo pelo Administrador geral do SEI e funcionalidades de processo/documento e Assistente pelo Usuário interno com perfil Básico; versão alvo 1.5.0, publicação em `docs/manuais/ia/`. Manuais existentes: `manual-sei-ia-administracao.md` e `manual-sei-ia-usuario.md`, cada um com sua pasta `imagens-<slug>`. O manual de Usuário e suas 32 imagens são material pré-existente fornecido pelo responsável; registro não implica revisão funcional |
