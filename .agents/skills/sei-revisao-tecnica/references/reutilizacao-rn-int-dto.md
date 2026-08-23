# Reaproveitamento Tecnico em RN / INT / DTO

A skill `sei-revisao-tecnica` aplica esta referencia quando o escopo cria ou
altera funcao, metodo ou classe em RN, INT ou DTO. O objetivo e detectar
duplicacao estrutural, acoplamento e posicionamento tecnico inadequado.

Esta verificacao nao interpreta requisito, especificacao, regra de negocio ou
produto. Similaridade que dependa de semantica funcional nao e achado tecnico.

## Checklist U1-U10

| ID | Verificacao observavel | Severidade tecnica | Referencia |
|---|---|---|---|
| U1 | Existe implementacao estruturalmente equivalente na mesma classe? | ALTA | evidencia em ambos os metodos |
| U2 | Existe implementacao estruturalmente equivalente em RN, INT ou DTO relacionado? | MEDIA | evidencia em ambos os arquivos |
| U3 | A dependencia respeita as camadas RN, INT, DTO, pagina e operacao? | ALTA | `sei-verificacao-rn` T3/T5 |
| U4 | Nome e sufixo seguem os contratos `Controlado`, `Conectado` e recursos `md_<sigla>_*`? | MEDIA | `sei-verificacao-rn` T1 |
| U5 | Ha bloco de orquestracao, validacao tecnica ou transformacao literalmente repetido? | MEDIA | trechos e linhas comparadas |
| U6 | SQL cru pode ser substituido por DTO e criterios ja disponiveis? | ALTA | matriz V05 |
| U7 | Ha acoplamento a pagina, sessao, entrada HTTP ou superglobal em camada interna? | ALTA | matriz V06 |
| U8 | A visibilidade publica, protegida ou privada e a minima exigida pelos chamadores observados? | MEDIA | chamadores localizados |
| U9 | A adicao amplia superficie de permissao, transacao, release ou multi-SGBD? | conforme gate | gates aplicaveis |
| U10 | Existe contrato oficial de core ou API com a mesma operacao tecnica e tipos compativeis? | MEDIA | `sei-mod-api-classes` |

## Busca minima

1. Inspecione a propria classe e seus chamadores.
2. Inspecione RN, INT e DTO relacionados no mesmo modulo.
3. Consulte os catalogos de `sei-mod-api-classes`, `sei-mod-api-operacoes` e
   `sei-mod-api-eventos` quando houver integracao com o core.
4. Consulte `.agents/references/padrao-codificacao-php.md` e
   `.agents/references/padrao-modelagem-dados.md` para contratos tecnicos.

## Evidencia e decisao

- Cite `arquivo:linha` para a implementacao nova e para o equivalente.
- Demonstre equivalencia por assinatura, tipos, montagem de DTO, criterios,
  chamadas e fluxo tecnico. Nao presuma equivalencia pelo nome.
- Se a equivalencia depender de intencao funcional, nao emita achado. Registre a
  verificacao como inconclusiva apenas se ela impedir outra conclusao tecnica.
- Classe interna do core nao e achado por si so. Registre somente risco atual de
  seguranca, transacao, compatibilidade suportada ou contrato API/WS violado.
- Sem equivalente localizado, informe apenas que a busca tecnica nao encontrou
  duplicacao. Isso nao prova necessidade funcional.

Classifique cada achado como `introduzido`, `ampliado`, `preexistente` ou
`incerto`. Duplicacao preexistente sem agravamento permanece `WARN` e pode gerar
candidato a tarefa, sem bloquear o parecer atual.
