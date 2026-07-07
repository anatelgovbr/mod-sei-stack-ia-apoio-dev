# 2. Criação e Ativação

Os códigos-fonte do módulo de exemplo ABC estão disponíveis no diretório `sei/config/modulo_exemplo` (ver arquivo **instrucoes.txt**).

Siga os passos básicos para a criação de um módulo:

a)  criar diretório dentro do diretório já existente de módulos do sistema (`sei/web/modulos`), um diretório opcional para identificar a instituição e o diretório que identifica o módulo de fato.


![](../manual_desenvolvimento/imagens/image002.jpg)

b)  criar uma classe que estenda a classe `SeiIntegracao` do core do SEI e implemente os métodos `getNome`, `getVersao` e `getInstituicao`. Exemplo:

```php
class AbcExemploIntegracao extends SeiIntegracao{

  public function getNome(){
    return 'Módulo de exemplos ABC';
  }

  public function getVersao() {
    return '1.0.0';
  }

  public function getInstituicao(){
    return 'TRF4 - Tribunal Regional Federal da 4ª Região';
  }
}
```

A classe acima exemplificada deve ser salva em um arquivo com o mesmo nome. No exemplo acima, ficaria `AbcExemploIntegracao.php`.

c)  adicionar no arquivo de configuração do sistema `ConfiguracaoSEI.php` na chave `Modulos` a referência para o nome da classe e para o diretório onde ela se encontra:

```php
  'SEI' => array(....
                'Modulos' => array('AbcExemploIntegracao' => 'abc/exemplo')
                ),
```
d)  verificar se o módulo foi carregado por meio do menu Infra/Módulos do SEI:


![](../manual_desenvolvimento/imagens/image003.png)
