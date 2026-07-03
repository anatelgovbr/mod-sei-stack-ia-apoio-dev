# Checklists Modulares SEI

Visoes operacionais por tema para revisao tecnica e security review de modulos
SEI/SIP.

## Regra de uso

- Estes arquivos nao substituem as fontes autoritativas do repositorio.
- Cada checklist modular reutiliza IDs e regras ja existentes em gates, matriz,
  skills e referencias.
- Em caso de conflito, prevalecem `AGENTS.md`,
  `.agents/references/gates-de-implementacao.md`,
  `.agents/security/matriz-vulnerabilidades-sei.md` e as skills de gate.

## Checklists disponiveis

| Tema | Arquivo | Quando usar | Fontes primarias |
|---|---|---|---|
| Permissoes | `checklist-permissoes-sei.md` | paginas, acoes, AJAX, WS, recursos SIP | `gates-de-implementacao.md`, `matriz-vulnerabilidades-sei.md`, `checklist-seguranca.md` |
| RN e transacoes | `checklist-rn-transacoes-sei.md` | `*RN.php`, escrita em BD, pos-commit | `AGENTS.md`, `sei-verificacao-rn`, `matriz-vulnerabilidades-sei.md` |
| Modelagem de dados | `checklist-modelagem-dados-sei.md` | revisao transversal de modelagem, release e multi-SGBD | `padrao-modelagem-dados.md`, `sei-verificacao-banco-dados`, `gates-de-implementacao.md` |
| DTO InfraPHP | `checklist-dto-infraphp-sei.md` | `*DTO.php`, joins relacionados, PK/FK | `padrao-modelagem-dados.md`, `sei-verificacao-banco-dados` |
| BD, DDL e release | `checklist-bd-ddl-sei.md` | `*BD.php`, scripts DDL, release SEI/SIP | `padrao-modelagem-dados.md`, `padrao-scripts-release.md`, `gates-de-implementacao.md` |

## Ponto de entrada recomendado

- Para revisao ampla: `.agents/checklists/checklist-seguranca.md`
- Para PR: `.agents/security/guia-security-review-pr.md`
- Para validacao tecnica de entrega: `.specify/templates/checklist-sei-template.md`
