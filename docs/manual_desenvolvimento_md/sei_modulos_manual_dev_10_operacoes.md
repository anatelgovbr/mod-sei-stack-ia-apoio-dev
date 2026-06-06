# 10. Operações

Os módulos podem realizar operações no sistema, como geração de processos, inclusão de documentos e atualização de andamentos, utilizando os objetos da API em conjunto com os métodos disponibilizados na classe SeiRN. A camada de Web Services do SEI também utiliza a API, sendo assim, todas as operações realizadas por meio de Web Services também podem ser realizadas diretamente pelos módulos.

- **Atenção**: Não é recomendado o uso de outras classes ou objetos
    internos do sistema.
- Eventuais alterações nos objetos da API e métodos da classe
    SeiRN serão documentadas em um roteiro de adaptação para os
    módulos. Alterações em outros componentes internos do sistema não
    serão documentadas.

Sempre que uma operação possuir opção de uso do ID interno ou do número de protocolo deve-se optar pelo ID, caso a informação esteja disponível, pois isso evitará um ou mais acessos ao banco.

## adicionarArquivo

| **Entrada** |
|---|
| Instância do objeto EntradaAdicionarArquivoAPI preenchida com:<br><ul><li>Nome</li><li>Tamanho</li><li>Hash</li><li>Conteudo</li></ul> |
| **Saída** |
| Retornar o identificador do arquivo criado no repositório. |

**Exemplo:**

```php
$strArquivo = DIR_SEI_TEMP.'/exemplo.pdf';
$fp = fopen($strArquivo, "rb");

$objEntradaAdicionarArquivoAPI = new EntradaAdicionarArquivoAPI();
$objEntradaAdicionarArquivoAPI->setNome('exemplo.pdf');
$objEntradaAdicionarArquivoAPI->setTamanho(filesize($strArquivo));
$objEntradaAdicionarArquivoAPI->setHash(md5_file($strArquivo));
$objEntradaAdicionarArquivoAPI->setConteudo(base64_encode(fread($fp, 1024*1024))); //blocos de 1Mb

$objSeiRN = new SeiRN();
$numIdArquivo = $objSeiRN->adicionarArquivo($objEntradaAdicionarArquivoAPI);
while (!feof($fp)) {
  $objEntradaAdicionarConteudoArquivoAPI = new EntradaAdicionarConteudoArquivoAPI();
  $objEntradaAdicionarConteudoArquivoAPI->setIdArquivo($numIdArquivo);
  $objEntradaAdicionarConteudoArquivoAPI->setConteudo(base64_encode(fread($fp, 1024*1024))); //blocos de 1Mb
  $objSeiRN->adicionarConteudoArquivo($objEntradaAdicionarConteudoArquivoAPI);
}
fclose($fp);
```

## adicionarConteudoArquivo

| **Entrada** |
|---|
| Instância do objeto EntradaAdicionarConteudoArquivoAPI preenchida com:<br><ul><li>IdArquivo</li><li>Conteudo</li></ul> |
| **Observação** |
| Ver exemplo em adicionarArquivo. |

## agendarPublicacao

| **Entrada** |
|---|
| Instância do objeto EntradaAgendarPublicacaoAPI preenchida com:<br><ul><li>IdDocumento ou ProtocoloDocumento</li><li>StaMotivo</li><li>IdVeiculoPublicacao</li><li>DataDisponibilizacao</li><li>Resumo</li><li>ImprensaNacional</li></ul> |
| **Observação** |
| Para identificação é necessário informar apenas um dos atributos IdDocumento ou ProtocoloDocumento. O atributo ImprensaNacional é opcional. |

**Exemplo:**

```php
$objEntradaAgendarPublicacaoAPI = new EntradaAgendarPublicacaoAPI();
//$objEntradaAgendarPublicacaoAPI->setIdDocumento(42039220124080979);
$objEntradaAgendarPublicacaoAPI->setProtocoloDocumento('0046786');
$objEntradaAgendarPublicacaoAPI->setStaMotivo(1);
$objEntradaAgendarPublicacaoAPI->setIdVeiculoPublicacao(21);
$objEntradaAgendarPublicacaoAPI->setDataDisponibilizacao('07/09/2018');
$objEntradaAgendarPublicacaoAPI->setResumo('teste');
$objPublicacaoImprensaNacionalAPI = new PublicacaoImprensaNacionalAPI();
$objPublicacaoImprensaNacionalAPI->setIdVeiculo(2);
$objPublicacaoImprensaNacionalAPI->setPagina(85);
$objPublicacaoImprensaNacionalAPI->setIdSecao(4);
$objPublicacaoImprensaNacionalAPI->setData('03/09/2018');
$objEntradaAgendarPublicacaoAPI->setImprensaNacional($objPublicacaoImprensaNacionalAPI);
$objSeiRN = new SeiRN();
$objPublicacaoAPI = $objSeiRN->agendarPublicacao($objEntradaAgendarPublicacaoAPI);
```

## alterarPublicacao

| **Entrada** |
|---|
| Instância do objeto EntradaAlterarPublicacaoAPI preenchida com:<br><ul><li>IdPublicacao ou IdDocumento ou ProtocoloDocumento</li><li>StaMotivo</li><li>IdVeiculoPublicacao</li><li>DataDisponibilizacao</li><li>Resumo</li><li>ImprensaNacional</li></ul> |
| **Observação** |
| Para identificação é necessário informar apenas um dos atributos IdPublicacao, IdDocumento ou ProtocoloDocumento. Os demais atributos são opcionais e somente os informados serão alterados se o estado da publicação permitir. |

**Exemplo:**

```php
$objEntradaAlterarPublicacaoAPI = new EntradaAlterarPublicacaoAPI();
//$objEntradaAlterarPublicacaoAPI->setIdPublicacao(100000960);
//$objEntradaAlterarPublicacaoAPI->setIdDocumento(42039220124080979);
$objEntradaAlterarPublicacaoAPI->setProtocoloDocumento('0046786');
$objEntradaAlterarPublicacaoAPI->setStaMotivo(null);
$objEntradaAlterarPublicacaoAPI->setIdVeiculoPublicacao(null);
$objEntradaAlterarPublicacaoAPI->setDataDisponibilizacao('10/09/2018');
$objEntradaAlterarPublicacaoAPI->setResumo('teste');
$objPublicacaoImprensaNacionalAPI = new PublicacaoImprensaNacionalAPI();
$objPublicacaoImprensaNacionalAPI->setIdVeiculo(2);
$objPublicacaoImprensaNacionalAPI->setPagina(85);
$objPublicacaoImprensaNacionalAPI->setIdSecao(4);
$objPublicacaoImprensaNacionalAPI->setData('06/09/2018');
$objEntradaAlterarPublicacaoAPI->setImprensaNacional($objPublicacaoImprensaNacionalAPI);
$objSeiRN = new SeiRN();
$objSeiRN->alterarPublicacao($objEntradaAlterarPublicacaoAPI);
```

## anexarProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaAnexarProcessoAPI preenchida com:<br><ul><li>IdProcedimentoPrincipal ou ProtocoloProcedimentoPrincipal</li><li>IdProcedimentoAnexado ou ProtocoloProcedimentoAnexado</li></ul> |

**Exemplo:**

```php
$objEntradaAnexarProcessoAPI = new EntradaAnexarProcessoAPI();
//$objEntradaAnexarProcessoAPI->setIdProcedimentoPrincipal();
$objEntradaAnexarProcessoAPI->setProtocoloProcedimentoPrincipal('0000495-63.2014.4.04.8000');
//$objEntradaAnexarProcessoAPI->setIdProcedimentoAnexado();
$objEntradaAnexarProcessoAPI->setProtocoloProcedimentoAnexado('0000504-25.2014.4.04.8000');


$objSeiRN = new SeiRN();
$objSeiRN->anexarProcesso($objEntradaAnexarProcessoAPI);
```

## atribuirProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaAtribuirProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>IdUsuario</li><li>SinReabrir</li></ul> |

**Exemplo:**

```php
$objEntradaAtribuirProcessoAPI = new EntradaAtribuirProcessoAPI();
//$objEntradaAtribuirProcessoAPI->setIdProcedimento();
$objEntradaAtribuirProcessoAPI->setProtocoloProcedimento('0000262-95.2016.4.04.8000');
$objEntradaAtribuirProcessoAPI->setIdUsuario(100002382);

$objEntradaAtribuirProcessoAPI->setSinReabrir('S');
$objSeiRN = new SeiRN();
$objSeiRN->atribuirProcesso($objEntradaAtribuirProcessoAPI);
```

## atualizarContatos

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto ContatoAPI preenchidas com:<br><ul><li>StaOperacao</li><li>IdContato</li><li>IdTipoContato</li><li>Sigla</li><li>Nome</li><li>NomeSocial</li><li>StaNatureza</li><li>IdContatoAssociado</li><li>SinEnderecoAssociado</li><li>Endereco</li><li>Complemento</li><li>Bairro</li><li>IdCidade</li><li>IdEstado</li><li>IdPais</li><li>Cep</li><li>StaGenero</li><li>IdCargo</li><li>Cpf</li><li>Cnpj</li><li>Rg</li><li>OrgaoExpedidor</li><li>Matricula</li><li>MatriculaOab</li><li>TelefoneFixo</li><li>TelefoneCelular</li><li>DataNascimento</li><li>Email</li><li>SitioInternet</li><li>Observação</li><li>NumeroPassaporte</li><li>IdPaisPassaporte</li><li>SinAtivo</li></ul> |

**Exemplo:**

```php
$objContatoAPI = new ContatoAPI();
$objContatoAPI->setStaOperacao('A');
$objContatoAPI->setIdContato(100003924);
$objContatoAPI->setIdTipoContato(1);
$objContatoAPI->setSigla('def');
$objContatoAPI->setNome('Dddddd Eeeeee Ffffff');
$objContatoAPI->setNomeSocial(null);
$objContatoAPI->setStaNatureza('F');
$objContatoAPI->setIdContatoAssociado(null);
$objContatoAPI->setSinEnderecoAssociado('N');
$objContatoAPI->setEndereco('Rua Otávio Francisco Caruso da Rocha, 2000');
$objContatoAPI->setComplemento(null);
$objContatoAPI->setBairro('Praia de Belas');
$objContatoAPI->setIdCidade(4927);
$objContatoAPI->setIdEstado(23);
$objContatoAPI->setIdPais(76);
$objContatoAPI->setCep('90010-395');
$objContatoAPI->setStaGenero('M');
$objContatoAPI->setIdCargo(100001865);
$objContatoAPI->setCpf(11572070730);
$objContatoAPI->setCnpj(null);
$objContatoAPI->setRg(56584632);
$objContatoAPI->setOrgaoExpedidor('SSP/RS');
$objContatoAPI->setMatricula('54834');
$objContatoAPI->setMatriculaOab(null);
$objContatoAPI->setTelefoneFixo(null);
$objContatoAPI->setTelefoneCelular('(99)9999-9999');
$objContatoAPI->setDataNascimento('13/05/1971');
$objContatoAPI->setEmail('def@abc.gov.br');
$objContatoAPI->setSitioInternet(null);
$objContatoAPI->setObservacao('Exemplo alteração contato.');
$objContatoAPI->setNumeroPassaporte(null);
$objContatoAPI->setIdPaisPassaporte(null);
$objContatoAPI->setSinAtivo('S');

$objSeiRN = new SeiRN();
$objSeiRN->atualizarContatos(array($objContatoAPI));
```

## bloquearDocumento

| **Entrada** |
|---|
| Instância do objeto EntradaBloquearDocumentoAPI preenchida com:<br><ul><li>IdDocumento ou ProtocoloDocumento</li></ul> |
| **Observações** |
| Não será possível alterar o conteúdo nem cancelar assinaturas de documentos bloqueados. Entretanto novas assinaturas poderão ser adicionadas. Os metadados do documento não são bloqueados. |

**Exemplo:**

```php
$objEntradaBloquearDocumentoAPI = new EntradaBloquearDocumentoAPI();
//$objEntradaBloquearDocumentoAPI->setIdDocumento();
$objEntradaBloquearDocumentoAPI->setProtocoloDocumento('0031076');

$objSeiRN = new SeiRN();
$objSeiRN->bloquearDocumento($objEntradaBloquearDocumentoAPI);
```

## bloquearProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaBloquearProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |
| **Observações** |
| Quando um processo estiver bloqueado as operações abaixo NÃO serão permitidas:<br><ul><li>alterar cadastro do processo</li><li>alterar cadastro do documento</li><li>incluir documento no processo</li><li>alterar conteúdo de documentos (internos/externos)</li><li>enviar processo</li><li>enviar email</li><li>agendar publicação</li><li>assinar documento</li><li>mover documento</li><li>cancelar documento</li><li>gerar circular</li><li>excluir documento</li><li>excluir processo</li><li>sobrestar processo</li><li>anexar processo</li></ul><br>Operações permitidas em processos bloqueados:<br><ul><li>atribuir marcador da unidade (*)</li><li>atribuir processo (*)</li><li>atualizar andamento (*)</li><li>liberar/cancelar acesso externo (*)</li><li>incluir em bloco de reunião (*)</li><li>relacionar processo (*)</li><li>duplicar processo (*)</li><li>dar ciência (*)</li><li>registrar anotação</li><li>cadastrar acompanhamento especial</li><li>solicitar desarquivamento</li><li>concluir processo</li><li>reabrir processo</li></ul><br>* somente com processo aberto<br>Não é possível bloquear processos sigilosos. |

**Exemplo:**

