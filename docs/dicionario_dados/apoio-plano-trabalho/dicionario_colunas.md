# Dicionário de Dados do Módulo SEI Apoio a Plano de Trabalho - v1.0.0

## Índice de Tabelas

- [md_apt_etapa_pl_doc_modelo](#md_apt_etapa_pl_doc_modelo)

## md_apt_etapa_pl_doc_modelo

Representa a associação entre um item de etapa de plano de trabalho e um documento modelo de editor interno, com uma linha para cada item de etapa associado a um documento modelo. O registro é criado ou passa a integrar o conjunto quando um item de etapa recebe um documento modelo de editor interno. Inclui o item de etapa e o documento modelo e exclui o conteúdo do documento, os demais atributos do item de etapa e associações adicionais para o mesmo item. Mantém a associação cadastrada referente ao item de etapa e ao documento modelo selecionados. É produzido a partir da configuração administrativa dos itens de etapa e utilizado pela geração de documentos de editor interno originados de planos de trabalho. Não deve ser interpretado ou utilizado como o item de etapa, o documento modelo ou o conteúdo do documento.

| Tabela | Coluna | Descrição |
|---|---|---|
| md_apt_etapa_pl_doc_modelo | id_md_apt_etapa_pl_doc_modelo | Identificador da associação entre um item de etapa de plano de trabalho e um documento modelo de editor interno, correspondente à identificação técnica única do registro de associação, determinado na criação da associação. É expresso em referência numérica inteira e obtido pela geração sequencial do identificador. O valor nulo não se aplica, pois a identificação é chave primária e obrigatória. É utilizado para localizar, alterar ou excluir a associação e não representa o item de etapa, o documento modelo ou o conteúdo do documento. |
| md_apt_etapa_pl_doc_modelo | id_documento | Identificador do documento modelo de editor interno, correspondente à referência ao documento do sistema associado ao item de etapa, determinado na seleção do protocolo de documento modelo. É expresso em referência numérica de maior capacidade e obtido pela validação e associação do documento selecionado. O valor nulo não se aplica, pois a referência é obrigatória. É utilizado para localizar o conteúdo e os metadados do documento modelo na geração do documento e não representa o conteúdo do documento nem o protocolo formatado. |
| md_apt_etapa_pl_doc_modelo | id_item_etapa | Identificador do item de etapa de plano de trabalho, correspondente à referência ao item que recebe a associação do documento modelo, determinado na configuração administrativa da associação. É expresso em referência numérica inteira e obtido pela seleção do item de etapa. O valor nulo não se aplica, pois a referência é obrigatória. É utilizado para limitar uma associação de documento modelo por item e para localizar a associação durante a geração de documentos e não representa a etapa de trabalho ou o plano de trabalho. |

