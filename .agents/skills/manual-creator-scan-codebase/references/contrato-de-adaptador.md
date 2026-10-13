# Contrato de adaptador

O adaptador traduz as convenções comprovadas do repositório para a investigação do manual. Ele localiza evidências; não cria regras de negócio nem substitui a entrevista. Os caminhos que declara são relativos à raiz do repositório de uso, salvo insumos locais expressamente indicados.

## Entrevista e seleção

Antes de fechar o adaptador, extraia as respostas já fornecidas e investigue pistas locais. Pergunte somente o que continuar materialmente indeterminado:

- Qual sistema ou módulo e quais tarefas entram no manual?
- Quem vai usá-lo, com quais objetivos, conhecimentos e permissões?
- Qual versão ou revisão, idioma e configuração da interface serão documentados?
- Onde o Markdown será lido, qual renderizador será usado e qual logo representa o sistema?
- Há manual anterior, capturas atuais, documentação funcional ou ambiente autorizado para conferir recursos dinâmicos? Quem fará a coleta manual dos prints pendentes?

Compare nome, caminhos e componentes do alvo com o reconhecimento dos adaptadores em `../registro-adaptadores.md`. Um candidato único e comprovado pode ser selecionado; candidatos concorrentes exigem inspeção discriminante e, se necessário, escolha do responsável. Sem candidato, crie o adaptador por entrevista e scan de descoberta. Em pedido de verificação, a ausência dele permite somente conclusões independentes das convenções desconhecidas, sem escrita.

Inspecione a cadeia de uma tarefa representativa, incluindo apresentação e regra chamada, para provar que os pontos de leitura são adequados. A varredura completa do manual vem depois do adaptador, não durante a descoberta. Use `rg --files` para localizar candidatos e `rg -n` para referências quando disponíveis; confirme o conteúdo com a codificação encontrada. Não trate falta de resultado em UTF-8 como ausência de texto em código de outra codificação.

## Grupos obrigatórios

Preencha cada grupo com evidência local ou resposta identificada da entrevista. Declare `não aplicável` com motivo quando a capacidade não existir. Um item desconhecido que afete escopo, permissões, interpretação de tela ou publicação é pendência, não valor padrão.

| Grupo | Conteúdo obrigatório |
|---|---|
| Reconhecimento e alcance | Nome oficial, pistas de inclusão e exclusão, sistema ou módulo, fronteiras e componentes compartilhados |
| Versão e variante | Fontes de versão ou revisão, configuração e recursos habilitados, idioma da interface e como conferir a correspondência com o material fornecido |
| Leitura da codebase | Raízes, extensões, codificação por fonte, exclusões comprovadas e ferramentas disponíveis; não excluir dependência que forneça comportamento no alcance sem rastrear sua contribuição |
| Pontes de evidência | Como conectar entidades ou objetos, contratos, rotas, menus, componentes, campos, serviços, regras, permissões e testes; identificadores e estratégias concretas de busca; como comprovar o caminho visível de acesso à tela sem confundi-lo com rota ou arquivo técnico |
| Interface e textos | Onde localizar labels, botões, opções, críticas, mensagens, ajudas, ícones acessíveis, traduções, interpolação, textos vindos de banco ou serviço e estados condicionais; como rastrear menus, abas, ações, modais e variantes por persona para orientar os prints |
| Personas e acesso | Objetivos, tarefas, familiaridade relevante, termos de negócio, papéis ou perfis de acesso relacionados e fonte da relação; incertezas que exijam entrevista |
| Publicação e recursos | Pasta de publicação, pasta de imagens e slug do manual, manual anterior, logo e outras imagens aprovadas, fonte e tratamento de dados sensíveis; renderizador, apresentação do aviso Markdown, comportamento de âncoras, padrão de geração das capturas e coleta manual pelo responsável |
| Validação e limites | Checks locais, observação de interface disponível e autorizada, caminhos para evidência complementar, lacunas e condições de bloqueio; data ou revisão da última conferência |

O adaptador declara a pasta de publicação e a pasta de imagens dos manuais. Ao criá-lo, registre o destino padrão de [formato-manual.md](formato-manual.md), salvo outra escolha do responsável; mudança de destino se faz no adaptador, não na skill. Se não existir versão de produto, identifique a revisão examinada e as alterações locais incluídas, em vez de fabricar uma versão. Código-fonte disponível não prova qual versão está implantada.

Na amostra de descoberta, demonstre como localizar a tela e comprovar seu caminho pelos nomes visíveis, com persona e condição de acesso. Se houver somente rota técnica ou trecho de navegação indeterminado, registre esse limite. O adaptador define o método e remete ao aviso de [formato-manual.md](formato-manual.md); o plano de posições para todas as capturas só nasce na varredura funcional posterior. Preparar somente o adaptador não autoriza escrever o manual nem inserir avisos nele.

## Personas e permissões

Persona representa um grupo de pessoas com objetivos e necessidades de leitura. Papel ou perfil representa uma condição de acesso implementada. Registre a relação entre ambos, sem equipará-los: uma persona pode ter mais de um perfil, e um perfil pode atender várias personas.

| Persona ou público | Objetivo e tarefas | Conhecimento relevante | Perfil e restrições | Fonte e confirmação |
|---|---|---|---|---|

Use grupos de público conhecidos no sistema ou informados pelo responsável. A inferência de um nome de perfil é pista para a entrevista, não persona confirmada. Não invente idade, profissão, experiência ou permissão. Um público único é suficiente quando comprovado; mantenha a tabela mesmo nesse caso. Regras de autorização vêm da implementação e da configuração efetiva, e não apenas de um botão oculto.

## Criação e composição

Crie `adapters/<slug_do_alvo>.md` dentro da skill instalada. Use slug com letras minúsculas sem acento, números e hífens, sem separadores de caminho. Preencha o esqueleto abaixo com conteúdo concreto antes de registrar o alvo.

```markdown
# Adaptador: <nome oficial do alvo>

## Reconhecimento e alcance

## Versão e variante

## Leitura da codebase

## Pontes de evidência

## Interface e textos

## Personas e acesso

## Publicação e recursos

## Validação e limites
```

Somente extraia uma base compartilhada quando duas adaptações reais demonstrarem as mesmas convenções. O adaptador declara o caminho da base e cada exceção; grupos não preenchidos nem herdados explicitamente continuam faltantes. Não crie antecipadamente famílias de frameworks e não copie os adaptadores SEI para um alvo de outra codebase.

Registre o nome, o link para o arquivo e as pistas de reconhecimento e alcance na tabela de `../registro-adaptadores.md` apenas após completar o contrato. O comportamento de entrevista, varredura, formato e verificação permanece nas referências gerais.

## Revalidação e atualização

A cada execução, abra o adaptador e confira reconhecimento, fontes correntes de versão ou revisão, caminhos, codificações, pontos de leitura da interface, traduções e perfis. Registre a conferência e os resultados no relatório da execução. Se houver divergência de convenção, ajuste o adaptador antes da escrita do manual; em verificação, relate a divergência sem ajustá-lo.

Uma mudança funcional com as mesmas convenções não exige reconstruir o adaptador: confirme sua validade e siga a cadeia afetada, inclusive chamadores, textos, permissões, configurações e testes. Se a diferença não puder ser delimitada pelo histórico, compare todo o alcance do manual com as fontes atuais e reporte esse alcance maior de conferência. Isso não autoriza reescrever conteúdo ainda correto.
