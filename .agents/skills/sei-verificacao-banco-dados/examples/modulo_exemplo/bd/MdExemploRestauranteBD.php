<?php
require_once dirname(__FILE__) . '/../../../infra/infra_php/infra.php';

class MdExemploRestauranteBD extends InfraBD {

    public function __construct($objInfraIBanco) {
        parent::__construct($objInfraIBanco);
    }

    protected function getVersao() {
        return '1.0.0';
    }
}