# Proteção das dependências entre módulo e core

## Acionamento e alcance

Ao criar ou alterar referência física ou dependência funcional de módulo sobre registro persistido do core, avalie seu ciclo de vida antes da implementação. Inclua Administração, protocolos de processos e documentos e demais entidades para as quais SeiIntegracao exponha eventos pertinentes. A presença de um método na API não comprova que ele permita veto. Examine também mudança de uso em RN sem novo DTO ou DDL. O alcance é a dependência afetada pela demanda, sem exigir saneamento de todo o legado.

## Procedimento e matriz de cobertura

1. Inventarie as dependências afetadas por DTO, RN, scripts de instalação e documentação funcional. `configurarFK` é metadado de relacionamento, não prova de constraint física. Confirme a FK no DDL/script da versão suportada, sua direção, colunas e política de exclusão; declare quando a evidência for somente estrutural ou funcional.
2. Registre uma linha por dependência e operação na matriz abaixo. Separe exclusão, eliminação, desativação e demais transições relevantes. Considere caminhos internos, serviços e tarefas que realmente executam a operação, não apenas a tela.
3. Defina a política pela regra documentada: vetar, permitir, limpar ou desvincular. FK restritiva que permanecer exige prevenção antes da tentativa de remoção. Histórico e configurações inativas ainda podem conservar a FK. Desativação não viola a FK por si só: identifique quando o uso funcional exige registro ativo. Cascata ou nulificação não autorizam perda de dados sem regra conhecida. Pergunte somente a decisão de negócio ainda desconhecida.
4. Localize o evento em SeiIntegracao e leia o método chamador do core. Comprove assinatura, objeto único ou array, atributos preenchidos, posição em relação a cada escrita relevante e commit, alcance e encadeamento da exceção. Uma referência a registro filho removido antes do evento também pode falhar antes da interceptação do registro principal. Registre arquivo, método, linhas e versão examinada.
5. Classifique a eficácia: antes da escrita; depois da escrita dentro da transação, com rollback demonstrado; depois do commit; inexistente; ou tarde para alcançar a FK. Se o DELETE falhar antes do evento, rollback não torna o evento alcançável. Exija alternativa oficial comprovada ou proposta de evolução do core; não declare cobertura nem faça patch automático no core. Não capture erro SQL genérico para convertê-lo em recusa de negócio.
6. Implemente hook pequeno que delega à RN do módulo. Consulte referências por DTO/BD em lote com OPER_IN quando o contrato receber arrays. Objetos únicos continuam únicos; agrupe relacionados e evite consultas por item. Lance InfraException::lancarValidacao ou adicionarValidacao seguido de lancarValidacoes; propague a crítica até o tratamento transacional. Retornar false não substitui o veto por exceção. Escrita de limpeza segue os padrões transacionais do projeto; efeitos externos somente após commit.
7. Confira autorização e saída: o administrador autorizado no core pode não ter recurso de navegação/listagem do módulo. Use helper interno adequado ao hook, sem exigir permissão secundária indevida ou liberar acesso a informações restritas. Preserve o veto e mostre apenas nomes/contexto autorizados. Não enfraqueça permissões dos métodos públicos existentes.
8. Quando permitir a desativação, confira o fluxo inverso em cadastrar, alterar, reativar, importar e outros caminhos que tornem a dependência operante. Valide o estado novo enviado, sem bloquear correções legítimas por associações antigas removidas. Avalie concorrência entre criação do vínculo e remoção/mudança de estado; transação e IN não eliminam a corrida. Se relevante, comprove bloqueio e ordem de aquisição coerentes, sem impor lock universal.
9. Verifique a matriz e os testes antes da entrega. Nenhuma dependência afetada fica sem decisão explícita; aprovação de auditor estrutural ou presença de hook não comprovam eficácia. Pendência em dependência nova/ampliada impede declarar sua proteção concluída. Passivo não ampliado e fora do escopo é relatado separadamente.

