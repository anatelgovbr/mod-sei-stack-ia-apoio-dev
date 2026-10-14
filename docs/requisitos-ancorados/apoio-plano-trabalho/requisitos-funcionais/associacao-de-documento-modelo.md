# Associação de documento modelo

O administrador do módulo associa a cada item de etapa de plano de trabalho um documento de editor interno que serve de modelo para os documentos gerados a partir do item. A tela fica em Administração > Apoio a Plano de Trabalho.

Fora do escopo: criar, editar ou versionar o documento modelo, que é um documento comum do SEI; associar modelo a documento que não vem de plano de trabalho.

Regras de negócio: [regras-de-negocio.md](../regras-de-negocio.md).

## Listar

### RF-APT-001: Listar planos de trabalho ativos

Quando o administrador do módulo abrir a tela Administração > Apoio a Plano de Trabalho, o sistema deve listar os planos de trabalho ativos em ordem alfabética.

- Verificação: teste manual, cenário RF-APT-001.C1.
- Cenário: RF-APT-001.C1 Planos ativos em ordem alfabética
  - Dado os planos de trabalho ativos "Beta" e "Alfa" e o plano inativo "Gama"
  - Quando o administrador abrir a tela Apoio a Plano de Trabalho
  - Então a lista mostra "Alfa" e "Beta", nessa ordem
  - E o plano "Gama" não aparece

### RF-APT-002: Listar etapas e itens do plano

Quando o administrador do módulo escolher um plano de trabalho, o sistema deve listar as etapas ativas do plano e os itens ativos de cada etapa, em ordem, com o protocolo do documento modelo associado a cada item ou um traço para o item sem associação.

- Verificação: teste manual, cenários RF-APT-002.C1 a RF-APT-002.C3.
- Cenário: RF-APT-002.C1 Itens com e sem associação
  - Dado um plano com uma etapa ativa que tem um item associado e um item sem associação
  - Quando o administrador escolher o plano
  - Então as etapas e os itens aparecem na ordem definida no plano
  - E o item associado mostra o protocolo do documento modelo
  - E o item sem associação mostra um traço
- Cenário: RF-APT-002.C2 Etapa e item inativos
  - Dado um plano com uma etapa inativa e uma etapa ativa que tem um item inativo
  - Quando o administrador escolher o plano
  - Então a etapa inativa e o item inativo não aparecem
- Cenário: RF-APT-002.C3 Plano sem etapa ativa
  - Dado um plano de trabalho sem etapa ativa
  - Quando o administrador escolher o plano
  - Então a lista não mostra etapas nem itens

### RF-APT-019: Mostrar só as ações permitidas

Enquanto o usuário não tiver a permissão de uma operação do módulo, o sistema deve ocultar na listagem a ação correspondente.

- Verificação: teste manual, cenário RF-APT-019.C1.
- Cenário: RF-APT-019.C1 Usuário só com permissão de listar
  - Dado um usuário com permissão de listar e sem permissão de associar, alterar e excluir
  - Quando ele escolher um plano de trabalho
  - Então a listagem mostra os itens e os protocolos associados
  - E não mostra as ações de associar, alterar e excluir

## Cadastrar e alterar

### RF-APT-003: Associar documento modelo a item de etapa

Quando o administrador do módulo informar o protocolo de um documento modelo válido para um item de etapa sem associação, o sistema deve criar a associação entre o item e o documento.

- Verificação: teste manual, cenário RF-APT-003.C1.
- Cenário: RF-APT-003.C1 Associação de documento modelo válido
  - Dado um item de etapa sem associação
  - E um documento de editor interno acessível pela unidade do administrador
  - Quando o administrador associar o protocolo desse documento ao item
  - Então a listagem mostra o protocolo do documento na linha do item

### RF-APT-004: Abrir a alteração quando o item já tem associação

Se o administrador do módulo abrir o cadastro de associação para um item de etapa que já tem associação, então o sistema deve apresentar a alteração da associação existente.

- Verificação: teste manual, cenário RF-APT-004.C1.
- Cenário: RF-APT-004.C1 Cadastro aberto para item já associado
  - Dado um item de etapa com documento modelo associado
  - Quando o administrador abrir o cadastro de associação para esse item
  - Então a tela apresentada é a de alteração da associação existente

### RF-APT-005: Recusar segunda associação para o mesmo item

Se o administrador do módulo tentar cadastrar associação para um item de etapa que já tem associação, então o sistema deve recusar o cadastro e informar que o item já tem associação.

- Verificação: teste manual, cenário RF-APT-005.C1.
- Cenário: RF-APT-005.C1 Dois cadastros abertos para o mesmo item
  - Dado um item de etapa sem associação
  - E dois formulários de cadastro abertos para esse item
  - Quando o administrador salvar um documento modelo válido no primeiro e depois no segundo
  - Então o segundo cadastro é recusado com o aviso de que o item já tem associação
  - E o item fica associado ao documento do primeiro cadastro

### RF-APT-006: Trocar o documento modelo de uma associação

Quando o administrador do módulo informar o protocolo de outro documento modelo válido para uma associação existente, o sistema deve trocar o documento modelo da associação e manter o item de etapa.

- Verificação: teste manual, cenários RF-APT-006.C1 e RF-APT-006.C2.
- Cenário: RF-APT-006.C1 Troca por documento modelo válido
  - Dado um item associado ao documento modelo A
  - Quando o administrador alterar a associação para o documento modelo válido B
  - Então o item passa a mostrar o protocolo do documento B
