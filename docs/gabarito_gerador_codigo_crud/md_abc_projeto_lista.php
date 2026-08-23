<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/



try {
  require_once __DIR__ . '/SEI.php';


  session_start();

  //////////////////////////////////////////////////////////////////////////////
  //InfraDebug::getInstance()->setBolLigado(false);
  //InfraDebug::getInstance()->setBolDebugInfra(true);
  //InfraDebug::getInstance()->limpar();
  //////////////////////////////////////////////////////////////////////////////

  SessaoSEI::getInstance()->validarLink();

  SessaoSEI::getInstance()->validarPermissao($_GET['acao']);

  PaginaSEI::getInstance()->prepararSelecao('md_abc_projeto_selecionar');

  switch ($_GET['acao']) {
    case 'md_abc_projeto_excluir':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcProjetoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcProjetoDTO = new MdAbcProjetoDTO();
          $objMdAbcProjetoDTO->setNumIdMdAbcProjeto($strId);
          $arrObjMdAbcProjetoDTO[] = $objMdAbcProjetoDTO;
        }
        $objMdAbcProjetoRN = new MdAbcProjetoRN();
        $objMdAbcProjetoRN->excluir($arrObjMdAbcProjetoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_projeto_desativar':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcProjetoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcProjetoDTO = new MdAbcProjetoDTO();
          $objMdAbcProjetoDTO->setNumIdMdAbcProjeto($strId);
          $arrObjMdAbcProjetoDTO[] = $objMdAbcProjetoDTO;
        }
        $objMdAbcProjetoRN = new MdAbcProjetoRN();
        $objMdAbcProjetoRN->desativar($arrObjMdAbcProjetoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_projeto_reativar':
      $strTitulo = 'Reativar Projetos';
      if (PaginaSEI::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcProjetoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcProjetoDTO = new MdAbcProjetoDTO();
          $objMdAbcProjetoDTO->setNumIdMdAbcProjeto($strId);
          $arrObjMdAbcProjetoDTO[] = $objMdAbcProjetoDTO;
        }
        $objMdAbcProjetoRN = new MdAbcProjetoRN();
        $objMdAbcProjetoRN->reativar($arrObjMdAbcProjetoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_projeto_selecionar':
      $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar Projeto','Selecionar Projetos');

      //Se cadastrou alguem
      if (PaginaSEI::GET('acao_origem')==='md_abc_projeto_cadastrar' && isset($_GET['id_md_abc_projeto'])) {
        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('id_md_abc_projeto'));
      }
      break;

    case 'md_abc_projeto_listar':
      $strTitulo = 'Projetos';
      break;

    default:
      throw new InfraException("Ação '".PaginaSEI::GET('acao')."' não reconhecida.");
  }

  $arrComandos = array();
  if (PaginaSEI::GET('acao')==='md_abc_projeto_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  if (PaginaSEI::GET('acao')==='md_abc_projeto_listar' || PaginaSEI::GET('acao')==='md_abc_projeto_selecionar') {
    $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNovo" value="Novo" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_projeto_cadastrar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ovo</button>';
    }
  }

  $objMdAbcProjetoDTO = new MdAbcProjetoDTO();
  $objMdAbcProjetoDTO->retNumIdMdAbcProjeto();
  $objMdAbcProjetoDTO->retStrIdentificacao();
  //$objMdAbcProjetoDTO->retStrDescricao();
  //$objMdAbcProjetoDTO->retDtaCadastramento();

  if (PaginaSEI::GET('acao')==='md_abc_projeto_reativar') {
    //Lista somente inativos
    $objMdAbcProjetoDTO->setBolExclusaoLogica(false);
    $objMdAbcProjetoDTO->adicionarCriterio(array('SinAtivo'), array(InfraDTO::$OPER_IGUAL), array('N'));
  }

  PaginaSEI::getInstance()->prepararOrdenacao($objMdAbcProjetoDTO, 'Identificacao', InfraDTO::$TIPO_ORDENACAO_ASC);
  //PaginaSEI::getInstance()->prepararPaginacao($objMdAbcProjetoDTO);

  $objMdAbcProjetoRN = new MdAbcProjetoRN();
  $arrObjMdAbcProjetoDTO = $objMdAbcProjetoRN->listar($objMdAbcProjetoDTO);

  //PaginaSEI::getInstance()->processarPaginacao($objMdAbcProjetoDTO);

  /** @var MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO */

  $numRegistros = count($arrObjMdAbcProjetoDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (PaginaSEI::GET('acao')==='md_abc_projeto_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
    } elseif (PaginaSEI::GET('acao')==='md_abc_projeto_reativar') {
      $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_reativar');
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_excluir');
      $bolAcaoDesativar = false;
    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_excluir');
      $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_projeto_desativar');
    }

    
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_projeto_desativar&acao_origem='.PaginaSEI::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_projeto_reativar&acao_origem='.PaginaSEI::GET('acao').'&acao_confirmada=sim');
    }
    

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_projeto_excluir&acao_origem='.PaginaSEI::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    if (PaginaSEI::GET('acao')!=='md_abc_projeto_reativar') {
      $strCaptionTabela = 'Projetos';
    } else {
      $strCaptionTabela = 'Projetos Inativos';
    }

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.PaginaSEI::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.PaginaSEI::getInstance()->getThCheck().'</th>'."\n";
    }
    $strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcProjetoDTO,'Identificação','Identificacao',$arrObjMdAbcProjetoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcProjetoDTO,'Descrição','Descricao',$arrObjMdAbcProjetoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcProjetoDTO,'Data de Início','Cadastramento',$arrObjMdAbcProjetoDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">Ações</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObjMdAbcProjetoDTO[$i]->getNumIdMdAbcProjeto(),$arrObjMdAbcProjetoDTO[$i]->getStrIdentificacao()).'</td>';
      }
      $strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcProjetoDTO[$i]->getStrIdentificacao()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcProjetoDTO[$i]->getStrDescricao()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcProjetoDTO[$i]->getDtaCadastramento()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcProjetoDTO[$i]->getNumIdMdAbcProjeto());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_projeto_consultar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_projeto='.$arrObjMdAbcProjetoDTO[$i]->getNumIdMdAbcProjeto()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeConsultar().'" title="Consultar Projeto" alt="Consultar Projeto" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_projeto_alterar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_projeto='.$arrObjMdAbcProjetoDTO[$i]->getNumIdMdAbcProjeto()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeAlterar().'" title="Alterar Projeto" alt="Alterar Projeto" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcProjetoDTO[$i]->getNumIdMdAbcProjeto();
        $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObjMdAbcProjetoDTO[$i]->getStrIdentificacao());
      }

      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeDesativar().'" title="Desativar Projeto" alt="Desativar Projeto" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeReativar().'" title="Reativar Projeto" alt="Reativar Projeto" class="infraImg" /></a>&nbsp;';
      }


      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeExcluir().'" title="Excluir Projeto" alt="Excluir Projeto" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (PaginaSEI::GET('acao')==='md_abc_projeto_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

} catch (Exception $e) {
  PaginaSEI::getInstance()->processarExcecao($e);
}