```php
$objEntradaBloquearProcessoAPI = new EntradaBloquearProcessoAPI();
//$objEntradaBloquearProcessoAPI->setIdProcedimento();
$objEntradaBloquearProcessoAPI->setProtocoloProcedimento('0000262-95.2016.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->bloquearProcesso($objEntradaBloquearProcessoAPI);
```

## cancelarAgendamentoPublicacao

| **Entrada** |
|---|
| Instância do objeto EntradaCancelarAgendamentoPublicacaoAPI preenchida com pelo menos um dos atributos:<br><ul><li>IdPublicacao ou IdDocumento ou ProtocoloDocumento</li></ul> |

**Exemplo:**

```php
$objEntradaCancelarAgendamentoPublicacaoAPI = new EntradaCancelarAgendamentoPublicacaoAPI();
$objEntradaCancelarAgendamentoPublicacaoAPI->setProtocoloDocumento('0046786');
//$objEntradaCancelarAgendamentoPublicacaoAPI->setIdDocumento(42039220124080979);
//$objEntradaCancelarAgendamentoPublicacaoAPI->setIdPublicacao(100000960);
$objSeiRN = new SeiRN();
$objSeiRN->cancelarAgendamentoPublicacao($objEntradaCancelarAgendamentoPublicacaoAPI);
```

## cancelarDisponibilizacaoBloco

| **Entrada** |
|---|
| Instância do objeto EntradaCancelarDisponibilizacaoBlocoAPI preenchida com:<br><ul><li>IdBloco</li></ul> |

**Exemplo:**

```php
$objEntradaCancelarDisponibilizacaoBlocoAPI = new EntradaCancelarDisponibilizacaoBlocoAPI();
$objEntradaCancelarDisponibilizacaoBlocoAPI->setIdBloco(932);

$objSeiRN = new SeiRN();
$objSeiRN->cancelarDisponibilizacaoBloco($objEntradaCancelarDisponibilizacaoBlocoAPI);
```

## cancelarDocumento

| **Entrada** |
|---|
| Instância do objeto EntradaCancelarDocumentoAPI preenchida com:<br><ul><li>IdDocumento ou ProtocoloDocumento</li><li>Motivo</li></ul> |

**Exemplo:**

```php
$objEntradaCancelarDocumentoAPI = new EntradaCancelarDocumentoAPI();
//$objEntradaCancelarDocumentoAPI->setIdDocumento();
$objEntradaCancelarDocumentoAPI->setProtocoloDocumento('0031076');
$objEntradaCancelarDocumentoAPI->setMotivo('Exemplo cancelamento de documento módulo ABC.');


$objSeiRN = new SeiRN();
$objSeiRN->cancelarDocumento($objEntradaCancelarDocumentoAPI);
```

## concluirBloco

| **Entrada** |
|---|
| Instância do objeto EntradaConcluirBlocoAPI preenchida com:<br><ul><li>IdBloco</li></ul> |

**Exemplo:**

```php
$objEntradaConcluirBlocoAPI = new EntradaConcluirBlocoAPI();
$objEntradaConcluirBlocoAPI->setIdBloco(1043);

$objSeiRN = new SeiRN();
$objSeiRN->concluirBloco($objEntradaConcluirBlocoAPI);
```

## concluirControlePrazo

| **Entrada** |
|---|
| Instâncias do objeto EntradaConcluirControlePrazoAPI preenchidas com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$arrObjEntradaConcluirControlePrazoAPI = array();
$objEntradaConcluirControlePrazoAPI = new EntradaConcluirControlePrazoAPI();
//$objEntradaConcluirControlePrazoAPI->setIdProcedimento();
$objEntradaConcluirControlePrazoAPI->setProtocoloProcedimento('11.1.000000485-4');
$arrObjEntradaConcluirControlePrazoAPI[] = $objEntradaConcluirControlePrazoAPI;
$objEntradaConcluirControlePrazoAPI = new EntradaConcluirControlePrazoAPI();
//$objEntradaConcluirControlePrazoAPI->setIdProcedimento();
$objEntradaConcluirControlePrazoAPI->setProtocoloProcedimento('11.1.000000467-6');
$arrObjEntradaConcluirControlePrazoAPI[] = $objEntradaConcluirControlePrazoAPI;
$objSeiRN = new SeiRN();
$objSeiRN->concluirControlePrazo($arrObjEntradaConcluirControlePrazoAPI);
```

## concluirProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaConcluirProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$objEntradaConcluirProcessoAPI = new EntradaConcluirProcessoAPI();
//$objEntradaConcluirProcessoAPI->setIdProcedimento();
$objEntradaConcluirProcessoAPI->setProtocoloProcedimento('0000262-95.2016.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->concluirProcesso($objEntradaConcluirProcessoAPI);
```

## ConfirmarDisponibilizacaoPublicacao

| **Entrada** |
|---|
| Instância do objeto EntradaConfirmarDisponibilizacaoPublicacaoAPI preenchida com:<br><ul><li>IdVeiculoDisponibilizacao</li><li>DataDisponibilizacao</li><li>DataPublicacao</li><li>Numero</li><li>IdDocumentos</li></ul> |
| **Observações** |
| Esse método é responsável por atualizar o andamento de agendamento no processo com o número e a data efetiva da publicação. Além disso, haverá mudança no nível de acesso do documento para público e o conteúdo será disponibilizado na pesquisa de publicações do SEI (se a opção Exibir as publicações enviadas para este veículo na pesquisa de publicações interna estiver marcada no cadastro do veículo de publicação). |

**Exemplo:**

```php
$objEntradaConfirmarDisponibilizacaoPublicacaoAPI = new EntradaConfirmarDisponibilizacaoPublicacaoAPI();
$objEntradaConfirmarDisponibilizacaoPublicacaoAPI->setIdVeiculoPublicacao(21);
$objEntradaConfirmarDisponibilizacaoPublicacaoAPI->setDataDisponibilizacao('10/09/2018');
$objEntradaConfirmarDisponibilizacaoPublicacaoAPI->setDataPublicacao('11/09/2018');
$objEntradaConfirmarDisponibilizacaoPublicacaoAPI->setNumero('57');
$objEntradaConfirmarDisponibilizacaoPublicacaoAPI->setIdDocumentos(array('42039220124080979','42039220124082477'));
$objSeiRN = new SeiRN();
$objSeiRN->confirmarDisponibilizacaoPublicacao($objEntradaConfirmarDisponibilizacaoPublicacaoAPI);
```

## consultarBloco

