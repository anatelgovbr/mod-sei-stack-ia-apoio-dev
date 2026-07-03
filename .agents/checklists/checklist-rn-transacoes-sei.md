# Checklist de RN e Transacoes SEI

Checklist operacional para revisar `*RN.php`, isolamento de camadas, transacoes
e efeitos colaterais em modulos SEI/SIP.

## Fontes de verdade

- `AGENTS.md` - `Padrao Transacional Obrigatorio`, `Guardrails Universais`
- `.agents/skills/sei-verificacao-rn/SKILL.md` - `T1-T5`
- `.agents/security/matriz-vulnerabilidades-sei.md` - `V07`
- `.agents/checklists/checklist-seguranca.md` - secoes `1.3`, `1.6`

## Quando usar

- qualquer alteracao em `*RN.php`
- revisao de escrita em BD
- operacoes com email, Solr, indexacao ou integracao externa

## Checklist operacional

| # | Item | Origem | Severidade |
|---|---|---|---|
| 1 | A RN implementa `inicializarObjInfraIBanco()` e retorna o banco correto | `T2` | BLOQUEANTE |
| 2 | A RN acessa apenas sua propria BD; quando precisar outra entidade, delega para outra RN ou explicita excecao consciente | `T3` | BLOQUEANTE |
| 3 | Metodos CRUD seguem o sufixo esperado quando aplicavel: escrita `Controlado`, leitura `Conectado` | `T1` | AVISO |
| 4 | Controle manual de conexao ou transacao esta contextualizado e nao conflita com o ciclo do `InfraRN` | `T4` | AVISO |
| 5 | Efeitos colaterais irreversiveis ficam fora da transacao critica e rodam apos a persistencia | `V07`, `E2` | ALTA |
| 6 | Excecoes preservam contexto com `InfraException` encadeada quando o metodo faz orchestracao relevante | `T5` (padrao recorrente nos exemplos do manual) | AVISO |
| 7 | Escrita critica registra auditoria e nao depende apenas da pagina para proteger a operacao | `L3` | ALTA |

## Sinais de risco comuns

- RN instanciando `OutraEntidadeBD` diretamente
- email ou integracao externa dentro de metodo `*Controlado`
- `abrirTransacao()` com varios retornos intermediarios sem clareza
- validacao de permissao comentada em metodos de escrita