| Dependência e fonte física/funcional | Uso e regra conhecida | Operação/caminho | Política e motivo | Evento/contrato | Callsite, escrita, commit e versão | Autorização e fluxo inverso | Teste e resultado |
|---|---|---|---|---|---|---|---|
| tabela.coluna → entidade do core | ativo, inativo ou histórico | excluir/eliminar/desativar/... | vetar/permitir/limpar/desvincular | objeto ou array, atributos | evidência por operação | contexto do chamador e ativação | verificado/pendente/sem evento eficaz |

## Estrutura da crítica

Adapte entidade, ação e concordância ao cenário. Identifique módulo e funcionalidade; use dois-pontos, uma linha em branco e lista simples de nomes dos registros causadores do impedimento. Não obrigue ID nem bloco “Utilização” por item. Informações de associação só entram quando necessárias, conhecidas e autorizadas, por exemplo os tipos de processos que usam uma série documental. Ordene de forma estável e elimine repetições por identidade/contexto, sem fundir registros distintos só por terem nomes iguais. Não inclua itens livres do lote.

```text
<Estes/Estas/Este/Esta> <entidade(s)> não <podem/pode> ser <ação>, pois são utilizados pelo módulo <nome>, na funcionalidade <funcionalidade>:

   - <nome do registro 1>
   - <nome do registro 2>
   - <nome do registro N>
```

Exemplo de preenchimento:

```text
Estes Tipos de Documento não podem ser excluídos, pois são utilizados pelo módulo <nome>, na funcionalidade <funcionalidade>:

   - <nome do tipo de documento 1>
   - <nome do tipo de documento 2>
   - <nome do tipo de documento N>
```

Ajuste também “são utilizados” ao gênero e número da entidade. Use quebras de linha reais no contrato de apresentação e o tratamento de saída existente do SEI, sem concatenar HTML aos nomes. Confira a renderização. Completude é por módulo/evento: SeiIntegracao::executar encadeia a primeira exceção; não promete agregação global de todos os módulos. Não altere mensagens legadas fora do escopo para padronizá-las.

## Verificação

- Teste sem vínculo, com vínculo, com configuração inativa, com histórico e cada bloco de associação. Quando houver lote, coloque o item usado depois de um item livre, inclua vários usados e associações repetidas. Confira somente os causadores e a mensagem literal.
- Teste os caminhos inversos, inclusive salvamento que reative implicitamente e correção que remova dependência antiga. Confira permissão negada e administrador do core sem navegação no módulo, com registro livre e usado; não exponha detalhes restritos.
- Exercite o método real do core com FK física em ambiente descartável e confira crítica esperada, ausência de erro SQL e rollback integral. Invocação direta do hook e doubles isolados não provam alcance do evento nem comportamento do banco. Separe exclusão e eliminação; confira caminhos alternativos e concorrência relevante.
- Testes unitários novos seguem AGENTS.md e padrao-testes-phpunit.md: caminho espelhado, AAA, DataProvider e red/green com defeito no comportamento testado. Registre comandos, resultados e verificações pendentes; não use banco do usuário como fixture descartável.

## Exemplos locais e limites

- PeticionamentoIntegracao::excluirDocumento e MdPetPiTpProcessoRN::validarExclusaoDocumentoModelo: veto do Modelo por Protocolo. excluirProcesso e excluirDocumentoPeticionamentoInterno mostram limpeza legítima de registros dependentes, não veto universal por FK.
- MdPetPiTpProcessoRN::validarOperacaoTipoDocumento e _validarReativacao: união dos três blocos e proteção inversa. Confira os recursos de leitura exigidos no perfil real, em vez de presumir autorização.
- PENIntegracao lista registros e distingue operações, mas contém consultas por item. LitigiosoIntegracao e CorreiosIntegracao têm caminhos que usam só o primeiro elemento do lote. Esses detalhes não são gabaritos.
- O catálogo informa referências do checkout examinado; valide novamente o core das versões suportadas. Para entidades sem evento eficaz, preserve a lacuna na matriz.