| **Entrada** |
|---|
| Instância do objeto EntradaConsultarBlocoAPI preenchida com:<br><ul><li>IdBloco</li><li>SinRetornarProtocolos</li></ul> |
| **Saída** |
| Instância do objeto SaidaConsultarBlocoAPI preenchida com:<br><ul><li>IdBloco</li><li>Descricao</li><li>Tipo</li><li>Estado</li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>SinPrioridade</li><li>SinRevisao</li><li>UsuarioAtribuicao (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>UnidadesDisponibilizacao (array: UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li><li>Protocolos (array: ProtocoloBlocoAPI)<ul><li>ProtocoloFormatado</li><li>Identificacao</li><li>Assinaturas (array: AssinaturaAPI)<ul><li>Nome</li><li>CargoFuncao</li><li>DataHora</li><li>IdUsuario</li><li>IdOrigem</li><li>IdOrgao</li><li>Sigla</li></ul></li></ul></li></ul> |

**Exemplo:**

```php
$objEntradaConsultarBlocoAPI = new EntradaConsultarBlocoAPI();
$objEntradaConsultarBlocoAPI->setIdBloco(911);
$objEntradaConsultarBlocoAPI->setSinRetornarProtocolos('S');

$objSeiRN = new SeiRN();

$objSaidaConsultarBlocoAPI = $objSeiRN->consultarBloco($objEntradaConsultarBlocoAPI);

SaidaConsultarBlocoAPI Object (
  [IdBloco] =>911
  [Descricao] =>Teste...
  [Tipo] =>A
  [Estado] =>D
  [Unidade] =>UnidadeAPI Object (
    [IdUnidade] =>110000001
    [Sigla] =>TESTE
    [Descricao] =>Unidade de Teste
  )
  [Usuario] =>UsuarioAPI Object (
    [IdUsuario] =>33645
    [Sigla] =>abc
    [Nome] =>Aaaaaa Bbbbbb Cccccc
  )
  [SinPrioridade] =>S
  [SinRevisao] =>N
  [UsuarioAtribuicao] =>UsuarioAPI Object (
    [IdUsuario] =>28767
    [Sigla] =>def
    [Nome] =>Dddddd Eeeeee Ffffff
  )
  [UnidadesDisponibilizacao] =>Array (
    [0] =>UnidadeAPI Object (
      [IdUnidade] =>100000555
      [Sigla] =>DG
      [Descricao] =>Diretoria-geral
    )
    [1] =>UnidadeAPI Object (
      [IdUnidade] =>100000644
      [Sigla] =>VPRES
      [Descricao] =>Vice-presidência
    )
  )
  [Protocolos] =>Array (
    [0] =>ProtocoloBlocoAPI Object (
      [ProtocoloFormatado] =>0011108
      [Identificacao] =>Ato 52
      [Assinaturas] =>Array (
        [0] =>AssinaturaAPI Object (
          [Nome] =>Dddddd Eeeeee Ffffff
          [CargoFuncao] =>Supervisor
          [DataHora] =>21/19/2016 16:59:12
          [IdUsuario] =>10000142
          [IdOrigem] =>20011987745
          [IdOrgao] =>1
          [Sigla] =>def
        )
      )
    )
    [1] =>ProtocoloBlocoAPI Object (
      [ProtocoloFormatado] =>0024507
      [Identificacao] =>Atestado
      [Assinaturas] =>Array (
        [0] =>AssinaturaAPI Object (
          [Nome] =>Gggggg Hhhhhh Iiiiii
          [CargoFuncao] =>Diretor
          [DataHora] =>15/09/2016 16:43:13
          [IdUsuario] =>10000217
          [IdOrigem] =>58480521101
          [IdOrgao] =>1
          [Sigla] =>ghi
        )
      )
    )
  )
)
```

## consultarDocumento

| **Entrada** |
|---|
| Instância do objeto EntradaConsultarDocumentoAPI preenchida com:<br><ul><li>IdDocumento ou ProtocoloDocumento</li><li>SinRetornarAndamentoGeracao</li><li>SinRetornarAssinaturas</li><li>SinRetornarPublicacao</li><li>SinRetornarCampos</li><li>SinRetornarBlocos</li></ul> |
| **Saída** |
| Instância do objeto SaidaConsultarDocumentoAPI preenchida com:<br><ul><li>IdProcedimento</li><li>ProcedimentoFormatado</li><li>IdDocumento</li><li>DocumentoFormatado</li><li>Serie<ul><li>IdSerie</li><li>Nome</li></ul></li><li>Numero</li><li>NomeArvore</li><li>DinValor</li><li>Data</li><li>UnidadeElaboradora (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li><li>AndamentoGeracao (array:AndamentoAPI)<ul><li>Descricao</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li></ul></li><li>Assinaturas (array:AssinaturaAPI)<ul><li>Nome</li><li>CargoFuncao</li><li>DataHora</li><li>IdUsuario</li><li>IdOrigem</li><li>IdOrgao</li><li>Sigla</li></ul></li><li>Publicacao (PublicacaoAPI)<ul><li>IdPublicacao</li><li>IdDocumento</li><li>StaMotivo</li><li>Resumo</li><li>IdVeiculoPublicacao</li><li>NomeVeiculo</li><li>StaTipoVeiculo</li><li>Numero</li><li>DataDisponibilizacao</li><li>DataPublicacao</li><li>Estado</li><li>ImprensaNacional (PublicacaoImprensaNacionalAPI)<ul><li>IdVeiculo</li><li>SiglaVeiculo</li><li>DescricaoVeiculo</li><li>Pagina</li><li>IdSecao</li><li>Secao</li><li>Data</li></ul></li></ul></li><li>Campos (CampoAPI)<ul><li>Nome</li><li>Valor</li></ul></li><li>NivelAcessoLocal<ul><li>0=Público</li><li>1=Restrito</li><li>2=Sigiloso</li></ul></li><li>NivelAcessoGlobal<ul><li>0=Público</li><li>1=Restrito</li><li>2=Sigiloso</li></ul></li><li>Blocos</li><li>LinkAcesso (link não assinado para montar a árvore de processo posicionando no documento)</li></ul> |
| **Observações** |
| Cada um dos sinalizadores do objeto de entrada implica em processamento adicional realizado pelo sistema, sendo assim, recomenda-se que seja solicitado o retorno somente para informações estritamente necessárias. Todos os sinalizadores de entrada são opcionais com valor padrão N. |

**Exemplo:**

```php
$objEntradaConsultarDocumentoAPI = new EntradaConsultarDocumentoAPI();
//$objEntradaConsultarDocumentoAPI->setIdDocumento();
$objEntradaConsultarDocumentoAPI->setProtocoloDocumento('0023930');
$objEntradaConsultarDocumentoAPI->setSinRetornarAssinaturas('S');

$objEntradaConsultarDocumentoAPI->setSinRetornarPublicacao('S');


$objSeiRN = new SeiRN();
$objSaidaConsultarDocumentoAPI =  $objSeiRN->consultarDocumento($objEntradaConsultarDocumentoAPI);

SaidaConsultarDocumentoAPI Object (
  [IdProcedimento] =>42039220124056042
  [ProcedimentoFormatado] =>0000277-98.2015.4.04.8000
  [IdDocumento] =>42039220124060399
  [DocumentoFormatado] =>0023930
  [LinkAcesso] =\>
  https://sei-desenv.trf4.jus.br/mga/controlador.php?acao=procedimento_trabalhar&id_procedimento=42039220124056042&id_documento=42039220124060399
  [Serie] =>SerieAPI Object (
    [IdSerie] =>371
    [Nome] =>Ata
  )
  [Numero] =\>
  [NomeArvore] =\>
  [DinValor] =\>
  [Data] =>03/06/2015
  [UnidadeElaboradora] =>UnidadeAPI Object (
    [IdUnidade] =>110000001
    [Sigla] =>TESTE
    [Descricao] =>Unidade de Teste
  )
  [Assinaturas] =>Array (
    [0] =>AssinaturaAPI Object (
      [Nome] =>Aaaaaa Bbbbbb Cccccc
      [CargoFuncao] =>Diretor
      [DataHora] =>10/06/2015 15:31:00
      [IdUsuario] =>10000082
      [IdOrigem] =>26654779110
      [IdOrgao] =>1
      [Sigla] =>abc
    )
  )
  [Publicacao] =>stdClass Object (
    [IdPublicacao] =>100000878
    [IdDocumento] =>42039220124060399
    [StaMotivo] =>1
    [Resumo] =\>
    [IdVeiculoPublicacao] =>21
    [NomeVeiculo] =>Diário Eletrônico Administrativo
    [StaTipoVeiculo] =>E
    [Numero] =\>
    [DataDisponibilizacao] =>12/06/2015
    [DataPublicacao] =\>
    [Estado] =>A
    [ImprensaNacional] =>stdClass Object (
      [IdVeiculo] =>2
      [SiglaVeiculo] =>DJU
      [DescricaoVeiculo] =>Diário da Justiça
      [Pagina] =>122
      [IdSecao] =>4
      [Secao] =>2
      [Data] =>01/06/2015
    )
  )
)
```

## consultarProcedimento

| **Entrada** |
|---|
| Instância do objeto EntradaConsultarProcedimentoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>SinRetornarAssuntos</li><li>SinRetornarInteressados</li><li>SinRetornarObervacoes</li><li>SinRetornarAndamentoGeracao</li><li>SinRetornarAndamentoConclusao</li><li>SinRetornarUltimoAndamento</li><li>SinRetornarUnidadesProcedimentoAberto</li><li>SinRetornarProcedimentosRelacionados</li><li>SinRetornarProcedimentosAnexados</li></ul> |
| **Saída** |
| Instância do objeto SaidaConsultarProcedimentoAPI preenchida com:<br><ul><li>IdProcedimento</li><li>ProcedimentoFormatado</li><li>Especificacao</li><li>DataAutuacao</li><li>TipoProcedimento<ul><li>IdTipoProcedimento</li><li>Nome</li></ul></li><li>TipoPrioridade<ul><li>IdTipoPrioridade</li><li>Nome</li></ul></li><li>Assuntos (array:AssuntoAPI)<ul><li>CodigoEstruturado</li><li>Descricao</li></ul></li><li>Interessados (array:InteressadoAPI)<ul><li>Sigla</li><li>Nome</li></ul></li><li>Observacoes (array:ObservacaoAPI)<ul><li>Descricao</li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li></ul></li><li>AndamentoGeracao (array:AndamentoAPI)<ul><li>Descricao</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li></ul></li><li>AndamentoConclusao (array:AndamentoAPI)<ul><li>Descricao</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li></ul></li><li>UltimoAndamento (array:AndamentoAPI)<ul><li>Descricao</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li></ul></li><li>UnidadesProcedimentoAberto (array:UnidadeProcedimentoAbertoAPI)<ul><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li><li>UsuarioAtribuicao (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li></ul></li><li>ProcedimentosRelacionados (array:ProcedimentoResumidoAPI)<ul><li>IdProcedimento</li><li>ProcedimentoFormatado</li><li>TipoProcedimento<ul><li>IdTipoProcedimento</li><li>Nome</li></ul></li></ul></li><li>ProcedimentosAnexados (array:ProcedimentoResumidoAPI)<ul><li>IdProcedimento</li><li>ProcedimentoFormatado</li><li>TipoProcedimento<ul><li>IdTipoProcedimento</li><li>Nome</li></ul></li></ul></li><li>NivelAcessoLocal<ul><li>0=Público</li><li>1=Restrito</li><li>2=Sigiloso</li></ul></li><li>NivelAcessoGlobal<ul><li>0=Público</li><li>1=Restrito</li><li>2=Sigiloso</li></ul></li><li>LinkAcesso (link não assinado para montar a árvore de processo)</li></ul> |
| **Observações** |
| Cada um dos sinalizadores do objeto de entrada implica em processamento adicional realizado pelo sistema, sendo assim, recomenda-se que seja solicitado o retorno somente para informações estritamente necessárias. Todos os sinalizadores de entrada são opcionais com valor padrão N. |

**Exemplo:**

```php
$objEntradaConsultarProcedimentoAPI = new EntradaConsultarProcedimentoAPI();
//$objEntradaConsultarProcedimentoAPI->setIdProcedimento();
$objEntradaConsultarProcedimentoAPI->setProtocoloProcedimento('0000486-33.2016.4.04.8000');
$objEntradaConsultarProcedimentoAPI->setSinRetornarAndamentoGeracao('S');
$objEntradaConsultarProcedimentoAPI->setSinRetornarUnidadesProcedimentoAberto('S');

$objSeiRN = new SeiRN();


$objSaidaConsultarProcedimentoAPI = $objSeiRN->consultarProcedimento($objEntradaConsultarProcedimentoAPI);

SaidaConsultarProcedimentoAPI Object (
  [IdProcedimento] =>10000000012635
  [ProcedimentoFormatado] =>0000486-33.2016.4.04.8000
  [Especificacao] =>Exemplo ABC com 2 documentos
  [DataAutuacao] =>04/10/2016
  [LinkAcesso] =\>
  https://sei-desenv.trf4.jus.br/mga/controlador.php?acao=procedimento_trabalhar&id_procedimento=10000000012635
  [TipoProcedimento] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000312
    [Nome] =>Autorização
  )
  [TipoPrioridade] =>TipoPrioridadeAPI Object (
    [IdTipoPrioridade] =>1
    [Nome] =>Pessoa com Deficiência
  )
  [AndamentoGeracao] =>AndamentoAPI Object (
    [Descricao] =>Processo público gerado
    [DataHora] =>04/10/2016 18:08:59
    [Usuario] =>UsuarioAPI Object (
      [IdUsuario] =>100002382
      [Sigla] =>abc
      [Nome] =>Aaaaaa Bbbbbb Cccccc
    )
    [Unidade] =>UnidadeAPI Object (
      [IdUnidade] =>110000001
      [Sigla] =>TESTE
      [Descricao] =>Unidade de Teste
    )
  )
  [UnidadesProcedimentoAberto] =>Array (
    [0] =>UnidadeProcedimentoAbertoAPI Object (
      [Unidade] =>UnidadeAPI Object (
        [IdUnidade] =>100000555
        [Sigla] =>DG
        [Descricao] =>Diretoria-geral
      )
      [UsuarioAtribuicao] =\>
    )
    [1] =>UnidadeProcedimentoAbertoAPI Object (
      [Unidade] =>UnidadeAPI Object (
        [IdUnidade] =>100000644
        [Sigla] =>VPRES
        [Descricao] =>Vice-presidência
      )
      [UsuarioAtribuicao] =\>
    )
  )
)
```

## consultarProcedimentoIndividual

| **Entrada** |
|---|
| Instância do objeto EntradaConsultarProcedimentoIndividualAPI preenchida com:<br><ul><li>IdOrgaoProcedimento</li><li>IdTipoProcedimento</li><li>IdOrgaoUsuario</li><li>SiglaUsuario</li></ul> |
| **Saída** |
| Instância do objeto ProcedimentoResumidoAPI preenchida com:<br><ul><li>IdProcedimento</li><li>ProcedimentoFormatado</li><li>TipoProcedimento<ul><li>IdTipoProcedimento</li><li>Nome</li></ul></li></ul> |
| **Observações** |
| Se houver mais de um processo individual onde o usuário é interessado então será retornado o mais recente. Caso nenhum processo seja encontrado será retornado nulo. |

**Exemplo:**

```php
$objEntradaConsultarProcedimentoIndividualAPI = new EntradaConsultarProcedimentoIndividualAPI();
$objEntradaConsultarProcedimentoIndividualAPI->setIdOrgaoProcedimento(1);
$objEntradaConsultarProcedimentoIndividualAPI->setIdTipoProcedimento(100000189);
$objEntradaConsultarProcedimentoIndividualAPI->setIdOrgaoUsuario(1);
$objEntradaConsultarProcedimentoIndividualAPI->setSiglaUsuario('abc');

$objSeiRN = new SeiRN();
$objProcedimentoResumidoAPI = $objSeiRN->consultarProcedimentoIndividual($objEntradaConsultarProcedimentoIndividualAPI);

ProcedimentoResumidoAPI Object (
  [IdProcedimento] =>1000000005880
  [ProcedimentoFormatado] =>12.1.000000261-0
  [TipoProcedimento] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000189
    [Nome] =>Averbação de Cursos
  )
)
```

## consultarPublicacao

| **Entrada** |
|---|
| Instância do objeto EntradaConsultarPublicacaoAPI:<br><ul><li>IdPublicacao ou IdDocumento ou ProtocoloDocumento</li><li>SinRetornarAndamento</li><li>SinRetornarAssinaturas</li></ul> |
| **Saída** |
| Instância do objeto PublicacaoAPI preenchida com:<br><ul><li>IdPublicacao</li><li>IdDocumento</li><li>StaMotivo</li><li>Resumo</li><li>IdVeiculoPublicacao</li><li>NomeVeiculo</li><li>StaTipoVeiculo</li><li>Numero</li><li>DataDisponibilizacao</li><li>DataPublicacao</li><li>Estado</li><li>ImprensaNacional (PublicacaoImprensaNacionalAPI)<ul><li>IdVeiculo</li><li>SiglaVeiculo</li><li>DescricaoVeiculo</li><li>Pagina</li><li>IdSecao</li><li>Secao</li><li>Data</li></ul></li></ul> |

**Exemplo:**

```php
$objEntradaConsultarPublicacaoAPI = new EntradaConsultarPublicacaoAPI();
//$objEntradaConsultarPublicacaoAPI->setIdPublicacao(100000960);
//$objEntradaConsultarPublicacaoAPI->setIdDocumento(42039220124080979);
$objEntradaConsultarPublicacaoAPI->setProtocoloDocumento('0046786');
$objSeiRN = new SeiRN();
$objSaidaConsultarPublicacaoAPI = $objSeiRN->consultarPublicacao($objEntradaConsultarPublicacaoAPI);
SaidaConsultarPublicacaoAPI Object (
  [Publicacao] =>stdClass Object (
    [IdPublicacao] =>100000878
    [IdDocumento] =>42039220124060399
    [StaMotivo] =>1
    [Resumo] =\>
    [IdVeiculoPublicacao] =>21
    [NomeVeiculo] =>Diário Eletrônico Administrativo
    [StaTipoVeiculo] =>E
    [Numero] =\>
    [DataDisponibilizacao] =>12/06/2015
    [DataPublicacao] =\>
    [Estado] =>A
    [ImprensaNacional] =>stdClass Object (
      [IdVeiculo] =>2
      [SiglaVeiculo] =>DJU
      [DescricaoVeiculo] =>Diário da Justiça
      [Pagina] =>122
      [IdSecao] =>4
      [Secao] =>2
      [Data] =>01/06/2015
    )
  )
  [Andamento] =>stdClass Object (
    [Descricao] =>Publicação do documento 0023930 (Ata) no veículo Diário Eletrônico Administrativo de 12/06/2015 (Data de Disponibilização)
    [DataHora] =>11/06/2015 10:41:57
    [Unidade] =>stdClass Object (
      [IdUnidade] =>110000001
      [Sigla] =>TESTE
      [Descricao] =>Unidade de Teste de Sistemas
    )
    [Usuario] =>stdClass Object (
      [IdUsuario] =>100002382
      [Sigla] =>abc
      [Nome] =>Aaaaaa Bbbbbb Cccccc
    )
  )
  [Assinaturas] =>Array (
    [0] =>AssinaturaAPI Object (
      [Nome] =>Aaaaaa Bbbbbb Cccccc
      [CargoFuncao] =>Diretor
      [DataHora] =>10/06/2015 15:31:00
      [IdUsuario] =>10000082
      [IdOrigem] =>26654779110
      [IdOrgao] =>1
      [Sigla] =>abc
    )
  )
)
```

## definirControlePrazo

| **Saída** |
|---|
| Conjunto de Instâncias do objeto EntradaDefinirControlePrazoAPI preenchidas com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>DataPrazo</li><li>Dias</li><li>SinDiasUteis</li></ul> |

**Exemplo:**

```php
$arrObjEntradaDefinirControlePrazoAPI = array();
$objEntradaDefinirControlePrazoAPI = new EntradaDefinirControlePrazoAPI();
//$objEntradaDefinirControlePrazoAPI->setIdProcedimento();
$objEntradaDefinirControlePrazoAPI->setProtocoloProcedimento('12.1.000000989-5');
$objEntradaDefinirControlePrazoAPI->setDataPrazo('01/10/2018');
$objEntradaDefinirControlePrazoAPI->setDias(null);
$objEntradaDefinirControlePrazoAPI->setSinDiasUteis(null);
$arrObjEntradaDefinirControlePrazoAPI[] = $objEntradaDefinirControlePrazoAPI;
$objEntradaDefinirControlePrazoAPI = new EntradaDefinirControlePrazoAPI();
//$objEntradaDefinirControlePrazoAPI->setIdProcedimento();
$objEntradaDefinirControlePrazoAPI->setProtocoloProcedimento('10.1.000000470-0');
$objEntradaDefinirControlePrazoAPI->setDataPrazo(null);
$objEntradaDefinirControlePrazoAPI->setDias(15);
$objEntradaDefinirControlePrazoAPI->setSinDiasUteis('S');
$arrObjEntradaDefinirControlePrazoAPI[] = $objEntradaDefinirControlePrazoAPI;
$objSeiRN = new SeiRN();
$objSeiRN->definirControlePrazo($arrObjEntradaDefinirControlePrazoAPI);
```

## definirMarcador

| **Saída** |
|---|
| Conjunto de Instâncias do objeto DefinicaoMarcadorAPI preenchidas com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>IdMarcador</li><li>Texto</li></ul> |

**Exemplo:**

```php
$arrObjDefinicaoMarcadorAPI = array();

$objDefinicaoMarcadorAPI = new DefinicaoMarcadorAPI();
//$objDefinicaoMarcadorAPI->setIdProcedimento();
$objDefinicaoMarcadorAPI->setProtocoloProcedimento('0000488-03.2016.4.04.8000');

$objDefinicaoMarcadorAPI->setIdMarcador(9);
$objDefinicaoMarcadorAPI->setTexto('Exemplo definição marcador processo módulo ABC.');
$arrObjDefinicaoMarcadorAPI[] = $objDefinicaoMarcadorAPI;

$objDefinicaoMarcadorAPI = new DefinicaoMarcadorAPI();
//$objDefinicaoMarcadorAPI->setIdProcedimento();
$objDefinicaoMarcadorAPI->setProtocoloProcedimento('0000442-14.2016.4.04.8000');
$objDefinicaoMarcadorAPI->setIdMarcador(4);
$objDefinicaoMarcadorAPI->setTexto('Exemplo definição marcador processo módulo ABC.');
$arrObjDefinicaoMarcadorAPI[] = $objDefinicaoMarcadorAPI;

$objSeiRN = new SeiRN();
$objSeiRN->definirMarcador($arrObjDefinicaoMarcadorAPI);
```

## desanexarProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaDesanexarProcessoAPI preenchida com:<br><ul><li>IdProcedimentoPrincipal ou ProtocoloProcedimentoPrincipal</li><li>IdProcedimentoAnexado ou ProtocoloProcedimentoAnexado</li><li>Motivo</li></ul> |

**Exemplo:**

```php
$objEntradaDesanexarProcessoAPI = new EntradaDesanexarProcessoAPI();
//$objEntradaDesanexarProcessoAPI->setIdProcedimentoPrincipal();
$objEntradaDesanexarProcessoAPI->setProtocoloProcedimentoPrincipal('0000495-63.2014.4.04.8000');
//$objEntradaDesanexarProcessoAPI->setIdProcedimentoAnexado();
$objEntradaDesanexarProcessoAPI->setProtocoloProcedimentoAnexado('0000504-25.2014.4.04.8000');
$objEntradaDesanexarProcessoAPI->setMotivo('Exemplo desanexação de processo módulo ABC.');

$objSeiRN = new SeiRN();
$objSeiRN->desanexarProcesso($objEntradaDesanexarProcessoAPI);
```

## desbloquearProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaBloquearProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$objEntradaDesbloquearProcessoAPI = new EntradaDesbloquearProcessoAPI();
//$objEntradaDesbloquearProcessoAPI->setIdProcedimento();


$objEntradaDesbloquearProcessoAPI->setProtocoloProcedimento('0000262-95.2016.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->desbloquearProcesso($objEntradaDesbloquearProcessoAPI);
```

## devolverBloco

| **Entrada** |
|---|
| Instância do objeto EntradaDevolverBlocoAPI preenchida com:<br><ul><li>IdBloco</li></ul> |

**Exemplo:**

```php
$objEntradaDevolverBlocoAPI = new EntradaDevolverBlocoAPI();
$objEntradaDevolverBlocoAPI->setIdBloco(944);

$objSeiRN = new SeiRN();
$objSeiRN->devolverBloco($objEntradaDevolverBlocoAPI);
```

## disponibilizarBloco

| **Entrada** |
|---|
| Instância do objeto EntradaDisponibilizarBlocoAPI preenchida com:<br><ul><li>IdBloco</li></ul> |

**Exemplo:**

```php
$objEntradaDisponibilizarBlocoAPI = new EntradaDisponibilizarBlocoAPI();
$objEntradaDisponibilizarBlocoAPI->setIdBloco(932);

$objSeiRN = new SeiRN();
$objSeiRN->disponibilizarBloco($objEntradaDisponibilizarBlocoAPI);
```

## enviarEmail

| **Entrada** |
|---|
| Instância do objeto EntradaEnviarEmailAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>De</li><li>Para</li><li>CCO</li><li>Assunto</li><li>Mensagem</li><li>NivelAcesso Opcional<ul><li>0 = Público (valor padrão)</li><li>1 = Restrito</li></ul></li><li>IdHipoteseLegal Opcional, Identificador interno da hipótese legal associada</li><li>IdDocumentos</li><li>Arquivos</li></ul> |
| **Saída** |
| Instância do objeto SaidaEnviarEmailAPI preenchida com:<br><ul><li>IdDocumento</li><li>DocumentoFormatado</li><li>LinkAcesso</li></ul> |
| **Observações** |
| No atributo Arquivos a chave deve conter o nome que o arquivo receberá no e-mail e o valor deve conter o nome do arquivo localizado no diretório temporário do SEI (/opt/sei/temp). Após o envio do e-mail os arquivos serão removidos do diretório. Se não informado o nível de acesso será assumido o nível de acesso Público. |

**Exemplo:**

```php
$objEntradaEnviarEmailAPI = new EntradaEnviarEmailAPI();
//$objEntradaEnviarEmailAPI->setIdProcedimento();
$objEntradaEnviarEmailAPI->setProtocoloProcedimento('0000508-57.2017.4.04.8000');
$objEntradaEnviarEmailAPI->setDe('aaa@abc.gov.br');
$objEntradaEnviarEmailAPI->setPara('bbb@abc.gov.br;ccc@abc.gov.br');
$objEntradaEnviarEmailAPI->setCCO(null);
$objEntradaEnviarEmailAPI->setAssunto('Teste');
$objEntradaEnviarEmailAPI->setMensagem('Conteúdo da Mensagem');

$objEntradaEnviarEmailAPI->setNivelAcesso('1');
$objEntradaEnviarEmailAPI->setIdDocumentos(array('42039220124073679','42039220124074073'));
$objEntradaEnviarEmailAPI->setArquivos(array('Folheto.png' => '4317899510884396eb43bb25357939ea', 'Resumo.pdf' => 'b9fdce2f728b076b7a7cb60b9453ec19'));

$objSeiRN = new SeiRN();
$objSaidaEnviarEmailAPI = $objSeiRN->enviarEmail($objEntradaEnviarEmailAPI);
```

## enviarProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaEnviarProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>UnidadesDestino</li><li>SinManterAbertoUnidade (valor padrão N)</li><li>SinRemoverAnotacao (valor padrão N)</li><li>SinEnviarEmailNotificacao (valor padrão N)</li><li>DataRetornoProgramado (valor padrão nulo)</li><li>DiasRetornoProgramado (valor padrão nulo)</li><li>SinDiasUteisRetornoProgramado (valor padrão N)</li><li>SinReabrir (valor padrão N)</li></ul> |

**Exemplo:**

```php
$objEntradaEnviarProcessoAPI = new EntradaEnviarProcessoAPI();
 $objEntradaEnviarProcessoAPI->setIdProcedimento(10000000012057);
//$objEntradaEnviarProcessoAPI->setProtocoloProcedimento();
$objEntradaEnviarProcessoAPI->setUnidadesDestino(array(100000555,100000644));
$objEntradaEnviarProcessoAPI->setSinManterAbertoUnidade('S');

$objSeiRN = new SeiRN();
$objSeiRN->enviarProcesso($objEntradaEnviarProcessoAPI);
```

## excluirBloco

| **Entrada** |
|---|
| Instância do objeto EntradaExcluirBlocoAPI preenchida com:<br><ul><li>IdBloco</li></ul> |

**Exemplo:**

```php
$objEntradaExcluirBlocoAPI = new EntradaExcluirBlocoAPI();
$objEntradaExcluirBlocoAPI->setIdBloco(933);

$objSeiRN = new SeiRN();
$objSeiRN->excluirBloco($objEntradaExcluirBlocoAPI);
```

## excluirDocumento

| **Entrada** |
|---|
| Instância do objeto EntradaExcluirDocumentoAPI preenchida com:<br><ul><li>IdDocumento ou ProtocoloDocumento</li></ul> |

**Exemplo:**

```php
$objEntradaExcluirDocumentoAPI = new EntradaExcluirDocumentoAPI();
//$objEntradaExcluirDocumentoAPI->setIdDocumento();
$objEntradaExcluirDocumentoAPI->setProtocoloDocumento('0031076');

$objSeiRN = new SeiRN();
$objSeiRN->excluirDocumento($objEntradaExcluirDocumentoAPI);
```

## excluirProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaExcluirProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$objEntradaExcluirProcessoAPI = new EntradaExcluirProcessoAPI();
//$objEntradaExcluirProcessoAPI->setIdProcedimento();
$objEntradaExcluirProcessoAPI->setProtocoloProcedimento('0000495-63.2014.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->excluirProcesso($objEntradaExcluirProcessoAPI);
```

## gerarBloco

| **Entrada** |
|---|
| Instância do objeto EntradaGerarBlocoAPI preenchida com:<br><ul><li>Tipo<ul><li>A = Assinatura</li><li>R = Reunião</li><li>I = Interno</li></ul></li><li>Descricao</li><li>UnidadesDisponibilizacao</li><li>Documentos ou IdDocumentos</li><li>SinDisponibilizar</li></ul> |
| **Saída** |
| Retorna o ID do bloco gerado. |

**Exemplo:**

```php
$objEntradaGerarBlocoAPI = new EntradaGerarBlocoAPI();
$objEntradaGerarBlocoAPI->setTipo('A');
$objEntradaGerarBlocoAPI->setDescricao('Exemplo geração de bloco módulo ABC');
$objEntradaGerarBlocoAPI->setUnidadesDisponibilizacao(array('100000555','100000644'));

//se os identificadores estiverem disponíveis utilizar setIdDocumentos evitando consulta ao banco
$objEntradaGerarBlocoAPI->setDocumentos(array('0031064','0030780'));

//$objEntradaGerarBlocoAPI->setIdDocumentos();
$objEntradaGerarBlocoAPI->setSinDisponibilizar('S');

$objSeiRN = new SeiRN();
$numIdBloco = $objSeiRN->gerarBloco($objEntradaGerarBlocoAPI);
```

## gerarProcedimento

| **Entrada** |
|---|
| Instância do objeto EntradaGerarProcedimentoAPI preenchida com:<br><ul><li>Procedimento (ProcedimentoAPI)<ul><li>IdTipoProcedimento</li><li>NumeroProtocolo e DataAutuacao (opcionais)</li><li>Especificacao</li><li>Assuntos (array:AssuntoAPI preenchido com CodigoEstruturado, também adicionará automaticamente os assuntos sugeridos para o tipo de processo),</li><li>Interessados (array:InteressadoAPI),</li><li>Observacao</li><li>NivelAcesso (se não informado assumirá o nível padrão especificado para o tipo de processo)</li><li>IdHipoteseLegal</li></ul></li><li>Documentos - array:DocumentoAPI<ul><li>Tipo</li><li>IdSerie</li><li>Numero</li><li>Data</li><li>Descricao</li><li>IdTipoConferencia</li><li>SinArquivamento</li><li>Remetente (RemetenteAPI)</li><li>Interessados (array:InteressadoAPI)</li><li>Destinatarios (array:DestinatarioAPI)</li><li>Observacao</li><li>NivelAcesso (se não informado assumirá o nível padrão especificado para o tipo de processo)</li><li>IdHipoteseLegal</li><li>NomeArquivo (obrigatório para documentos externos)</li><li>IdArquivo ou Conteudo (Base64) ou ConteudoMTOM (Binário)</li><li>Campos (array:CampoAPI preenchidos com Nome/Valor, somente para formulários)</li></ul></li><li>ProcedimentosRelacionados - array com os IDs dos processos</li><li>UnidadesEnvio - array com os IDs das unidades</li><li>SinManterAbertoUnidade</li><li>SinEnviarEmailNotificacao</li><li>DataRetornoProgramado</li><li>DiasRetornoProgramado</li><li>SinDiasUteisRetornoProgramado</li><li>IdMarcador</li><li>TextoMarcador</li><li>DataControlePrazo</li><li>DiasControlePrazo</li><li>SinDiasUteisControlePrazo</li></ul> |
| **Saída** |
| Instância do objeto SaidaGerarProcedimentoAPI preenchida com:<br><ul><li>IdProcedimento</li><li>ProcedimentoFormatado</li><li>LinkAcesso (link não assinado para montar a árvore de processo)</li><li>RetornoInclusaoDocumentos - array:SaidaIncluirDocumentoAPI<ul><li>IdDocumento</li><li>DocumentoFormatado</li><li>LinkAcesso (link não assinado para montar a árvore de processo posicionando no documento)</li></ul></li></ul> |
| **Observações** |
| Ao utilizar a operação gerarProcedimento, atenção para a boa prática descrita neste manual em:<br><ul><li>3\. Considerações Prévias \> Conexões e Transações \> Transações de informações utilizando a operação GerarProcedimento</li></ul> |

**Exemplo:**

```php
$objProcedimentoAPI = new ProcedimentoAPI();
$objProcedimentoAPI->setIdTipoProcedimento(100000312);
$objProcedimentoAPI->setEspecificacao('Exemplo ABC');

$arrObjInteressadoAPI = array();
$objInteressadoAPI = new InteressadoAPI();
$objInteressadoAPI->setCpf('437.095.810-52');
$objInteressadoAPI->setNome('Marcos');
$arrObjInteressadoAPI[] = $objInteressadoAPI;
$objInteressadoAPI = new InteressadoAPI();
$objInteressadoAPI->setSigla('lmr');
$objInteressadoAPI->setNome('Luiza');
$arrObjInteressadoAPI[] = $objInteressadoAPI;

$objProcedimentoAPI->setInteressados($arrObjInteressadoAPI);
$objEntradaGerarProcedimentoAPI = new EntradaGerarProcedimentoAPI();
$objEntradaGerarProcedimentoAPI->setProcedimento($objProcedimentoAPI);

$objSeiRN = new SeiRN();
$objSeiRN->gerarProcedimento($objEntradaGerarProcedimentoAPI);

//Gera processo com 2 documentos enviando para 2 unidades mantendo aberto na unidade atual
$objProcedimentoAPI = new ProcedimentoAPI();
$objProcedimentoAPI->setIdTipoProcedimento(100000312);
$objProcedimentoAPI->setEspecificacao('Exemplo ABC com 2 documentos');

$objDocumentoAPIGerado = new DocumentoAPI();
$objDocumentoAPIGerado->setTipo('G');
$objDocumentoAPIGerado->setIdSerie(371);


$objDocumentoAPIGerado->setConteudo(base64_encode('Texto do documento interno'));

$objDocumentoAPIExterno = new DocumentoAPI();
$objDocumentoAPIExterno->setTipo('R');
$objDocumentoAPIExterno->setIdSerie(293);
$objDocumentoAPIExterno->setData('26/03/2014');
$objDocumentoAPIExterno->setNomeArquivo('exemplo.pdf');
$objDocumentoAPIExterno->setConteudo(base64_encode(file_get_contents(DIR_SEI_TEMP.'/exemplo.pdf')));

$objEntradaGerarProcedimentoAPI = new EntradaGerarProcedimentoAPI();
$objEntradaGerarProcedimentoAPI->setProcedimento($objProcedimentoAPI);
$objEntradaGerarProcedimentoAPI->setDocumentos(array($objDocumentoAPIGerado, $objDocumentoAPIExterno));
$objEntradaGerarProcedimentoAPI->setUnidadesEnvio(array(100000555,100000644));
$objEntradaGerarProcedimentoAPI->setSinManterAbertoUnidade('S');

$objSeiRN = new SeiRN();
$objSeiRN->gerarProcedimento($objEntradaGerarProcedimentoAPI);
```

## incluirDocumento

| **Entrada** |
|---|
| Instância do objeto DocumentoAPI preenchida com:<br><ul><li>Tipo</li><li>IdProcedimento ou ProtocoloProcedimento</li><li>IdSerie</li><li>Numero</li><li>NomeArvore</li><li>DinValor</li><li>Data</li><li>Descricao</li><li>IdTipoConferencia</li><li>SinArquivamento</li><li>Remetente (RemetenteAPI)</li><li>Interessados (array:InteressadoAPI)</li><li>Destinatarios (array:DestinatarioAPI)</li><li>Observacao</li><li>NivelAcesso (se não informado assumirá o nível padrão especificado para o tipo de processo)</li><li>IdHipoteseLegal</li><li>NomeArquivo (obrigatório para documentos externos)</li><li>IdArquivo ou Conteudo (Base64) ou ConteudoMTOM (Binário)</li><li>Campos (array:CampoAPI preenchidos com Nome/Valor, somente para formulários)</li><li>SinBloqueado (valor padrão N, se informado com S então não será possível alterar o conteúdo)</li></ul> |
| **Saída** |
| Instância do objeto SaidaIncluirDocumentoAPI preenchida com:<br><ul><li>IdDocumento</li><li>DocumentoFormatado</li><li>LinkAcesso (link não assinado para montar a árvore de processo posicionando no documento)</li></ul> |

**Exemplo:**

```php
//Incluir documento interno
$objDocumentoAPI = new DocumentoAPI();
//Se o ID do processo é conhecido utilizar setIdProcedimento no lugar de setProtocoloProcedimento
//evitando uma consulta ao banco
$objDocumentoAPI->setProtocoloProcedimento('0000488-03.2016.4.04.8000');
//$objDocumentoAPI->setIdProcedimento();
$objDocumentoAPI->setTipo('G');
$objDocumentoAPI->setIdSerie(371);
$objDocumentoAPI->setConteudo(base64_encode('Texto do documento interno'));

$objSeiRN = new SeiRN();
$objSeiRN->incluirDocumento($objDocumentoAPI);

//Incluir documento externo
$objDocumentoAPI = new DocumentoAPI();

//Se o ID do processo é conhecido utilizar setIdProcedimento no lugar de setProtocoloProcedimento
//evitando uma consulta ao banco
$objDocumentoAPI->setProtocoloProcedimento('0000488-03.2016.4.04.8000');
//$objDocumentoAPI->setIdProcedimento();

$objDocumentoAPI->setTipo('R');
$objDocumentoAPI->setIdSerie(293);
$objDocumentoAPI->setData('26/03/2014');
$objDocumentoAPI->setNomeArquivo('exemplo.pdf');
$objDocumentoAPI->setConteudo(base64_encode(file_get_contents(DIR_SEI_TEMP.'/exemplo.pdf')));

$objSeiRN = new SeiRN();
$objSeiRN->incluirDocumento($objDocumentoAPI);
```

## incluirDocumentoBloco

| **Entrada** |
|---|
| Instância do objeto EntradaIncluirDocumentoBlocoAPI preenchida com:<br><ul><li>IdBloco</li><li>IdDocumento ou ProtocoloDocumento</li><li>Anotacao</li></ul> |

**Exemplo:**

```php
$objEntradaIncluirDocumentoBlocoAPI = new EntradaIncluirDocumentoBlocoAPI();
$objEntradaIncluirDocumentoBlocoAPI->setIdBloco(932);
//$objEntradaIncluirDocumentoBlocoAPI->setIdDocumento();
$objEntradaIncluirDocumentoBlocoAPI->setProtocoloDocumento('0011323');
$objEntradaIncluirDocumentoBlocoAPI->setAnotacao('Exemplo anotação em documento do bloco módulo ABC.');

$objSeiRN = new SeiRN();
$objSeiRN->incluirDocumentoBloco($objEntradaIncluirDocumentoBlocoAPI);
```

## incluirProcessoBloco

| **Entrada** |
|---|
| Instância do objeto EntradaIncluirProcessoBlocoAPI preenchida com:<br><ul><li>IdBloco</li><li>IdProcedimento ou ProtocoloProcedimento</li><li>Anotacao</li></ul> |

**Exemplo:**

```php
$objEntradaIncluirProcessoBlocoAPI = new EntradaIncluirProcessoBlocoAPI();
$objEntradaIncluirProcessoBlocoAPI->setIdBloco(777);
//$objEntradaIncluirProcessoBlocoAPI->setIdProcedimento();
$objEntradaIncluirProcessoBlocoAPI->setProtocoloProcedimento('0001570-06.2015.4.04.8000');
$objEntradaIncluirProcessoBlocoAPI->setAnotacao('Exemplo anotação em processo do bloco módulo ABC.');

$objSeiRN = new SeiRN();
$objSeiRN->incluirProcessoBloco($objEntradaIncluirProcessoBlocoAPI);
```

## lancarAndamento

| **Entrada** |
|---|
| Instância do objeto EntradaLancarAndamentoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>IdTarefa ou IdTarefaModulo</li><li>Atributos (array:AtributoAndamentoAPI)<ul><li>Nome</li><li>Valor</li><li>IdOrigem</li></ul></li></ul> |
| **Saída** |
| Instância do objeto AndamentoAPI preenchida com:<br><ul><li>IdAndamento</li><li>IdTarefa</li><li>IdTarefaModulo</li><li>Descricao</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li><li>Atributos (array: AtributoAndamentoAPI)<ul><li>Nome</li><li>Valor</li><li>IdOrigem</li></ul></li></ul> |
| **Observações** |
| Se informado o atributo IdTarefa do objeto de entrada então ele deve ser um número maior ou igual a 1000 (identificadores abaixo desse valor são reservados do core do SEI) ou então 65 que equivale à tarefa de atualização de andamento (nesse caso informar um atributo com Nome=DESCRICAO e Valor=texto do andamento). |

**Exemplo:**

```php
$objEntradaLancarAndamentoAPI = new EntradaLancarAndamentoAPI();
$objEntradaLancarAndamentoAPI->setIdProcedimento(10000000012057);
$objEntradaLancarAndamentoAPI->setIdTarefaModulo('MD_ABC_AUDIENCIA_REALIZADA');

$arrObjAtributoAndamentoAPI = array();
$objAtributoAndamentoAPI = new AtributoAndamentoAPI();
$objAtributoAndamentoAPI->setNome('PREDIO');
$objAtributoAndamentoAPI->setValor('101');
$objAtributoAndamentoAPI->setIdOrigem(54); //ID do prédio, pode ser null
$arrObjAtributoAndamentoAPI[] = $objAtributoAndamentoAPI;
$objAtributoAndamentoAPI = new AtributoAndamentoAPI();
$objAtributoAndamentoAPI->setNome('SALA');
$objAtributoAndamentoAPI->setValor('3A');
$objAtributoAndamentoAPI->setIdOrigem(9334); //ID da sala, pode ser null
$arrObjAtributoAndamentoAPI[] = $objAtributoAndamentoAPI;
$objEntradaLancarAndamentoAPI->setAtributos($arrObjAtributoAndamentoAPI);

$objSeiRN = new SeiRN();
$objAndamentoAPI = $objSeiRN->lancarAndamento($objEntradaLancarAndamentoAPI);

AndamentoAPI Object (
  [IdAndamento] =>106159
  [IdTarefa] =>1016
  [IdTarefaModulo] =>MD_ABC_AUDIENCIA_REALIZADA
  [Descricao] =>Audiência agendada no prédio 101 (sala 3A)
  [DataHora] =>05/10/2016 16:12:40
  [Usuario] =>UsuarioAPI Object (
    [IdUsuario] =>100002382
    [Sigla] =>abc
    [Nome] =>Aaaaaa Bbbbbb Cccccc
  )
  [Unidade] =>UnidadeAPI Object (
    [IdUnidade] =>110000001
    [Sigla] =>TESTE
    [Descricao] =>Unidade de Teste
  )
  [Atributos] =>Array (
    [0] =>AtributoAndamentoAPI Object (
      [Nome] =>PREDIO
      [Valor] =>101
      [IdOrigem] =>54
    )
    [1] =>AtributoAndamentoAPI Object (
      [Nome] =>SALA
      [Valor] =>3A
      [IdOrigem] =>9334
    )
  )
)
```

## listarAndamentos

| **Entrada** |
|---|
| Instância do objeto EntradaListarAndamentosAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>SinRetornarAtributos</li><li>Andamentos</li><li>Tarefas</li><li>TarefasModulos</li></ul> |
| **Saída** |
| Lista de instâncias do objeto AndamentoAPI preenchidas com:<br><ul><li>IdAndamento</li><li>IdTarefa</li><li>IdTarefaModulo</li><li>Descricao</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Unidade (UnidadeAPI)<ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li></ul></li><li>Atributos (array: AtributoAndamentoAPI)<ul><li>Nome</li><li>Valor</li><li>IdOrigem</li></ul></li></ul> |
| **Observações** |
| No objeto de entrada é necessário informar pelo menos um dos atributos Andamentos, Tarefas ou TarefasModulos. No atributo Tarefas é possível filtrar por qualquer tarefa do sistema (verificar os valores de tarefas internas nas constantes existentes no arquivo TarefaRN.php). |

**Exemplo:**

```php
$objEntradaListarAndamentosAPI = new EntradaListarAndamentosAPI();
$objEntradaListarAndamentosAPI->setIdProcedimento(10000000012057);
//$objEntradaListarAndamentosAPI->setProtocoloProcedimento();
$objEntradaListarAndamentosAPI->setTarefasModulos(array('MD_ABC_AUDIENCIA_REALIZADA'));
$objEntradaListarAndamentosAPI->setSinRetornarAtributos('S');


$objSeiRN = new SeiRN();
$arrObjAndamentoAPI = $objSeiRN->listarAndamentos($objEntradaListarAndamentosAPI);

Array (
  [0] =>AndamentoAPI Object (
    [IdAndamento] =>106159
    [IdTarefa] =>1016
    [IdTarefaModulo] =>MD_ABC_AUDIENCIA_REALIZADA
    [Descricao] =>Audiência agendada no prédio 101 (sala 3A)
    [DataHora] =>05/10/2016 16:12:40
    [Usuario] =>UsuarioAPI Object (
      [IdUsuario] =>100002382
      [Sigla] =>abc
      [Nome] =>Aaaaaa Bbbbbb Cccccc
    )
    [Unidade] =>UnidadeAPI Object (
      [IdUnidade] =>110000001
      [Sigla] =>TESTE
      [Descricao] =>Unidade de Teste
    )
    [Atributos] =>Array (
      [0] =>AtributoAndamentoAPI Object (
        [Nome] =>PREDIO
        [Valor] =>101
        [IdOrigem] =>54
      )
      [1] =>AtributoAndamentoAPI Object (
        [Nome] =>SALA
        [Valor] =>3A
        [IdOrigem] =>9334
      )
    )
  )
)
```

## listarAndamentosMarcadores

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarAndamentosMarcadoresAPI preenchidas com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>Marcadores</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto AndamentoMarcadorAPI preenchidas com:<br><ul><li>IdAndamentoMarcador</li><li>Texto</li><li>DataHora</li><li>Usuario (UsuarioAPI)<ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul></li><li>Marcador (MarcadorAPI)<ul><li>IdMarcador</li><li>Nome</li><li>Icone</li><li>SinAtivo</li></ul></li><li>DataHora</li></ul> |

**Exemplo:**

```php
$objEntradaListarAndamentosMarcadoresAPI = new EntradaListarAndamentosMarcadoresAPI();
//$objEntradaListarAndamentosMarcadoresAPI->setIdProcedimento();
$objEntradaListarAndamentosMarcadoresAPI->setProtocoloProcedimento('0000488-03.2016.4.04.8000');
//$objEntradaListarAndamentosMarcadoresAPI->setMarcadores($Marcadores);

$objSeiRN = new SeiRN();


$arrObjAndamentoMarcadorAPI = $objSeiRN->listarAndamentosMarcadores($objEntradaListarAndamentosMarcadoresAPI);

Array (
  [0] =>AndamentoMarcadorAPI Object (
    [IdAndamentoMarcador] =>99
    [Texto] =>Texto do andamento
    [DataHora] =>07/10/2016 11:30:15
    [Usuario] =>UsuarioAPI Object (
      [IdUsuario] =>56555
      [Sigla] =>abc
      [Nome] =>Aaaaaa Bbbbbb Cccccc
    )
    [Marcador] =>MarcadorAPI Object (
      [IdMarcador] =>12
      [Nome] =>Teste 4
      [Icone] =\>
      data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wB/ACdeZVobAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAgklEQVR4nJWSyxHAIAhEkbGXNEFulkIfacRSvGFfycGMMUqIctL1LR8Hdx4brIT/esghjiIl1g05xJ32TpQseoWWLhAAVAV/c1Pi9oo2DcMw3qZHBQ1aDZykJUsZph/apqcMLX0bKHH9b5t+KqiekX611HlUGrrVoMQCUs9qk251vS8g0UT9daGY9AAAAABJRU5ErkJggg==
      [SinAtivo] =>S
    )
  )
  [1] =>AndamentoMarcadorAPI Object (
    [IdAndamentoMarcador] =>98
    [Texto] =>Texto do andamento com marcador removido
    [DataHora] =>07/10/2016 11:29:56
    [Usuario] =>UsuarioAPI Object (
      [IdUsuario] =>56555
      [Sigla] =>abc
      [Nome] =>Aaaaaa Bbbbbb Cccccc
    )
    [Marcador] =\>
  )
  [2] =>AndamentoMarcadorAPI Object (
    [IdAndamentoMarcador] =>97
    [Texto] =>Texto do andamento
    [DataHora] =>06/10/2016 18:48:37
    [Usuario] =>UsuarioAPI Object (
      [IdUsuario] =>37322
      [Sigla] =>def
      [Nome] =>Dddddd Eeeeee Ffffff
    )
    [Marcador] =>MarcadorAPI Object (
      [IdMarcador] =>8
      [Nome] =>Teste 3
      [Icone] =\>
      data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wB/ACdeZVobAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAZklEQVR4nGP8X6/OQApgwSWRuaUEU3C6Tw8T8apx2oCserpPD5ogug14zMaigaBqFCdhVY0pyES82QgNRKqGBAD2YMWlmlgNcNVQDch8/KoRNuDSgynOhEcOqylMuFTgspOR1OQNAPr/JbzEDsOcAAAAAElFTkSuQmCC
      [SinAtivo] =>S
    )
  )
  [3] =>AndamentoMarcadorAPI Object (
    [IdAndamentoMarcador] =>96
    [Texto] =>Texto do andamento
    [DataHora] =>06/10/2016 18:48:26
    [Usuario] =>UsuarioAPI Object (
      [IdUsuario] =>56555
      [Sigla] =>abc
      [Nome] =>Aaaaaa Bbbbbb Cccccc
    )
    [Marcador] =>MarcadorAPI Object (
      [IdMarcador] =>9
      [Nome] =>Marcador1
      [Icone] =\>
      data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wB/ACdeZVobAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAZklEQVR4nGP8X6/OQApgwSVx0HEmpqD9/nQm4lXjtAFZtf3+dDRBdBvwmI1FA0HVKE7CqhpTkIl4sxEaiFQNCQDswYpLNbEa4KqhGpD5+FUjbMClB1OcCY8cVlOYcKnAZScjqckbAEmjJZ7CtTvqAAAAAElFTkSuQmCC
      [SinAtivo] =>S
    )
  )
)
```

## listarCargos

| **Entrada** |
|---|
| Instância do objeto EntradaListarCargosAPI preenchida com:<br><ul><li>IdCargo</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto CargoAPI preenchidas com:<br><ul><li>IdCargo</li><li>ExpressaoCargo</li><li>ExpressaoTratamento</li><li>ExpressaoVocativo</li></ul> |

**Exemplo:**

```php
$objEntradaListarCargosAPI = new EntradaListarCargosAPI();
$objEntradaListarCargosAPI->setIdCargo(null); //listar todos
$objSeiRN = new SeiRN();
$arrObjCargoAPI = $objSeiRN->listarCargos($objEntradaListarCargosAPI);

Array (
  [0] =>CargoAPI Object (
    [IdCargo] =>100001843
    [ExpressaoCargo] =>Almirante da Marinha do Brasil
    [ExpressaoTratamento] =>A Sua Excelência o Senhor
    [ExpressaoVocativo] =>Senhor Almirante
  )
  [1] =>CargoAPI Object (
    [IdCargo] =>100001845
    [ExpressaoCargo] =>Chefe de Gabinete
    [ExpressaoTratamento] =>Ao Senhor
    [ExpressaoVocativo] =>Senhor Chefe de Gabinete
  )
  [2] =>CargoAPI Object (
    [IdCargo] =>100001846
    [ExpressaoCargo] =>Cidadão
    [ExpressaoTratamento] =>Ao Senhor
    [ExpressaoVocativo] =>Senhor
  )
  [3] =>CargoAPI Object (
    [IdCargo] =>100001847
    [ExpressaoCargo] =>Cônsul
    [ExpressaoTratamento] =>A Sua Excelência o Senhor
    [ExpressaoVocativo] =>Senhor Cônsul
    ...
  )
```

## listarCidades

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarCidadesAPI preenchidas com:<br><ul><li>IdPais</li><li>IdEstado</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto EstadoAPI preenchidas com:<br><ul><li>IdCidade</li><li>IdEstado</li><li>IdPais</li><li>Nome</li><li>CodigoIbge</li><li>SinCapital</li><li>Latitude</li><li>Longitude</li></ul> |

**Exemplo:**

```php
$objEntradaListarCidadesAPI = new EntradaListarCidadesAPI();
$objEntradaListarCidadesAPI->setIdPais(76); //Brasil
$objEntradaListarCidadesAPI->setIdEstado(2); //Acre

$objSeiRN = new SeiRN();
$arrObjCidadeAPI = $objSeiRN->listarCidades($objEntradaListarCidadesAPI);

Array (
  [0] =>CidadeAPI Object (
    [IdCidade] =>67
    [IdEstado] =>2
    [IdPais] =>76
    [Nome] =>Rio Branco
    [CodigoIbge] =>1200401
    [SinCapital] =>S
    [Latitude] =>-9,9783
    [Longitude] =>-67,81053
  )
  [1] =>CidadeAPI Object (
    [IdCidade] =>53
    [IdEstado] =>2
    [IdPais] =>76
    [Nome] =>Acrelândia
    [CodigoIbge] =>1200013
    [SinCapital] =>N
    [Latitude] =>-10,073794
    [Longitude] =>-67,052317
  )
  [2] =>CidadeAPI Object (
    [IdCidade] =>54
    [IdEstado] =>2
    [IdPais] =>76
    [Nome] =>Assis Brasil
    [CodigoIbge] =>1200054
    [SinCapital] =>N
    [Latitude] =>-10,942866
    [Longitude] =>-69,563459
  )
  ....
)
```

## listarContatos

| **Entrada** |
|---|
| Instância do objeto EntradaListarContatosAPI preenchidas com:<br><ul><li>IdContatos</li><li>IdTipoContato</li><li>PaginaRegistros (opcional 1 a 1000 com valor padrão 1)</li><li>PaginaAtual (opcional começando em 1)</li><li>Sigla</li><li>Nome</li><li>Cpf</li><li>Cnpj</li><li>Matricula</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto ContatoAPI preenchidas com:<br><ul><li>IdContato</li><li>IdTipoContato</li><li>NomeTipoContato</li><li>Sigla</li><li>Nome</li><li>NomeSocial</li><li>StaNatureza</li><li>IdContatoAssociado</li><li>NomeContatoAssociado</li><li>SinEnderecoAssociado</li><li>CnpjAssociado</li><li>Endereco</li><li>Complemento</li><li>Bairro</li><li>IdCidade</li><li>NomeCidade</li><li>IdEstado</li><li>SiglaEstado</li><li>IdPais</li><li>NomePais</li><li>Cep</li><li>StaGenero</li><li>IdCargo</li><li>ExpressaoCargo</li><li>ExpressaoTratamento</li><li>ExpressaoVocativo</li><li>Cpf</li><li>Cnpj</li><li>Rg</li><li>OrgaoExpedidor</li><li>Matricula</li><li>MatriculaOab</li><li>TelefoneFixo</li><li>TelefoneCelular</li><li>DataNascimento</li><li>Email</li><li>SitioInternet</li><li>Observação</li><li>NumeroPassaporte</li><li>IdPaisPassaporte</li><li>NomePaisPassaporte</li><li>SinAtivo</li></ul> |

**Exemplo:**

```php
//Ler todos os contatos de um tipo em grupos de 100 registros

$numPaginaAtual = 1;
$objEntradaListarContatosAPI = new EntradaListarContatosAPI();
$objEntradaListarContatosAPI->setIdTipoContato(1);
$objEntradaListarContatosAPI->setPaginaRegistros(100);
$objEntradaListarContatosAPI->setPaginaAtual($numPaginaAtual++);

$objSeiRN = new SeiRN();

$arrObjContatoAPI = $objSeiRN->listarContatos($objEntradaListarContatosAPI);

while(count($arrObjContatoAPI)){

  //processar contatos
  $objEntradaListarContatosAPI->setPaginaAtual($numPaginaAtual++);

  $arrObjContatoAPI = $objSeiRN->listarContatos($objEntradaListarContatosAPI);
};

$objEntradaListarContatosAPI = new EntradaListarContatosAPI();
$objEntradaListarContatosAPI->setIdTipoContato(1);

$objEntradaListarContatosAPI->setCpf(11572070730);


$objSeiRN = new SeiRN();
$arrObjContatoAPI = $objSeiRN->listarContatos($objEntradaListarContatosAPI);

Array (
  [0] =>ContatoAPI Object (
    [IdContato] =>100003924
    [IdTipoContato] =>1
    [NomeTipoContato] =>Autoridades
    [Sigla] =>def
    [Nome] =>Dddddd Eeeeee Ffffff
    [StaNatureza] =>F
    [IdContatoAssociado] =\>
    [NomeContatoAssociado] =\>
    [SinEnderecoAssociado] =>N
    [CnpjAssociado] =\>
    [Endereco] =>Rua Otávio Francisco Caruso da Rocha, 2000
    [Complemento] =\>
    [Bairro] =>Praia de Belas
    [IdCidade] =>4927
    [NomeCidade] =>Porto Alegre
    [IdEstado] =>23
    [SiglaEstado] =>RS
    [IdPais] =>76
    [NomePais] =>Brasil
    [Cep] =>90010-395
    [StaGenero] =>M
    [IdCargo] =>100001865
    [ExpressaoCargo] =>Diretor
    [ExpressaoTratamento] =>Ao Senhor
    [ExpressaoVocativo] =>Senhor Diretor
    [Cpf] =>11572070730
    [Cnpj] =\>
    [Rg] =>56584632
    [OrgaoExpedidor] =>SSP/RS
    [Matricula] =>54834
    [MatriculaOab] =\>
    [TelefoneFixo] =\>
    [TelefoneCelular] =>(99)9999-9999
    [DataNascimento] =>13/05/1971
    [Email] =>def@abc.gov.br
    [SitioInternet] =\>
    [Observacao] =\>
    [NumeroPassaporte] =\>
    [IdPaisPassaporte] =\>
    [NomePaisPassaporte] =\>
    [SinAtivo] =>S
  )
)
```

## listarEstados

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarEstadosAPI preenchidas com:<br><ul><li>IdPais</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto EstadoAPI preenchidas com:<br><ul><li>IdEstado</li><li>IdPais</li><li>Sigla</li><li>Nome</li><li>CodigoIbge</li></ul> |

**Exemplo:**

```php
$objEntradaListarEstadosAPI = new EntradaListarEstadosAPI();
$objEntradaListarEstadosAPI->setIdPais(76); //Brasil

$objSeiRN = new SeiRN();
$arrObjEstadoAPI = $objSeiRN->listarEstados($objEntradaListarEstadosAPI);

Array (
  [0] =>EstadoAPI Object (
    [IdEstado] =>2
    [IdPais] =>76
    [Sigla] =>AC
    [Nome] =>Acre
    [CodigoIbge] =>12
  )
  [1] =>EstadoAPI Object (
    [IdEstado] =>14
    [IdPais] =>76
    [Sigla] =>AL
    [Nome] =>Alagoas
    [CodigoIbge] =>27
  )
  [2] =>EstadoAPI Object (
    [IdEstado] =>3
    [IdPais] =>76
    [Sigla] =>AM
    [Nome] =>Amazonas
    [CodigoIbge] =>13
  )
  ...
)
```

## listarExtensoesPermitidas

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarExtensoesPermitidasAPI preenchidas com:<br><ul><li>IdArquivoExtensao</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto ArquivoExtensaoAPI preenchidas com:<br><ul><li>IdArquivoExtensao</li><li>Extensao</li><li>Descricao</li></ul> |

**Exemplo:**

```php
$objEntradaListarExtensoesPermitidasAPI = new EntradaListarExtensoesPermitidasAPI();
$objEntradaListarExtensoesPermitidasAPI->setIdArquivoExtensao(null); //lista todas

$objSeiRN = new SeiRN();
$arrObjArquivoExtensaoAPI = $objSeiRN->listarExtensoesPermitidas($objEntradaListarExtensoesPermitidasAPI);

Array (
  [0] =>ArquivoExtensaoAPI Object (
    [IdArquivoExtensao] =>1
    [Extensao] =>html
    [Descricao] =>Linguagem de Marcação de Hipertexto utilizada em
    páginas da Web
  )
  [1] =>ArquivoExtensaoAPI Object (
    [IdArquivoExtensao] =>14
    [Extensao] =>jpg
    [Descricao] =>Imagem
  )
  [2] =>ArquivoExtensaoAPI Object (
    [IdArquivoExtensao] =>6
    [Extensao] =>odt
    [Descricao] =>Texto com formatação (padrão aberto)
  )
  ...
)
```

## listarFeriados

| **Entrada** |
|---|
| Instâncias de EntradaListarFeriadosAPI preenchida com:<br><ul><li>IdOrgao</li><li>DataInicial</li><li>DataFinal</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto FeriadoAPI preenchidas com:<br><ul><li>Data</li><li>Descricao</li></ul> |

**Exemplo:**

```php
$objEntradaListarFeriadosAPI = new EntradaListarFeriadosAPI();
$objEntradaListarFeriadosAPI->setIdOrgao(1);
$objEntradaListarFeriadosAPI->setDataInicial('01/04/2017');
$objEntradaListarFeriadosAPI->setDataFinal('30/06/2017');
$objSeiRN = new SeiRN();
$arrObjFeriadoAPI = $objSeiRN->listarFeriados($objEntradaListarFeriadosAPI);

Array (
  [0] =>FeriadoAPI Object (
    [Data] =>14/04/2017
    [Descricao] =>Sexta-feira Santa
  )
  [1] =>FeriadoAPI Object (
    [Data] =>21/04/2017
    [Descricao] =>Tiradentes
  )
  [2] =>FeriadoAPI Object (
    [Data] =>01/05/2017
    [Descricao] =>Dia do Trabalho
  )
  [3] =>FeriadoAPI Object (
    [Data] =>15/06/2017
    [Descricao] =>Corpus Christi
  )
)
```

## listarHipotesesLegais

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarHipotesesLegaisAPI preenchidas com:<br><ul><li>NivelAcesso<ul><li>1 = Restrito</li><li>2 = Sigiloso</li></ul></li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto HipoteseLegalAPI preenchidas com:<br><ul><li>IdHipoteseLegal</li><li>Nome</li><li>BaseLegal</li><li>NivelAcesso</li></ul> |

**Exemplo:**

```php
$objEntradaListarHipotesesLegaisAPI = new EntradaListarHipotesesLegaisAPI();
$objEntradaListarHipotesesLegaisAPI->setNivelAcesso(null); //listar todas


$objSeiRN = new SeiRN();
$arrObjHipoteseLegalAPI = $objSeiRN->listarHipotesesLegais($objEntradaListarHipotesesLegaisAPI);

Array (
  [0] =>HipoteseLegalAPI Object (
    [IdHipoteseLegal] =>1
    [Nome] =>Hipótese A
    [BaseLegal] =>Lei 1.000
    [NivelAcesso] =>2
  )
  [1] =>HipoteseLegalAPI Object (
    [IdHipoteseLegal] =>10
    [Nome] =>Hipótese B
    [BaseLegal] =>Lei 2.000
    [NivelAcesso] =>1
  )
  [2] =>HipoteseLegalAPI Object (
    [IdHipoteseLegal] =>2
    [Nome] =>Hipótese C
    [BaseLegal] =>Lei 3.000
    [NivelAcesso] =>1
  )
  ...
)
```

## listarMarcadoresUnidade

| **Saída** |
|---|
| Conjunto de Instâncias do objeto MarcadorAPI preenchidas com:<br><ul><li>IdMarcador</li><li>Nome</li><li>Icone</li><li>SinAtivo</li></ul> |

**Exemplo:**

```php
$objSeiRN = new SeiRN();
$arrObjMarcadorAPI = $objSeiRN->listarMarcadoresUnidade();

Array (
  [0] =>MarcadorAPI Object (
    [IdMarcador] =>9
    [Nome] =>Marcador A
    [Icone] =\>
    data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wB/ACdeZVobAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAZklEQVR4nGP8X6/OQApgwSVx0HEmpqD9/nQm4lXjtAFZtf3+dDRBdBvwmI1FA0HVKE7CqhpTkIl4sxEaiFQNCQDswYpLNbEa4KqhGpD5+FUjbMClB1OcCY8cVlOYcKnAZScjqckbAEmjJZ7CtTvqAAAAAElFTkSuQmCC
    [SinAtivo] =>S
  )
  [1] =>MarcadorAPI Object (
    [IdMarcador] =>10
    [Nome] =>Marcador B
    [Icone] =\>
    data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wB/ACdeZVobAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAhUlEQVR4nJWSvRGAIAyFA8culi4QO0bJHi7CKHSwABNpgYcYYpRU8PhefriYY19gJtzbQ/ZhFDGSbMg+4LpxsSS5Qk9XCACaYj9zY6T+anUahmGcTo+KVWgx7E86l1SH4UPr9C9DT18GjNT+W6fvCqJnpB8tMY9IA1sNjJQhtbPYpJld7xPPmkUafFnHsgAAAABJRU5ErkJggg==  [SinAtivo] =>S
  )
  [2] =>MarcadorAPI Object (
    [IdMarcador] =>4
    [Nome] =>Marcador C
    [Icone] =\>
    data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wB/ACdeZVobAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAaklEQVR4nGP8X6/OQApgwSXxbu5fTEGhZGYm4lXjtAFZtVAyM5ogug14zMaigaBqFCdhVY0pyES82QgNRKqGBAD2YMWlmlgNcNVQDch8/KoRNuDSgynOhEcOqylMuFTgshM9LeH3DwMDAwBgvyGtI+3dDAAAAABJRU5ErkJggg==  [SinAtivo] =>S
  )
  ...
)
```

## listarPaises

| **Saída** |
|---|
| Conjunto de Instâncias do objeto PaisAPI preenchidas com:<br><ul><li>IdPais</li><li>Nome</li></ul> |

**Exemplo:**

```php
$objSeiRN = new SeiRN();
$arrObjPaisAPI = $objSeiRN->listarPaises();

Array (
  [0] =>PaisAPI Object (
    [IdPais] =>4
    [Nome] =>Afeganistão
  )
  [1] =>PaisAPI Object (
    [IdPais] =>710
    [Nome] =>África do Sul
  )
  [2] =>PaisAPI Object (
    [IdPais] =>8
    [Nome] =>Albânia
  )
  ...
)
```

## listarSeries

| **Saída** |
|---|
| Conjunto de Instâncias do objeto SerieAPI preenchidas com:<br><ul><li>IdSerie</li><li>Nome</li><li>Aplicabilidade</li></ul> |

**Exemplo:**

```php
$objSeiRN = new SeiRN();
$arrObjSerieAPI = $objSeiRN->listarSeries();

Array (
  [0] =>SerieAPI Object (
    [IdSerie] =>349
    [Nome] =>Abono de Faltas
    [Aplicabilidade] =>T
  )
  [1] =>SerieAPI Object (
    [IdSerie] =>475
    [Nome] =>Acórdão
    [Aplicabilidade] =>I
  )
  [2] =>SerieAPI Object (
    [IdSerie] =>293
    [Nome] =>Anexo
    [Aplicabilidade] =>E
  )
  ...
)
```

## listarTiposConferencia

| **Saída** |
|---|
| Conjunto de Instâncias do objeto TipoConferenciaAPI preenchidas com:<br><ul><li>IdTipoConferencia</li><li>Descricao</li></ul> |

**Exemplo:**

```php
$objSeiRN = new SeiRN();
$arrObjTipoConferenciaAPI = $objSeiRN->listarTiposConferencia();

Array (
  [0] =>TipoConferenciaAPI Object (
    [IdTipoConferencia] =>3
    [Descricao] =>Cópia autenticada administrativamente
  )
  [1] =>TipoConferenciaAPI Object (
    [IdTipoConferencia] =>2
    [Descricao] =>Cópia autenticada por cartório
  )
  [2] =>TipoConferenciaAPI Object (
    [IdTipoConferencia] =>4
    [Descricao] =>Cópia simples
  )
  [3] =>TipoConferenciaAPI Object (
    [IdTipoConferencia] =>1
    [Descricao] =>Documento Original
  )
)
```

## listarTiposProcedimento

| **Saída** |
|---|
| Conjunto de Instâncias do objeto TipoProcedimentoAPI preenchidas com:<br><ul><li>IdTipoProcedimento</li><li>Nome</li></ul> |

**Exemplo:**

```php
$objSeiRN = new SeiRN();
$arrObjTipoProcedimentoAPI = $objSeiRN->listarTiposProcedimento();

Array (
  [0] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000311
    [Nome] =>Abono de Faltas
  )
  [1] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000334
    [Nome] =>Abono Permanência
  )
  [2] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000258
    [Nome] =>Afastamentos
  )
  ...
)
```

## listarTiposProcedimentoOuvidoria

| **Saída** |
|---|
| Lista os tipos de processos sinalizados como de Ouvidoria retornando um conjunto de Instâncias do objeto TipoProcedimentoAPI preenchidas com:<br><ul><li>IdTipoProcedimento</li><li>Nome</li><li>SinOuvidoriaAnonimo</li></ul> |

**Exemplo:**

```php
$objSeiRN = new SeiRN();
$arrObjTipoProcedimentoAPI = $objSeiRN->listarTiposProcedimentoOuvidoria();

Array (
  [0] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000373
    [Nome] =>Acesso à Informação Pública
    [SinOuvidoriaAnonimo] =>N
  )
  [1] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000347
    [Nome] =>Elogio
    [SinOuvidoriaAnonimo] =>N
  )
  [2] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000348
    [Nome] =>Pedido de Informação
    [SinOuvidoriaAnonimo] =>N
  )
  [3] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000349
    [Nome] =>Pedido de Preferência
    [SinOuvidoriaAnonimo] =>N
  )
  [4] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000350
    [Nome] =>Reclamação/Denúncia
    [SinOuvidoriaAnonimo] =>S
  )
  [5] =>TipoProcedimentoAPI Object (
    [IdTipoProcedimento] =>100000351
    [Nome] =>Sugestão
    [SinOuvidoriaAnonimo] =>N
  )
)
```

## listarUnidades

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarUnidadesAPI preenchidas com:<br><ul><li>IdUnidade</li><li>IdOrgao</li><li>PalavrasPesquisa</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto UnidadeAPI preenchidas com:<br><ul><li>IdUnidade</li><li>Sigla</li><li>Descricao</li><li>SinProtocolo</li><li>SinArquivamento</li><li>SinOuvidoria</li></ul> |

**Exemplo:**

```php
$objEntradaListarUnidadesAPI = new EntradaListarUnidadesAPI();
$objEntradaListarUnidadesAPI->setIdOrgao(2);
$objEntradaListarUnidadesAPI->setPalavrasPesquisa('nucleo');

$objSeiRN = new SeiRN();
$arrObjUnidadeAPI = $objSeiRN->listarUnidades($objEntradaListarUnidadesAPI);

Array (
  [0] =>UnidadeAPI Object (
    [IdUnidade] =>110000274
    [Sigla] =>RSPOANCI
    [Descricao] =>Núcleo de Controle Interno
    [SinProtocolo] =>N
    [SinArquivamento] =>N
    [SinOuvidoria] =>N
  )
  [1] =>UnidadeAPI Object (
    [IdUnidade] =>110000290
    [Sigla] =>RSPOANDOC
    [Descricao] =>Núcleo de Documentação
    [SinProtocolo] =>N
    [SinArquivamento] =>S
    [SinOuvidoria] =>N
  )
  [2] =>UnidadeAPI Object (
    [IdUnidade] =>110000276
    [Sigla] =>RSPOANGF
    [Descricao] =>Núcleo de Gestão Funcional
    [SinProtocolo] =>N
    [SinArquivamento] =>N
    [SinOuvidoria] =>N
  )
  ...
)
```

## listarUsuarios

| **Entrada** |
|---|
| Conjunto de Instâncias do objeto EntradaListarUsuariosAPI preenchidas com:<br><ul><li>IdUsuario</li></ul> |
| **Saída** |
| Conjunto de Instâncias do objeto UsuarioAPI preenchidas com:<br><ul><li>IdUsuario</li><li>Sigla</li><li>Nome</li></ul> |

**Exemplo:**

```php
$objEntradaListarUsuariosAPI = new EntradaListarUsuariosAPI();
$objEntradaListarUsuariosAPI->setIdUsuario(null);

$objSeiRN = new SeiRN();
$arrObjUsuarioAPI = $objSeiRN->listarUsuarios($objEntradaListarUsuariosAPI);

Array (
  [0] =>UsuarioAPI Object (
    [IdUsuario] =>100008510
    [Sigla] =>abc
    [Nome] =>Aaaaaa Bbbbbb Cccccc
  )
  [1] =>UsuarioAPI Object (
    [IdUsuario] =>100011470
    [Sigla] =>def
    [Nome] =>Dddddd Eeeeee Ffffff
  )
  [2] =>UsuarioAPI Object (
    [IdUsuario] =>100008709
    [Sigla] =>ghi
    [Nome] =>Gggggg Hhhhhh Iiiiii
  )
  ...
)
```

## reabrirBloco

| **Entrada** |
|---|
| Instância do objeto EntradaReabrirBlocoAPI preenchida com:<br><ul><li>IdBloco</li></ul> |

**Exemplo:**

```php
$objEntradaReabrirBlocoAPI = new EntradaReabrirBlocoAPI();
$objEntradaReabrirBlocoAPI->setIdBloco(1195);

$objSeiRN = new SeiRN();
$objSeiRN->reabrirBloco($objEntradaReabrirBlocoAPI);
```

## reabrirProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaReabrirProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$objEntradaReabrirProcessoAPI = new EntradaReabrirProcessoAPI();
//$objEntradaReabrirProcessoAPI->setIdProcedimento();
$objEntradaReabrirProcessoAPI->setProtocoloProcedimento('0000262-95.2016.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->reabrirProcesso($objEntradaReabrirProcessoAPI);
```

## registrarAnotacao

| **Saída** |
|---|
| Conjunto de Instâncias do objeto EntradaRegistrarAnotacaoAPI preenchidas com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>Descricao</li><li>SinPrioridade</li></ul> |

**Exemplo:**

```php
$arrObjEntradaRegistrarAnotacaoAPI = array();
$objEntradaRegistrarAnotacaoAPI = new EntradaRegistrarAnotacaoAPI();

//$objEntradaRegistrarAnotacaoAPI->setIdProcedimento();
$objEntradaRegistrarAnotacaoAPI->setProtocoloProcedimento('12.1.000000989-5');
$objEntradaRegistrarAnotacaoAPI->setDescricao('Texto da Anotação');
$objEntradaRegistrarAnotacaoAPI->setSinPrioridade('N');
$arrObjEntradaRegistrarAnotacaoAPI[] = $objEntradaRegistrarAnotacaoAPI;
$objEntradaRegistrarAnotacaoAPI = new EntradaRegistrarAnotacaoAPI();
//$objEntradaRegistrarAnotacaoAPI->setIdProcedimento();
$objEntradaRegistrarAnotacaoAPI->setProtocoloProcedimento('10.1.000000470-0');
$objEntradaRegistrarAnotacaoAPI->setDescricao('Texto da Anotação');
$objEntradaRegistrarAnotacaoAPI->setSinPrioridade('S');
$arrObjEntradaRegistrarAnotacaoAPI[] = $objEntradaRegistrarAnotacaoAPI;
$objSeiRN = new SeiRN();
$objSeiRN->registrarAnotacao($arrObjEntradaRegistrarAnotacaoAPI);
```

## registrarOuvidoria

| **Entrada** |
|---|
| Instância do objeto EntradaRegistrarOuvidoriaAPI preenchida com:<br><ul><li>IdOrgao</li><li>Nome</li><li>NomeSocial</li><li>Email</li><li>Cpf (opcional se Rg/OrgaoExpedidor informados)</li><li>Rg (opcional se Cpf informado)</li><li>OrgaoExpedidor (opcional se Cpf informado)</li><li>Telefone</li><li>Estado</li><li>Cidade</li><li>IdTipoProcedimento</li><li>Processos</li><li>SinRetorno</li><li>Mensagem</li><li>AtributosAdicionais (opcional)</li></ul> |

**Exemplo:**

```php
$objEntradaRegistrarOuvidoriaAPI = new EntradaRegistrarOuvidoriaAPI();
$objEntradaRegistrarOuvidoriaAPI->setIdOrgao(1);
$objEntradaRegistrarOuvidoriaAPI->setNome('Fulano da Silva');
$objEntradaRegistrarOuvidoriaAPI->setNomeSocial(null);
$objEntradaRegistrarOuvidoriaAPI->setEmail('fulano.silva@abc.def.com');
$objEntradaRegistrarOuvidoriaAPI->setCpf('65292096032');
$objEntradaRegistrarOuvidoriaAPI->setRg(null);

$objEntradaRegistrarOuvidoriaAPI->setOrgaoExpedidor(null);
$objEntradaRegistrarOuvidoriaAPI->setTelefone('(51) 3322-9987');
$objEntradaRegistrarOuvidoriaAPI->setEstado('RS');
$objEntradaRegistrarOuvidoriaAPI->setCidade('Porto Alegre');

$objEntradaRegistrarOuvidoriaAPI->setIdTipoProcedimento(100000347);

$objEntradaRegistrarOuvidoriaAPI->setProcessos('12.1.000039131-9 e 0005689-15.2017.4.04.8000');
$objEntradaRegistrarOuvidoriaAPI->setSinRetorno('S');
$objEntradaRegistrarOuvidoriaAPI->setMensagem('Texto da mensagem do contato com a ouvidoria...');

$arrObjAtributoOuvidoriaAPI = array();
$objAtributoOuvidoriaAPI = new AtributoOuvidoriaAPI();
$objAtributoOuvidoriaAPI->setId('C');
$objAtributoOuvidoriaAPI->setNome('RELACAO');

$objAtributoOuvidoriaAPI->setTitulo('Relação com a Justiça Federal');
$objAtributoOuvidoriaAPI->setValor('Cidadão');

$arrObjAtributoOuvidoriaAPI[] = $objAtributoOuvidoriaAPI;

$objAtributoOuvidoriaAPI = new AtributoOuvidoriaAPI();
$objAtributoOuvidoriaAPI->setId('56');
$objAtributoOuvidoriaAPI->setNome('ORIGEM');
$objAtributoOuvidoriaAPI->setTitulo('Origem');
$objAtributoOuvidoriaAPI->setValor('Itália');
$arrObjAtributoOuvidoriaAPI[] = $objAtributoOuvidoriaAPI;
$objEntradaRegistrarOuvidoriaAPI->setAtributosAdicionais($arrObjAtributoOuvidoriaAPI);

$objSeiRN = new SeiRN();
$objProcedimentoResumidoAPI = $objSeiRN->registrarOuvidoria($objEntradaRegistrarOuvidoriaAPI);
ProcedimentoResumidoAPI Object (
  [IdProcedimento] =>42039220124158072
  [ProcedimentoFormatado] =>0055122-41.2019.4.04.8000
)
```

## relacionarProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaRelacionarProcessoAPI preenchida com:<br><ul><li>IdProcedimento1 ou ProtocoloProcedimento1</li><li>IdProcedimento2 ou ProtocoloProcedimento2</li></ul> |

**Exemplo:**

```php
$objEntradaRelacionarProcessoAPI = new EntradaRelacionarProcessoAPI();
//$objEntradaRelacionarProcessoAPI->setIdProcedimento1();
$objEntradaRelacionarProcessoAPI->setProtocoloProcedimento1('11.1.000000485-4');
//$objEntradaRelacionarProcessoAPI->setIdProcedimento2();
$objEntradaRelacionarProcessoAPI->setProtocoloProcedimento2('11.1.000000467-6');

$objSeiRN = new SeiRN();
$objSeiRN->relacionarProcesso($objEntradaRelacionarProcessoAPI);
```

## removerControlePrazo

| **Entrada** |
|---|
| Instâncias do objeto EntradaRemoverControlePrazoAPI preenchidas com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$arrObjEntradaRemoverControlePrazoAPI = array();
$objEntradaRemoverControlePrazoAPI = new EntradaRemoverControlePrazoAPI();
//$objEntradaRemoverControlePrazoAPI->setIdProcedimento();
$objEntradaRemoverControlePrazoAPI->setProtocoloProcedimento('11.1.000000485-4');
$arrObjEntradaRemoverControlePrazoAPI[] = $objEntradaRemoverControlePrazoAPI;
$objEntradaRemoverControlePrazoAPI = new EntradaRemoverControlePrazoAPI();
//$objEntradaRemoverControlePrazoAPI->setIdProcedimento();
$objEntradaRemoverControlePrazoAPI->setProtocoloProcedimento('11.1.000000467-6');
$arrObjEntradaRemoverControlePrazoAPI[] = $objEntradaRemoverControlePrazoAPI;
$objSeiRN = new SeiRN();
$objSeiRN->removerControlePrazo($arrObjEntradaRemoverControlePrazoAPI);
```

## removerRelacionamentoProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaRemoverRelacionamentoProcessoAPI preenchida com:<br><ul><li>IdProcedimento1 ou ProtocoloProcedimento1</li><li>IdProcedimento2 ou ProtocoloProcedimento2</li></ul> |

**Exemplo:**

```php
$objEntradaRemoverRelacionamentoProcessoAPI = new EntradaRemoverRelacionamentoProcessoAPI();
//$objEntradaRemoverRelacionamentoProcessoAPI->setIdProcedimento1();
$objEntradaRemoverRelacionamentoProcessoAPI->setProtocoloProcedimento1('11.1.000000485-4');
//$objEntradaRemoverRelacionamentoProcessoAPI->setIdProcedimento2();
$objEntradaRemoverRelacionamentoProcessoAPI->setProtocoloProcedimento2('11.1.000000467-6');

$objSeiRN = new SeiRN();
$objSeiRN->removerRelacionamentoProcesso($objEntradaRemoverRelacionamentoProcessoAPI);
```

## removerSobrestamentoProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaRemoverSobrestamentoProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$objEntradaRemoverSobrestamentoProcessoAPI = new EntradaRemoverSobrestamentoProcessoAPI();
//$objEntradaRemoverSobrestamentoProcessoAPI->setIdProcedimento();
$objEntradaRemoverSobrestamentoProcessoAPI->setProtocoloProcedimento('0000495-63.2014.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->removerSobrestamentoProcesso($objEntradaRemoverSobrestamentoProcessoAPI);
```

## retirarDocumentoBloco

| **Entrada** |
|---|
| Instância do objeto EntradaRetirarDocumentoBlocoAPI preenchida com:<br><ul><li>IdBloco</li><li>IdDocumento ou ProtocoloDocumento</li></ul> |

**Exemplo:**

```php
$objEntradaRetirarDocumentoBlocoAPI = new EntradaRetirarDocumentoBlocoAPI();
$objEntradaRetirarDocumentoBlocoAPI->setIdBloco(932);
//$objEntradaRetirarDocumentoBlocoAPI->setIdDocumento();
$objEntradaRetirarDocumentoBlocoAPI->setProtocoloDocumento('0011323');

$objSeiRN = new SeiRN();
$objSeiRN->retirarDocumentoBloco($objEntradaRetirarDocumentoBlocoAPI);
```

## retirarProcessoBloco

| **Entrada** |
|---|
| Instância do objeto EntradaRetirarProcessoBlocoAPI preenchida com:<br><ul><li>IdBloco</li><li>IdProcedimento ou ProtocoloProcedimento</li></ul> |

**Exemplo:**

```php
$objEntradaRetirarProcessoBlocoAPI = new EntradaRetirarProcessoBlocoAPI();
$objEntradaRetirarProcessoBlocoAPI->setIdBloco(777);
//$objEntradaRetirarProcessoBlocoAPI->setIdProcedimento();
$objEntradaRetirarProcessoBlocoAPI->setProtocoloProcedimento('0001570-06.2015.4.04.8000');

$objSeiRN = new SeiRN();
$objSeiRN->retirarProcessoBloco($objEntradaRetirarProcessoBlocoAPI);
```

## sobrestarProcesso

| **Entrada** |
|---|
| Instância do objeto EntradaSobrestarProcessoAPI preenchida com:<br><ul><li>IdProcedimento ou ProtocoloProcedimento</li><li>IdProcedimentoVinculado ou ProtocoloProcedimentoVinculado (opcional)</li><li>Motivo</li></ul> |

**Exemplo:**

```php
$objEntradaSobrestarProcessoAPI = new EntradaSobrestarProcessoAPI();
//$objEntradaSobrestarProcessoAPI->setIdProcedimento();
$objEntradaSobrestarProcessoAPI->setProtocoloProcedimento('0000495-63.2014.4.04.8000');
$objEntradaSobrestarProcessoAPI->setMotivo('Exemplo sobrestamento de processo módulo ABC');

$objSeiRN = new SeiRN();
$objSeiRN->sobrestarProcesso($objEntradaSobrestarProcessoAPI);
```
