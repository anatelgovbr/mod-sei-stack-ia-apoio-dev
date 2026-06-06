<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

/**
 * @method MdAbcContratoDTO cadastrar(MdAbcContratoDTO $objMdAbcContratoDTO)
 * @method MdAbcContratoDTO[] listar(MdAbcContratoDTO $objMdAbcContratoDTO)
 * @method MdAbcContratoDTO|null consultar(MdAbcContratoDTO $objMdAbcContratoDTO)
 * @method MdAbcContratoDTO|null bloquear(MdAbcContratoDTO $objMdAbcContratoDTO)
 * @method void alterar(MdAbcContratoDTO $objMdAbcContratoDTO)
 * @method void excluir(MdAbcContratoDTO[] $arrObjMdAbcContratoDTO)
 * @method void desativar(MdAbcContratoDTO[] $arrObjMdAbcContratoDTO)
 * @method void reativar(MdAbcContratoDTO[] $arrObjMdAbcContratoDTO)
 */
class MdAbcContratoRN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return Bancoabc::getInstance();
  }

  private function validarNumIdMdAbcAquisicao(MdAbcContratoDTO $objMdAbcContratoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcContratoDTO->getNumIdMdAbcAquisicao())) {
      $objInfraException->adicionarValidacao('Aquisição não informadA.');
    }
  }

  private function validarStrNumero(MdAbcContratoDTO $objMdAbcContratoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcContratoDTO->getStrNumero())) {
      $objInfraException->adicionarValidacao('Número não informadN.');
    } else {
      $objMdAbcContratoDTO->setStrNumero(trim($objMdAbcContratoDTO->getStrNumero()));
      if (strlen($objMdAbcContratoDTO->getStrNumero())>20) {
        $objInfraException->adicionarValidacao('Número possui tamanho superior a 20 caracteres.');
      }
    }
  }

  private function validarDtaAssinatura(MdAbcContratoDTO $objMdAbcContratoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcContratoDTO->getDtaAssinatura())) {
      $objInfraException->adicionarValidacao('Data de Assinatura não informadD.');
    } elseif (!InfraData::validarData($objMdAbcContratoDTO->getDtaAssinatura())) {
      $objInfraException->adicionarValidacao('Data de Assinatura inválidD.');
    }
  }

  private function validarDinValor(MdAbcContratoDTO $objMdAbcContratoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcContratoDTO->getDinValor())) {
      $objInfraException->adicionarValidacao('Valor não informadV.');
    }
  }

  private function validarStrObservacao(MdAbcContratoDTO $objMdAbcContratoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcContratoDTO->getStrObservacao())) {
      $objMdAbcContratoDTO->setStrObservacao(null);
    } else {
      $objMdAbcContratoDTO->setStrObservacao(trim($objMdAbcContratoDTO->getStrObservacao()));
      if (strlen($objMdAbcContratoDTO->getStrObservacao())>500) {
        $objInfraException->adicionarValidacao('Observação possui tamanho superior a 500 caracteres.');
      }
    }
  }

  /**
   * @param MdAbcContratoDTO $objMdAbcContratoDTO
   * @return MdAbcContratoDTO
   * @throws InfraException
   */
  protected function cadastrarControlado(MdAbcContratoDTO $objMdAbcContratoDTO): MdAbcContratoDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_cadastrar', __METHOD__, $objMdAbcContratoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      $this->validarNumIdMdAbcAquisicao($objMdAbcContratoDTO, $objInfraException);
      $this->validarStrNumero($objMdAbcContratoDTO, $objInfraException);
      $this->validarDtaAssinatura($objMdAbcContratoDTO, $objInfraException);
      $this->validarDinValor($objMdAbcContratoDTO, $objInfraException);
      $this->validarStrObservacao($objMdAbcContratoDTO, $objInfraException);

      $objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      return $objMdAbcContratoBD->cadastrar($objMdAbcContratoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando Contrato.', $e);
    }
  }

  /**
   * @param MdAbcContratoDTO $objMdAbcContratoDTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado(MdAbcContratoDTO $objMdAbcContratoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_alterar', __METHOD__, $objMdAbcContratoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      if ($objMdAbcContratoDTO->isSetNumIdMdAbcAquisicao()) {
        $this->validarNumIdMdAbcAquisicao($objMdAbcContratoDTO, $objInfraException);
      }

      if ($objMdAbcContratoDTO->isSetStrNumero()) {
        $this->validarStrNumero($objMdAbcContratoDTO, $objInfraException);
      }

      if ($objMdAbcContratoDTO->isSetDtaAssinatura()) {
        $this->validarDtaAssinatura($objMdAbcContratoDTO, $objInfraException);
      }

      if ($objMdAbcContratoDTO->isSetDinValor()) {
        $this->validarDinValor($objMdAbcContratoDTO, $objInfraException);
      }

      if ($objMdAbcContratoDTO->isSetStrObservacao()) {
        $this->validarStrObservacao($objMdAbcContratoDTO, $objInfraException);
      }


      $objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      $objMdAbcContratoBD->alterar($objMdAbcContratoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando Contrato.', $e);
    }
  }

  /**
   * @param MdAbcContratoDTO[] $arrObjMdAbcContratoDTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObjMdAbcContratoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_excluir', __METHOD__, $arrObjMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcContratoDTO as $objMdAbcContratoDTO) {
        $objMdAbcContratoBD->excluir($objMdAbcContratoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo Contrato.', $e);
    }
  }

  /**
   * @param MdAbcContratoDTO $objMdAbcContratoDTO
   * @return MdAbcContratoDTO|null
   * @throws InfraException
   */
  protected function consultarConectado(MdAbcContratoDTO $objMdAbcContratoDTO): ?MdAbcContratoDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_consultar', __METHOD__, $objMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      return $objMdAbcContratoBD->consultar($objMdAbcContratoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando Contrato.', $e);
    }
  }

  /**
   * @param MdAbcContratoDTO $objMdAbcContratoDTO
   * @return MdAbcContratoDTO[]
   * @throws InfraException
   */
  protected function listarConectado(MdAbcContratoDTO $objMdAbcContratoDTO): array
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_listar', __METHOD__, $objMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      return $objMdAbcContratoBD->listar($objMdAbcContratoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando Contratos.', $e);
    }
  }

  /**
   * @param MdAbcContratoDTO $objMdAbcContratoDTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado(MdAbcContratoDTO $objMdAbcContratoDTO): int
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_listar', __METHOD__, $objMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      return $objMdAbcContratoBD->contar($objMdAbcContratoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando Contrato.', $e);
    }
  }

  /**
   * @param MdAbcContratoDTO[] $arrObjMdAbcContratoDTO
   * @return void
   * @throws InfraException
   */