PaginaSEI::getInstance()->montarDocType();
PaginaSEI::getInstance()->abrirHtml();
PaginaSEI::getInstance()->abrirHead();
PaginaSEI::getInstance()->montarMeta();
PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema().' - '.($strTitulo??false));
PaginaSEI::getInstance()->montarStyle();
PaginaSEI::getInstance()->abrirStyle();
?>
<?php if(0){?><style><?php }?>
<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_projeto_selecionar') {
    infraReceberSelecao();
    document.getElementById('btnFecharSelecao').focus();
  } else {
    document.getElementById('btnFechar').focus();
  }
  infraEfeitoTabelas(true);
}

<?php if ($bolAcaoDesativar??false) { ?>
function acaoDesativar(id,desc)
{
  if (confirm('Confirma desativação do Projeto \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcProjetoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcProjetoLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Projeto selecionado.');
    return;
  }
  if (confirm('Confirma desativação dos Projetos selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcProjetoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcProjetoLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativação do Projeto \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcProjetoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcProjetoLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Projeto selecionado.');
    return;
  }
  if (confirm('Confirma reativação dos Projetos selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcProjetoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcProjetoLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusão do Projeto \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcProjetoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcProjetoLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Projeto selecionado.');
    return;
  }
  if (confirm('Confirma exclusão dos Projetos selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcProjetoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcProjetoLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcProjetoLista" method="post" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
  <?php
  PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
  //PaginaSEI::getInstance()->abrirAreaDados('5em');
  //PaginaSEI::getInstance()->fecharAreaDados();
  PaginaSEI::getInstance()->montarAreaTabela($strResultado??false,$numRegistros??false);
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
