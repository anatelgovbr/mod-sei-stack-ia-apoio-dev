# 6. Padrão de Codificação PHP

## Nomes de Arquivos

Devem possuir apenas letras minúsculas, números e o caractere sublinhado acrescidos da extensão *.`php`*.

Classes ou interfaces devem utilizar arquivos individuais. Nesse caso, o nome do arquivo deve ser obrigatoriamente o mesmo nome da classe ou da interface acrescido da extensão *.`php`*.

## Indentação

Deve utilizar DOIS a QUATRO espaços para cada nível de indentação. **Não deve utilizar tabulação**.

## Classes e Interfaces

- Nomes de classe devem ser substantivos no singular tendo como prefixo Md e a sigla da instituição:
  - `MdAbcPedido`, `MdAbcItem`
- Utilizar a primeira letra de cada palavra em maiúscula:
  - `MdAbcNotaFiscal`
- Não deve utilizar preposições:
  - `MdAbcRequisicaoPagamento`

## Instâncias de Classes

- Para nomear instâncias de classes utilize o prefixo ***obj*** seguido do nome da classe:
  - `objMdAbcPedido`, `objMdAbcRequisicaoPagamento`
- Se for necessário utilizar mais de uma instância da mesma classe utilize um sufixo descritivo:
  - `objMdAbcPedidoOriginal`, `objMdAbcPedidoReclassificado`

## Constantes

- Devem ser declaradas com todas as letras em maiúsculo:
  - `MD_ABC_FATOR`
- Termos compostos devem ser separados pelo caractere sublinhado:
  - `MD_ABC_CONSUMO_MINIMO`

## Atributos e Variáveis de Métodos

Os atributos e variáveis devem ser nomeados utilizando um prefixo e um qualificador. O prefixo é definido de acordo com o tipo do atributo e o qualificador deve descrever o melhor possível o seu significado dentro da lógica do sistema. O qualificador deve conter a primeira letra em maiúscula e as demais em minúsculas. Termos compostos devem utilizar a primeira letra de cada termo em maiúscula e as demais em minúsculas (**não deve utilizar o caractere sublinhado**):

| Tipo do Atributo | Prefixo | Exemplo |
|---|---|---|
| Número | num | numIdadeMinima |
| String | str | strNome |
| Data | dta | dtaNascimento |
| Data/Hora | dth | dthEntrega |
| Array | arr | arrObjProtocolo |
| Booleano | bol | bolEncontrouUnidade |

## Métodos

Os nomes dos métodos devem ser verbos no infinitivo e conter apenas letras minúsculas. Termos compostos devem utilizar a primeira letra do segundo termo em diante em maiúscula (**não deve utilizar o caractere sublinhado**):

- `cadastrar`

- `calcularJuros`

- `gerarEstatisticas`

## Elementos HTML

Os elementos HTML devem ser nomeados utilizando um prefixo e um qualificador. O prefixo é definido de acordo com a tabela abaixo e o qualificador deve descrever o propósito do componente contendo a primeira letra em maiúscula e as demais em minúsculas. Termos compostos devem utilizar a primeira letra de cada termo em maiúscula e as demais em minúsculas (**não deve utilizar o caractere sublinhado**):

| Elemento | Prefixo | Exemplo |
|---|---|---|
| [input type=] text | txt | txtNome |
| [input type=] password | pwd | pwdSenha |
| [input type=] checkbox | chk | chkUnidadeProtocolo |
| [input type=] radio | rdo | rdoNivelAcesso |
| [input type=] submit | sbm | sbmSalvar |
| [input type=] file | fil | filAnexo |
| [input type=] hidden | hdn | hdnIdCidade |
| [input type=] image | img | imgLupa |
| [input type=] button | btn | btnFechar |
| Form | frm | frmAnotacaoCadastro |
| Div | div | divEndereco |
| Table | tbl | tblLocalizadores |
| iFrame | ifr | ifrmArvore |
| TextArea | txa | txaDescricao |
| Select | sel | selUnidades |