/*   protected function desativarControlado(array $arrObjMdAbcContratoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_desativar', __METHOD__, $arrObjMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcContratoDTO as $objMdAbcContratoDTO) {
        $objMdAbcContratoBD->desativar($objMdAbcContratoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro desativando Contrato.', $e);
    }
  }
 */
  /**
   * @param MdAbcContratoDTO[] $arrObjMdAbcContratoDTO
   * @return void
   * @throws InfraException
   */
/*   protected function reativarControlado(array $arrObjMdAbcContratoDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_reativar', __METHOD__, $arrObjMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcContratoDTO as $objMdAbcContratoDTO) {
        $objMdAbcContratoBD->reativar($objMdAbcContratoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro reativando Contrato.', $e);
    }
  }
 */
  /**
   * @param  MdAbcContratoDTO $objMdAbcContratoDTO
   * @return MdAbcContratoDTO|null
   * @throws InfraException
   */
/*   protected function bloquearConectado(MdAbcContratoDTO $objMdAbcContratoDTO): ?MdAbcContratoDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_contrato_consultar', __METHOD__, $objMdAbcContratoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcContratoBD = new MdAbcContratoBD($this->getObjInfraIBanco());

      return $objMdAbcContratoBD->bloquear($objMdAbcContratoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro bloqueando Contrato.', $e);
    }
  } */
}
