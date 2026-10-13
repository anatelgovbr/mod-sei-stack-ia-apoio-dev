# Pedidos, sistema fictício

Fontes correntes: `src/sistema.py` e `schema.sql`. O snapshot anterior identificado como v1 está em `historico/v1/`; não é histórico Git nem comprovação de implantação. Os descritores `MENUS` e `TELAS` dão nomes visíveis, campos e navegação. `apresentar`, `operar` e `acionar_tela` conectam perfil, apresentação, regra, entidade e mensagem visível. O schema representa a persistência do objeto; `auditoria_interna` não aparece na UI.

O Administrador configura o serviço, o Interno analisa pedidos e o Externo registra, consulta e acompanha pedidos. São perfis de acesso; a escolha do público de cada manual é do responsável. A versão vem de `VERSAO`. Toda a UI é em português brasileiro, UTF-8. A logo fictícia aprovada é `recursos/logo.svg`. Destino padrão: `docs/manuais/`, Markdown puro para GitHub Flavored Markdown, imagens em `imagens-<slug>/`. Não há capturas, aplicação navegável nem autorização externa.
