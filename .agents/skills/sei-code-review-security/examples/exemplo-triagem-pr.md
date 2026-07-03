# Exemplo de Triagem — PR ficticio

Exemplo de saida da skill `sei-code-review-security` sobre um PR hipotetico.
Serve apenas como referencia de formato e nivel de detalhe — nao e um caso real.

## Contexto do PR
Modulo `relacionamento-institucional`. Adiciona:
- `rn/MdRiRestauranteRN.php`: novo metodo `listarPorCidadeControlado()`
- `restaurante_lista.php`: novo botao de acao "exportar"

## Saida

```
## Triagem
Tipo: menu/pagina + RN · Arquivos: 2 · Camadas: pagina, rn
Gates acionados: sei-verificacao-pagina, sei-verificacao-rn, sei-testes-validacao
Escopo: OK (dentro de modulos/**)

## Bloqueantes
- [BLOQUEANTE][introduzido] restaurante_lista.php:42 — acao "exportar" sem validarPermissao()
  apos validarLink() (V02 / gate G3)

## Riscos relevantes
- [ALTA][introduzido] MdRiRestauranteRN.php:88 — metodo de leitura nomeado "Controlado";
  operacao read deveria usar sufixo "Conectado" (sei-verificacao-rn T1)

## Duplicacao / reaproveitamento
- listarPorCidadeControlado() — ja existe listarConectado() com criterio de
  cidade na mesma RN (linha 51). U1 ALTA: usar o metodo existente com criterio
  em vez de criar um novo. Pergunta: essa funcao precisa existir?

## Qualidade
- Testes: novo metodo `listarPorCidadeControlado()` sem cobertura PHPUnit — adicionar antes do merge
- [BAIXA][introduzido] nomes claros, sem codigo morto; complexidade ok; sem N+1

## Seguranca
- [BLOQUEANTE][introduzido] restaurante_lista.php:42 — acao "exportar" sem validarPermissao()
  apos validarLink() (V02 / gate G3)

## Impacto SEI
- Banco/release: sem DDL novo, sem impacto de script
- Permissoes/SIP: acao "exportar" exige recurso md_ri_exportar (definir)
- Multi-SGBD: sem risco
- Transacao: metodo de leitura, sem efeito colateral

## Recomendacoes
1. Adicionar validarPermissao('md_ri_exportar') na acao (bloqueante).
2. Reusar listarConectado() com criterio cidade; remover o metodo novo.
3. Se o metodo novo for mantido, renomear para sufixo Conectado.

## Veredito
**bloquear merge** (1 BLOQUEANTE aberto: V02 em restaurante_lista.php:42)
```
