<?php

require_once dirname(__FILE__) . '/../../../SEI.php';

class {{CLASS_NAME}}DTO extends InfraDTO
{
  public function getStrNomeTabela(): ?string
  {
    return '{{TABLE_NAME}}';
  }

  /**
   * @throws InfraException
   */
  public function montar(): void
  {
{{DTO_ATTRIBUTE_LINES}}
    // Render one adicionarAtributoTabelaRelacionada(...) per FK when applicable.
{{RELATED_ATTRIBUTE_LINES}}
    $this->configurarPK('{{PK_ATTRIBUTE_NAME}}', InfraDTO::$TIPO_PK_NATIVA);
    // Keep this line only when the entity has sin_ativo; omit it entirely when using the canonical no-sin_ativo path.
{{LOGICAL_DELETE_CONFIG_LINE}}
  }
}