- Cenário: RF-APT-006.C2 Troca recusada mantém o modelo anterior
  - Dado um item associado ao documento modelo A
  - Quando o administrador alterar a associação para um documento que não é modelo válido
  - Então a alteração é recusada com o motivo
  - E o item continua associado ao documento A

### RF-APT-010: Abrir o formulário em janela

Quando o administrador do módulo acionar a associação ou a alteração na listagem, o sistema deve abrir o formulário em janela sobre a listagem.

- Verificação: teste manual, cenários RF-APT-010.C1 e RF-APT-010.C2.
- Cenário: RF-APT-010.C1 Associação em janela
  - Dado um item de etapa sem associação
  - Quando o administrador acionar a associação do item na listagem
  - Então o formulário de associação abre em janela sobre a listagem
- Cenário: RF-APT-010.C2 Alteração em janela
  - Dado um item de etapa associado a um documento modelo
  - Quando o administrador acionar a alteração do item na listagem
  - Então o formulário de alteração abre em janela sobre a listagem

### RF-APT-011: Atualizar a listagem depois de salvar

Quando o administrador do módulo salvar a associação na janela, o sistema deve fechar a janela e recarregar a listagem com o novo estado.

- Verificação: teste manual, cenário RF-APT-011.C1; caso indesejado em RF-APT-020.
- Cenário: RF-APT-011.C1 Gravação na janela
  - Dado o formulário de associação de um item aberto em janela
  - Quando o administrador salvar um documento modelo válido
  - Então a janela fecha
  - E a listagem mostra o protocolo do documento na linha do item

### RF-APT-020: Manter a janela aberta quando a gravação é recusada

Se a gravação da associação na janela for recusada, então o sistema deve manter a janela aberta com o motivo da recusa.

- Verificação: teste manual, cenário RF-APT-020.C1.
- Cenário: RF-APT-020.C1 Gravação recusada na janela
  - Dado o formulário de associação de um item aberto em janela
  - Quando o administrador salvar um protocolo que não é de documento modelo válido
  - Então a janela continua aberta com o motivo da recusa
  - E a listagem não muda

## Validar o protocolo

### RF-APT-008: Recusar protocolo vazio

Se o protocolo informado estiver vazio, então o sistema deve recusar o protocolo sem procurar o documento.

- Verificação: teste manual, cenário RF-APT-008.C1.
- Cenário: RF-APT-008.C1 Gravação sem protocolo
  - Dado o formulário de associação de um item de etapa
  - Quando o administrador salvar sem informar o protocolo
  - Então o sistema pede o protocolo do documento modelo
  - E nenhuma associação é gravada

### RF-APT-021: Limitar o protocolo a 50 caracteres

O sistema deve aceitar no máximo 50 caracteres no protocolo do documento modelo.

- Verificação: teste manual, cenário RF-APT-021.C1.
- Cenário: RF-APT-021.C1 Protocolo no limite de tamanho
  - Dado o formulário de associação de um item de etapa
  - Quando o administrador digitar 51 caracteres no protocolo
  - Então o campo fica com os primeiros 50 caracteres

### RF-APT-009: Recusar documento que não é modelo válido

Se o protocolo informado não corresponder a documento modelo válido, então o sistema deve recusar o protocolo e informar o motivo.

- Verificação: teste manual, cenários RF-APT-009.C1 a RF-APT-009.C5.
- Cenário: RF-APT-009.C1 Protocolo de documento externo
  - Dado um item de etapa sem associação
  - Quando o administrador informar o protocolo de um documento externo
  - Então o sistema informa que só documento de editor interno é aceito
  - E nenhuma associação é gravada
- Cenário: RF-APT-009.C2 Protocolo que não é de documento
  - Dado um item de etapa sem associação
  - Quando o administrador informar um protocolo inexistente ou de processo
  - Então o sistema informa que o documento não foi encontrado
  - E nenhuma associação é gravada
- Cenário: RF-APT-009.C3 Documento sigiloso
  - Dado um item de etapa sem associação
  - Quando o administrador informar o protocolo de um documento sigiloso
  - Então o sistema informa que o documento não foi encontrado
  - E nenhuma associação é gravada
- Cenário: RF-APT-009.C4 Documento cancelado
  - Dado um item de etapa sem associação
  - Quando o administrador informar o protocolo de um documento cancelado
  - Então o sistema informa que o documento foi cancelado
  - E nenhuma associação é gravada
- Cenário: RF-APT-009.C5 Documento sem acesso para a unidade
  - Dado um item de etapa sem associação
  - Quando o administrador informar o protocolo de um documento que a unidade dele não acessa
  - Então o sistema informa que a unidade não possui acesso ao documento
  - E nenhuma associação é gravada

## Excluir

### RF-APT-007: Excluir associação

Quando o administrador do módulo excluir a associação de um item na listagem e confirmar, o sistema deve remover a associação.

- Verificação: teste manual, cenários RF-APT-007.C1 e RF-APT-007.C3.
- Cenário: RF-APT-007.C1 Exclusão de uma associação
  - Dado um item associado a um documento modelo
  - Quando o administrador excluir a associação do item e confirmar
  - Então o item passa a mostrar um traço no protocolo modelo
- Cenário: RF-APT-007.C3 Exclusão não confirmada
  - Dado um item associado a um documento modelo
  - Quando o administrador acionar a exclusão da associação e não confirmar
  - Então o item continua associado
