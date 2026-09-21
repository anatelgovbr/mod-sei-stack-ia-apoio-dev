<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

/**
 * @method MdAbcRelContratoProjDTO cadastrar(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO)
 * @method MdAbcRelContratoProjDTO[] listar(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO)
 * @method MdAbcRelContratoProjDTO|null consultar(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO)
 * @method MdAbcRelContratoProjDTO|null bloquear(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO)
 * @method void alterar(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO)
 * @method void excluir(MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO)
 * @method void desativar(MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO)
 * @method void reativar(MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO)
 */
class MdAbcRelContratoProjRN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return BancoSEI::getInstance();
  }

  private function validarNumIdMdAbcContrato(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato())) {
      $objInfraException->adicionarValidacao('Contrato não informado.');
    }
  }

  private function validarNumIdMdAbcProjeto(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto())) {
      $objInfraException->adicionarValidacao('Projeto não informado.');
    }
  }

  private function validarDtaAssociacao(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcRelContratoProjDTO->getDtaAssociacao())) {
      $objInfraException->adicionarValidacao('Data de Associação não informado.');
    } elseif (!InfraData::validarData($objMdAbcRelContratoProjDTO->getDtaAssociacao())) {
      $objInfraException->adicionarValidacao('Data de Associação inválida.');
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO
   * @return MdAbcRelContratoProjDTO
   * @throws InfraException
   */
  protected function cadastrarControlado(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO): MdAbcRelContratoProjDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_cadastrar', __METHOD__, $objMdAbcRelContratoProjDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      $this->validarNumIdMdAbcContrato($objMdAbcRelContratoProjDTO, $objInfraException);
      $this->validarNumIdMdAbcProjeto($objMdAbcRelContratoProjDTO, $objInfraException);
      $this->validarDtaAssociacao($objMdAbcRelContratoProjDTO, $objInfraException);

      $objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjBD->cadastrar($objMdAbcRelContratoProjDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_alterar', __METHOD__, $objMdAbcRelContratoProjDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      if ($objMdAbcRelContratoProjDTO->isSetNumIdMdAbcContrato()) {
        $this->validarNumIdMdAbcContrato($objMdAbcRelContratoProjDTO, $objInfraException);
      }

      if ($objMdAbcRelContratoProjDTO->isSetNumIdMdAbcProjeto()) {
        $this->validarNumIdMdAbcProjeto($objMdAbcRelContratoProjDTO, $objInfraException);
      }

      if ($objMdAbcRelContratoProjDTO->isSetDtaAssociacao()) {
        $this->validarDtaAssociacao($objMdAbcRelContratoProjDTO, $objInfraException);
      }


      $objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      $objMdAbcRelContratoProjBD->alterar($objMdAbcRelContratoProjDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObjMdAbcRelContratoProjDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_excluir', __METHOD__, $arrObjMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcRelContratoProjDTO as $objMdAbcRelContratoProjDTO) {
        $objMdAbcRelContratoProjBD->excluir($objMdAbcRelContratoProjDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO
   * @return MdAbcRelContratoProjDTO|null
   * @throws InfraException
   */
  protected function consultarConectado(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO): ?MdAbcRelContratoProjDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_consultar', __METHOD__, $objMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjBD->consultar($objMdAbcRelContratoProjDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO
   * @return MdAbcRelContratoProjDTO[]
   * @throws InfraException
   */
  protected function listarConectado(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO): array
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_listar', __METHOD__, $objMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjBD->listar($objMdAbcRelContratoProjDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando Associações.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO): int
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_listar', __METHOD__, $objMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjBD->contar($objMdAbcRelContratoProjDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO
   * @return void
   * @throws InfraException
   */
/*   protected function desativarControlado(array $arrObjMdAbcRelContratoProjDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_desativar', __METHOD__, $arrObjMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcRelContratoProjDTO as $objMdAbcRelContratoProjDTO) {
        $objMdAbcRelContratoProjBD->desativar($objMdAbcRelContratoProjDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro desativando Associação.', $e);
    }
  }
 */
  /**
   * @param MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO
   * @return void
   * @throws InfraException
   */
/*   protected function reativarControlado(array $arrObjMdAbcRelContratoProjDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_reativar', __METHOD__, $arrObjMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcRelContratoProjDTO as $objMdAbcRelContratoProjDTO) {
        $objMdAbcRelContratoProjBD->reativar($objMdAbcRelContratoProjDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro reativando Associação.', $e);
    }
  }
 */
  /**
   * @param  MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO
   * @return MdAbcRelContratoProjDTO|null
   * @throws InfraException
   */
/*   protected function bloquearConectado(MdAbcRelContratoProjDTO $objMdAbcRelContratoProjDTO): ?MdAbcRelContratoProjDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_proj_consultar', __METHOD__, $objMdAbcRelContratoProjDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjBD = new MdAbcRelContratoProjBD($this->getObjInfraIBanco());

      return $objMdAbcRelContratoProjBD->bloquear($objMdAbcRelContratoProjDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro bloqueando Associação.', $e);
    }
  } */
}
