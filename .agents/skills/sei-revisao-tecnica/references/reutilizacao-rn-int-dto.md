# Reaproveitamento Técnico em RN / INT / DTO

A skill `sei-revisao-tecnica` aplica esta referência quando o escopo cria ou
altera função, método ou classe em RN, INT ou DTO. O objetivo é detectar
duplicação estrutural, acoplamento e posicionamento técnico inadequado.

Esta verificação não interpreta requisito, especificação, regra de negócio ou
produto. Similaridade que dependa de semântica funcional não é achado técnico.

## Checklist U1-U10

| ID | Verificação observável | Severidade técnica | Referência |
|---|---|---|---|
| U1 | Existe implementação estruturalmente equivalente na mesma classe? | ALTA | evidência em ambos os métodos |
| U2 | Existe implementação estruturalmente equivalente em RN, INT ou DTO relacionado? | MEDIA | evidência em ambos os arquivos |
| U3 | A dependência respeita as camadas RN, INT, DTO, página e operação? | ALTA | `sei-verificacao-rn` T3/T5 |
| U4 | Nome e sufixo seguem os contratos `Controlado`, `Conectado` e recursos `md_<sigla>_*`? | MEDIA | `sei-verificacao-rn` T1 |
| U5 | Há bloco de orquestração, validação técnica ou transformação literalmente repetido? | MEDIA | trechos e linhas comparadas |
| U6 | SQL cru pode ser substituído por DTO e critérios já disponíveis? | ALTA | matriz V05 |
| U7 | Há acoplamento a página, sessão, entrada HTTP ou superglobal em camada interna? | ALTA | matriz V06 |
| U8 | A visibilidade pública, protegida ou privada é a mínima exigida pelos chamadores observados? | MEDIA | chamadores localizados |
| U9 | A adição amplia superfície de permissão, transação, release ou multi-SGBD? | conforme gate | gates aplicáveis |
| U10 | Existe contrato oficial de core ou API com a mesma operação técnica e tipos compatíveis? | MEDIA | `sei-mod-api-classes` |

## Busca mínima

1. Inspecione a própria classe e seus chamadores.
2. Inspecione RN, INT e DTO relacionados no mesmo módulo.
3. Consulte os catálogos de `sei-mod-api-classes`, `sei-mod-api-operacoes` e
   `sei-mod-api-eventos` quando houver integração com o core.
4. Consulte `.agents/references/padrao-codificacao-php.md` e
   `.agents/references/padrao-modelagem-dados.md` para contratos técnicos.

## Evidência e decisão

- Cite `arquivo:linha` para a implementação nova e para o equivalente.
- Demonstre equivalência por assinatura, tipos, montagem de DTO, critérios,
  chamadas e fluxo técnico. Não presuma equivalência pelo nome.
- Se a equivalência depender de intenção funcional, não emita achado. Registre a
  verificação como inconclusiva apenas se ela impedir outra conclusão técnica.
- Classe interna do core não é achado por si só. Registre somente risco atual de
  segurança, transação, compatibilidade suportada ou contrato API/WS violado.
- Sem equivalente localizado, informe apenas que a busca técnica não encontrou
  duplicação. Isso não prova necessidade funcional.

Classifique cada achado como `introduzido`, `ampliado`, `preexistente` ou
`incerto`. Duplicação preexistente sem agravamento permanece `WARN` e pode gerar
candidato a tarefa, sem bloquear o parecer atual.
