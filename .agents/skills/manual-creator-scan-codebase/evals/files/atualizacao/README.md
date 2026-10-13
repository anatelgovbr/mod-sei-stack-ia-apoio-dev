# Cenários fictícios de preservação

Os dados servem para avaliar a skill, sem representar normas, sistemas implantados ou recomendações reais. Execute os prompts de `evals/evals.json` em cópias isoladas, com a skill anterior e com a candidata. Preserve o estado inicial antes de cada caso. Resultados, diffs, relatórios e ferramentas da execução ficam no workspace de avaliação, fora desta skill.

| Cenário | Preocupações cobertas | Conferência principal |
|---|---|---|
| 5 | T1, T2, T3, T9, T11 | Manual estável e conhecimento externo intactos |
| 6 | T1, T7, T8, T11 | Complemento humano misturado com alteração funcional |
| 7 | T4, T5, T6, T7, T11 | Tela nova, campo novo, retirada comprovada e escopo por público |
| 8 | T1, T3, T9, T11 | Legado, fonte incompleta e ausência de histórico |
| 9 | T1, T2, T3, T8, T11 | Revisão editorial autorizada e equivalência de sentido |
| 10 | T10 | Entrevista e, após resposta, três públicos escolhidos |

Para a segunda interação do cenário 10, o responsável confirma: "Quero três manuais separados: Administração, Usuário Interno e Usuário Externo. Use os perfis correspondentes do README, os slugs manual-pedidos-administracao, manual-pedidos-usuario-interno e manual-pedidos-usuario-externo e o destino padrão com imagens locais. Pode preparar e registrar o adaptador e criar os três manuais. Os prints serão coletados depois."

Compare bytes dos trechos sem autorização editorial, confira o mérito dos parágrafos autorizados e examine cada mudança do diff contra código, autorização e causa estrutural. Um hash não avalia equivalência semântica. O verificador da skill também não avalia mérito ou validade jurídica; prints reais e renderização continuam dependentes de evidência própria.
