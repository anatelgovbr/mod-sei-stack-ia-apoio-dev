# Apoio a Plano de Trabalho (sigla APT)

O módulo permite que o administrador associe um documento modelo a cada item de etapa de plano de trabalho. Quando um usuário gera documento de editor interno a partir desse item, o conteúdo principal do documento gerado passa a ser o conteúdo principal do modelo.

- Requisitos técnicos: [requisitos-tecnicos.md](requisitos-tecnicos.md)
- Dicionário de dados: [docs/dicionario_dados/apoio-plano-trabalho/](../../dicionario_dados/apoio-plano-trabalho/)
- Instalação e operação: [README do módulo](../../../fontes/sei/src/main/php/sei/web/modulos/apoio-plano-trabalho/README.md)
- Como manter esta documentação: [docs/requisitos-ancorados/README.md](../README.md)

## Regras de negócio

O texto de cada regra está em [regras-de-negocio.md](regras-de-negocio.md).

- Associação
  - RN-APT-001: Um documento modelo por item de etapa
  - RN-APT-003: Permissão por operação
- Documento modelo
  - RN-APT-002: Documento modelo válido

## Requisitos funcionais

- [Associação de documento modelo](requisitos-funcionais/associacao-de-documento-modelo.md): administração das associações entre item de etapa e documento modelo.
- [Geração com documento modelo](requisitos-funcionais/geracao-com-documento-modelo.md): aplicação do conteúdo do modelo ao documento gerado a partir do item de etapa.

## Glossário

| Termo | Definição |
|---|---|
| Plano de trabalho, etapa e item de etapa | Estruturas do SEI que organizam o trabalho em um processo. Um documento pode ser gerado a partir de um item de etapa. |
| Documento modelo | Documento de editor interno já existente no SEI, escolhido pelo administrador do módulo para fornecer o conteúdo dos documentos gerados a partir de um item de etapa. |
| Associação | Ligação entre um item de etapa e um documento modelo, no máximo uma por item, conforme a RN-APT-001. |
| Documento modelo válido | Documento modelo que cumpre as condições da RN-APT-002. |
| Seção principal | Seção do documento de editor interno que guarda o corpo do texto. Cabeçalho e rodapé não são seção principal. |
| Versão vigente | Versão mais recente de uma seção do documento. |
| Administrador do módulo | Usuário com as permissões do módulo, conforme a RN-APT-003. |
| Usuário gerador | Usuário do SEI que gera documento a partir de um item de etapa. |
