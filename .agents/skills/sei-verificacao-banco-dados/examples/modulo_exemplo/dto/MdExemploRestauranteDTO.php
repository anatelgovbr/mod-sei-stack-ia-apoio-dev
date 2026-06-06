<?php
/**
 * @table Restaurantes participantes do programa de alimentacao institucional
 * @column sin_ativo S=Ativo, N=Inativo
 */
class MdExemploRestauranteDTO extends InfraDTO {

    public function getStrNomeTabela() {
        return "md_exemplo_restaurante";
    }

    public function montarDTO() {

        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, "IdRestaurante", "id_md_exemplo_restaurante");
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, "Nome", "nome");
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, "Endereco", "endereco");
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, "SinAtivo", "sin_ativo");

        $this->configurarPK("IdRestaurante", InfraDTO::$TIPO_PK_NATIVA);
        $this->configurarExclusaoLogica("SinAtivo", "N");
    }
}