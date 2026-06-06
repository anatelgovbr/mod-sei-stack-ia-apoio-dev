# Checklist rápido de segurança para módulos SEI

1. **Permissão**
   - Há validação explícita para cada ação sensível?
   - Use `validarPermissao($recurso)` ou `verificarPermissao($recurso)` (retorna bool, não lança erro).
   - Use `validarAuditarPermissao($recurso, __METHOD__, $valores)` quando a ação deve gerar **trilha de auditoria**.
     - Se o recurso estiver em regra de auditoria no SIP: grava na tabela `infra_auditoria`.
     - Se não estiver: faz apenas validação de permissão (sem gravar auditoria).
   - **Regra de decisão**: ações que alteram dados sensíveis, consultam CPF/CNPJ ou impactam processo/documento
     devem usar `validarAuditarPermissao`. Ações de leitura simples podem usar `validarPermissao`.
2. **Sessão e link**
   - O fluxo valida sessão e assinatura de link?
   - Links externos/sem assinatura são permitidos somente via whitelist/regex estrita (negar por padrão)?
2.1 **SSRF / Open redirect**
   - Não aceitar URLs arbitrárias vindas do usuário (GET/POST/headers) para redirecionamento, fetch, iframe, callback ou “link sem assinatura”.
   - Para qualquer URL permitida: aplicar whitelist (scheme/host/path) e validação por regex estrita; negar por padrão.
3. **Entrada**
   - Entradas de `GET/POST` são validadas e normalizadas?
4. **Saída**
   - Valores refletidos em HTML/JS usam funções de escape apropriadas?
5. **Banco**
   - Operações seguem padrões do framework (DTO/RN/BD), evitando SQL inseguro?
   - Nunca concatenar entradas em SQL (sem “string building” com GET/POST).
6. **Auditoria**
   - Eventos críticos geram trilha/auditoria quando aplicável?
7. **Exposição indevida**
   - Não há vazamento de dados sigilosos por mensagens, logs ou endpoints?
   - Logs não incluem segredos (tokens/senhas/chaves) nem PII; quando necessário, mascarar/anonymizar.
8. **Autorização em AJAX**
   - Em `processarControladorAjax` / `processarControladorAjaxExterno`, cada ação possui validação explícita de autorização?
9. **Contrato de parâmetros**
   - Evitar `$_REQUEST`; usar `PaginaSEI::POST/GET` com normalização de tipo (ex.: `int`, `int[]`, enum)?
10. **Dados sensíveis**
   - Ações de consulta por CPF/CNPJ/contato têm restrição por perfil e trilha de auditoria?