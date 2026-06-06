<?php

require_once dirname(__FILE__) . '/../../../SEI.php';

class {{CLASS_NAME}}INT extends InfraINT
{
  // Render one or more helpers such as montarSelectIdentificacao(...) or
  // montarSelectDescricao(..., $numIdMdAbcProjeto='') depending on the fixture.
  // FK-aware helpers accept the parent id parameter and filter before listar().
{{INT_METHODS}}
}
