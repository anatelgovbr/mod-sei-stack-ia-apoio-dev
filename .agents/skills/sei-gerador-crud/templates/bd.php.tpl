<?php

require_once dirname(__FILE__) . '/../../../SEI.php';

class {{CLASS_NAME}}BD extends InfraBD
{
  public function __construct(InfraIBanco $objInfraIBanco)
  {
    parent::__construct($objInfraIBanco);
  }
}
