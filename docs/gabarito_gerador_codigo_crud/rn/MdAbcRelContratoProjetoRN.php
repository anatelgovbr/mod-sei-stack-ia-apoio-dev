<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

/**
 * @method MdAbcRelContratoProjetoDTO cadastrar(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO)
 * @method MdAbcRelContratoProjetoDTO[] listar(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO)
 * @method MdAbcRelContratoProjetoDTO|null consultar(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO)
 * @method MdAbcRelContratoProjetoDTO|null bloquear(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO)
 * @method void alterar(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO)
 * @method void excluir(MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO)
 * @method void desativar(MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO)
 * @method void reativar(MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO)
 */
class MdAbcRelContratoProjetoRN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return Bancoabc::getInstance();
  }

  private function validarNumIdMdAbcContrato(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato())) {
      $objInfraException->adicionarValidacao('Contrato não informadC.');
    }
  }

  private function validarNumIdMdAbcProjeto(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto())) {
      $objInfraException->adicionarValidacao('Projeto não informadP.');
    }
  }

  private function validarDtaAssociacao(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcRelContratoProjetoDTO->getDtaAssociacao())) {
      $objInfraException->adicionarValidacao('Data de Associação não informadD.');
    } elseif (!InfraData::validarData($objMdAbcRelContratoProjetoDTO->getDtaAssociacao())) {
      $objInfraException->adicionarValidacao('Data de Associação inválidD.');
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO
   * @return MdAbcRelContratoProjetoDTO
   * @throws InfraException
   */
  protected function cadastrarControlado(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO): MdAbcRelContratoProjetoDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_cadastrar', __METHOD__, $objMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      $this->validarNumIdMdAbcContrato($objMdAbcRelContratoProjetoDTO, $objInfraException);
      $this->validarNumIdMdAbcProjeto($objMdAbcRelContratoProjetoDTO, $objInfraException);
      $this->validarDtaAssociacao($objMdAbcRelContratoProjetoDTO, $objInfraException);

      $objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjetoBD->cadastrar($objMdAbcRelContratoProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_alterar', __METHOD__, $objMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      if ($objMdAbcRelContratoProjetoDTO->isSetNumIdMdAbcContrato()) {
        $this->validarNumIdMdAbcContrato($objMdAbcRelContratoProjetoDTO, $objInfraException);
      }

      if ($objMdAbcRelContratoProjetoDTO->isSetNumIdMdAbcProjeto()) {
        $this->validarNumIdMdAbcProjeto($objMdAbcRelContratoProjetoDTO, $objInfraException);
      }

      if ($objMdAbcRelContratoProjetoDTO->isSetDtaAssociacao()) {
        $this->validarDtaAssociacao($objMdAbcRelContratoProjetoDTO, $objInfraException);
      }


      $objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      $objMdAbcRelContratoProjetoBD->alterar($objMdAbcRelContratoProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObjMdAbcRelContratoProjetoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_excluir', __METHOD__, $arrObjMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcRelContratoProjetoDTO as $objMdAbcRelContratoProjetoDTO) {
        $objMdAbcRelContratoProjetoBD->excluir($objMdAbcRelContratoProjetoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO
   * @return MdAbcRelContratoProjetoDTO|null
   * @throws InfraException
   */
  protected function consultarConectado(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO): ?MdAbcRelContratoProjetoDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_consultar', __METHOD__, $objMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjetoBD->consultar($objMdAbcRelContratoProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO
   * @return MdAbcRelContratoProjetoDTO[]
   * @throws InfraException
   */
  protected function listarConectado(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO): array
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_listar', __METHOD__, $objMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjetoBD->listar($objMdAbcRelContratoProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando Associações.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO): int
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_listar', __METHOD__, $objMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcRelContratoProjetoBD->contar($objMdAbcRelContratoProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando Associação.', $e);
    }
  }

  /**
   * @param MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO
   * @return void
   * @throws InfraException
   */
/*   protected function desativarControlado(array $arrObjMdAbcRelContratoProjetoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_desativar', __METHOD__, $arrObjMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcRelContratoProjetoDTO as $objMdAbcRelContratoProjetoDTO) {
        $objMdAbcRelContratoProjetoBD->desativar($objMdAbcRelContratoProjetoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro desativando Associação.', $e);
    }
  }
 */
  /**
   * @param MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO
   * @return void
   * @throws InfraException
   */
/*   protected function reativarControlado(array $arrObjMdAbcRelContratoProjetoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_reativar', __METHOD__, $arrObjMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcRelContratoProjetoDTO as $objMdAbcRelContratoProjetoDTO) {
        $objMdAbcRelContratoProjetoBD->reativar($objMdAbcRelContratoProjetoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro reativando Associação.', $e);
    }
  }
 */
  /**
   * @param  MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO
   * @return MdAbcRelContratoProjetoDTO|null
   * @throws InfraException
   */
/*   protected function bloquearConectado(MdAbcRelContratoProjetoDTO $objMdAbcRelContratoProjetoDTO): ?MdAbcRelContratoProjetoDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_rel_contrato_projeto_consultar', __METHOD__, $objMdAbcRelContratoProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcRelContratoProjetoBD = new MdAbcRelContratoProjetoBD($this->getObjInfraIBanco());

      return $objMdAbcRelContratoProjetoBD->bloquear($objMdAbcRelContratoProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro bloqueando Associação.', $e);
    }
  } */
}
