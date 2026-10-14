# Geração com documento modelo

Quando um usuário gera documento de editor interno a partir de um item de etapa com documento modelo associado, o conteúdo principal do documento gerado passa a ser o conteúdo principal do modelo.

Fora do escopo: documento externo e formulário; documento gerado antes da associação; atualização do documento gerado quando o modelo muda depois da geração; reescrita de links e âncoras do conteúdo copiado, que continuam apontando para o processo do modelo.

Regras de negócio: [regras-de-negocio.md](../regras-de-negocio.md).

## Aplicar o modelo

### RF-APT-012: Aplicar o conteúdo do modelo ao documento gerado

Quando um usuário gerar documento de editor interno a partir de item de etapa com associação, o sistema deve substituir o conteúdo da seção principal do documento gerado pelo conteúdo da versão vigente da seção principal do documento modelo.

- Verificação: teste manual, cenários RF-APT-012.C1 a RF-APT-012.C4.
- Cenário: RF-APT-012.C1 Geração com modelo acessível
  - Dado um item de etapa com documento modelo associado
  - E um usuário cuja unidade tem acesso ao modelo
  - Quando o usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo principal do modelo
- Cenário: RF-APT-012.C2 Modelo alterado depois da associação
  - Dado um item de etapa com documento modelo associado
  - E o conteúdo do modelo alterado depois da associação
  - Quando um usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo atual do modelo
- Cenário: RF-APT-012.C3 Item sem associação
  - Dado um item de etapa sem documento modelo associado
  - Quando um usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo inicial do SEI
- Cenário: RF-APT-012.C4 Documento que não é de editor interno
  - Dado um item de etapa com documento modelo associado
  - Quando um usuário gerar a partir do item um documento que não é de editor interno
  - Então o documento não é alterado pelo módulo

### RF-APT-013: Manter as demais seções

Quando substituir o conteúdo do documento gerado, o sistema deve manter as seções diferentes da seção principal como o SEI as criou.

- Verificação: teste manual, cenário RF-APT-013.C1.
- Cenário: RF-APT-013.C1 Cabeçalho e rodapé preservados
  - Dado um item de etapa com documento modelo associado
  - E um tipo de documento com cabeçalho e rodapé
  - Quando um usuário gerar documento desse tipo a partir do item
  - Então o cabeçalho e o rodapé são os criados pelo SEI
  - E só o corpo do documento vem do modelo

### RF-APT-014: Registrar a substituição como nova versão

Quando substituir o conteúdo do documento gerado, o sistema deve criar nova versão da seção principal e manter no histórico a versão criada pelo SEI.

- Verificação: teste manual, cenário RF-APT-014.C1.
- Cenário: RF-APT-014.C1 Histórico com duas versões
  - Dado um item de etapa com documento modelo associado
  - Quando um usuário gerar documento de editor interno a partir do item
  - Então o histórico do documento tem duas versões
  - E a primeira versão é a criada pelo SEI

### RF-APT-015: Registrar a autoria da nova versão

Quando substituir o conteúdo do documento gerado, o sistema deve registrar na nova versão o usuário e a unidade da sessão que gerou o documento.

- Verificação: teste manual, cenário RF-APT-015.C1.
- Cenário: RF-APT-015.C1 Autoria da versão do modelo
  - Dado um item de etapa com documento modelo associado
  - Quando um usuário gerar documento de editor interno a partir do item
  - Então a nova versão do documento registra o usuário e a unidade de quem gerou

### RF-APT-016: Registrar a autoria sem sessão de usuário

Se não houver sessão de usuário no momento da substituição, então o sistema deve registrar na nova versão o usuário e a unidade da versão criada pelo SEI.

- Verificação: inspeção de código.

### RF-APT-018: Aplicar o modelo sem exigir permissão do módulo

O sistema deve aplicar o documento modelo sem exigir do usuário gerador as permissões do módulo.

- Verificação: teste manual, cenário RF-APT-018.C1.
- Cenário: RF-APT-018.C1 Usuário sem permissões do módulo
  - Dado um item de etapa com documento modelo associado
  - E um usuário sem as permissões do módulo cuja unidade tem acesso ao modelo
  - Quando o usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo principal do modelo

## Gerar sem o modelo

### RF-APT-017: Gerar sem o modelo quando ele não é válido para o usuário

Se o documento modelo não for válido para a unidade do usuário gerador, então o sistema deve gerar o documento sem o conteúdo do modelo.

- Verificação: teste manual, cenários RF-APT-017.C1 a RF-APT-017.C3.
- Cenário: RF-APT-017.C1 Usuário sem acesso ao modelo
  - Dado um item de etapa com documento modelo associado
  - E um usuário cuja unidade não tem acesso ao modelo
  - Quando o usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo inicial do SEI
  - E o histórico do documento tem uma versão só
- Cenário: RF-APT-017.C2 Modelo cancelado depois da associação
  - Dado um item de etapa associado a um documento modelo que foi cancelado
  - Quando um usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo inicial do SEI
- Cenário: RF-APT-017.C3 Modelo que passou a sigiloso
  - Dado um item de etapa associado a um documento modelo que passou a sigiloso
  - Quando um usuário gerar documento de editor interno a partir do item
  - Então o documento abre com o conteúdo inicial do SEI
