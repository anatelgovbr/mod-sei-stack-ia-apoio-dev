<?php

require_once dirname(__FILE__) . '/../../../SEI.php';

/**
 * @method {{CLASS_NAME}}DTO cadastrar({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO)
 * @method {{CLASS_NAME}}DTO[] listar({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO)
 * @method {{CLASS_NAME}}DTO|null consultar({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO)
 * @method {{CLASS_NAME}}DTO|null bloquear({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO)
 * @method void alterar({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO)
 * @method void excluir({{CLASS_NAME}}DTO[] $arrObj{{CLASS_NAME}}DTO)
{{DOCBLOCK_LOGICAL_DELETE_METHODS}}
 */
class {{CLASS_NAME}}RN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return BancoSEI::getInstance();
  }

{{VALIDATOR_METHODS}}

  // cadastrarControlado always runs unconditional validators.

  /**
   * @param {{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO
   * @return {{CLASS_NAME}}DTO
   * @throws InfraException
   */
  protected function cadastrarControlado({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO): {{CLASS_NAME}}DTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('{{TABLE_NAME}}_cadastrar', __METHOD__, $obj{{CLASS_NAME}}DTO);

      $objInfraException = new InfraException();

      // For FK fields, render required checks such as validarNumId...().
{{CREATE_VALIDATION_LINES}}
      $objInfraException->lancarValidacoes();

      $obj{{CLASS_NAME}}BD = new {{CLASS_NAME}}BD($this->getObjInfraIBanco());
      return $obj{{CLASS_NAME}}BD->cadastrar($obj{{CLASS_NAME}}DTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando {{ENTITY_LABEL_SINGULAR}}.', $e);
    }
  }

  /**
   * @param {{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('{{TABLE_NAME}}_alterar', __METHOD__, $obj{{CLASS_NAME}}DTO);

      $objInfraException = new InfraException();

      // alterarControlado uses isSet*() guards, including FK fields.
{{UPDATE_VALIDATION_LINES}}
      $objInfraException->lancarValidacoes();

      $obj{{CLASS_NAME}}BD = new {{CLASS_NAME}}BD($this->getObjInfraIBanco());
      $obj{{CLASS_NAME}}BD->alterar($obj{{CLASS_NAME}}DTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando {{ENTITY_LABEL_SINGULAR}}.', $e);
    }
  }

  /**
   * @param {{CLASS_NAME}}DTO[] $arrObj{{CLASS_NAME}}DTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObj{{CLASS_NAME}}DTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('{{TABLE_NAME}}_excluir', __METHOD__, $arrObj{{CLASS_NAME}}DTO);

      $obj{{CLASS_NAME}}BD = new {{CLASS_NAME}}BD($this->getObjInfraIBanco());
      foreach ($arrObj{{CLASS_NAME}}DTO as $obj{{CLASS_NAME}}DTO) {
        $obj{{CLASS_NAME}}BD->excluir($obj{{CLASS_NAME}}DTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo {{ENTITY_LABEL_SINGULAR}}.', $e);
    }
  }

  /**
   * @param {{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO
   * @return {{CLASS_NAME}}DTO|null
   * @throws InfraException
   */
  protected function consultarConectado({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO): ?{{CLASS_NAME}}DTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('{{TABLE_NAME}}_listar', __METHOD__, $obj{{CLASS_NAME}}DTO);

      $obj{{CLASS_NAME}}BD = new {{CLASS_NAME}}BD($this->getObjInfraIBanco());
      return $obj{{CLASS_NAME}}BD->consultar($obj{{CLASS_NAME}}DTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando {{ENTITY_LABEL_SINGULAR}}.', $e);
    }
  }

  /**
   * @param {{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO
   * @return {{CLASS_NAME}}DTO[]
   * @throws InfraException
   */
  protected function listarConectado({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO): array
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('{{TABLE_NAME}}_listar', __METHOD__, $obj{{CLASS_NAME}}DTO);

      $obj{{CLASS_NAME}}BD = new {{CLASS_NAME}}BD($this->getObjInfraIBanco());
      return $obj{{CLASS_NAME}}BD->listar($obj{{CLASS_NAME}}DTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando {{ENTITY_LABEL_PLURAL}}.', $e);
    }
  }

  /**
   * @param {{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado({{CLASS_NAME}}DTO $obj{{CLASS_NAME}}DTO): int
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('{{TABLE_NAME}}_listar', __METHOD__, $obj{{CLASS_NAME}}DTO);

      $obj{{CLASS_NAME}}BD = new {{CLASS_NAME}}BD($this->getObjInfraIBanco());
      return $obj{{CLASS_NAME}}BD->contar($obj{{CLASS_NAME}}DTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando {{ENTITY_LABEL_SINGULAR}}.', $e);
    }
  }

  // Render desativarControlado(), reativarControlado(), and bloquearConectado()
  // here. Keep them active when sin_ativo exists and commented when it does not;
  // md_abc_aquisicao is the reference fixture for this commented form.
{{LOGICAL_DELETE_METHODS_BLOCK}}
}
