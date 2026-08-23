<?php

try {
    SessaoSEI::getInstance()->validarLink();
    SessaoSEI::getInstance()->validarPermissao('md_rt_exemplo_listar');
    $numId = PaginaSEI::GET('id', 'int');
} catch (Exception $objErro) {
    PaginaSEI::getInstance()->processarExcecao($objErro);
}
