<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcProjetoDTO extends InfraDTO
{
  public function getStrNomeTabela(): ?string
  {
    return 'md_abc_projeto';
  }

  /**
   * @throws InfraException
   */
  public function montar(): void
  {
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcProjeto', 'id_md_abc_projeto');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Identificacao', 'identificacao');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Descricao', 'descricao');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_DTA, 'Cadastramento', 'dta_cadastramento');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'SinAtivo', 'sin_ativo');


    $this->configurarPK('IdMdAbcProjeto', InfraDTO::$TIPO_PK_SEQUENCIAL);

    $this->configurarExclusaoLogica('SinAtivo', 'N');

  }
}
