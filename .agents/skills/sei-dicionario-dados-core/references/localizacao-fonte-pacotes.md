# Localização da fonte estrutural — SEI, SIP, Julgar

Alvo desta skill: componentes distribuídos por pacote de release externo, não por script já
presente neste repositório. O caminho desse repositório de pacotes não é fixo — não presumir nome,
local ou estrutura de diretório. Confirmar com o desenvolvedor antes de prosseguir (contrato
obrigatório do `SKILL.md`).

## Reconhecer a pasta de uma versão dentro do repositório de pacotes

Convenção observada: uma pasta por release, nome no padrão `SEI_v<X.Y.Z>` (ex.: `SEI_v5.0.4`). Ao
listar o repositório informado:

- **Incluir** pasta cujo nome bate exatamente com esse padrão.
- **Excluir** pasta cujo nome tem sufixo além da versão (ex.: `_Seges_MGI`, `_<org>`) — indica
  pacote derivado/customizado de um órgão, não o release oficial. Ignorar salvo instrução explícita
  do desenvolvedor.
- Pasta cujo nome não segue `SEI_v<versão>` mas corresponde a um componente com script próprio
  neste repositório (ver `.agents/references/mapa-modulos-scripts.md`) pode ser um caso híbrido —
  **confirmar com o desenvolvedor qual fonte prevalece** antes de tratar como pacote (ver bloqueio
  específico do Julgar no `SKILL.md`).

## Localizar o script dentro da pasta da versão

O formato muda por época — checar o que existe antes de escolher o método:

- **Sem zip** (só PDF/DOC): não há DDL bruto disponível. Ler o PDF de "Atualização"/"Novidades" com
  a tool `Read` (lê PDF nativamente) e tratar o resultado como evidência de confiança mais baixa —
  sinalizar isso na resposta ao desenvolvedor, nunca escrever a ressalva no arquivo publicado.
- **Com zip** (release completo de fontes): extrair com o módulo `zipfile` do Python — não depende
  de utilitário externo instalado, funciona independente do sistema operacional ou do que estiver
  disponível no ambiente. Dentro do zip, localizar por **sufixo de caminho**, não por caminho
  absoluto — alguns zips têm uma pasta-raiz extra (ex. `SEI-Fontes-v4.0.0/sei/scripts/...`).

### Convenção de nome de arquivo e método por época (SEI)

- Releases mais recentes: `sei/scripts/atualizar_versao_sei.php`.
- Releases mais antigas: `sei/scripts/atualizar_versao.php` (nome anterior, mesmo papel).
- Em ambos: classe com um método por versão, `function versao_X_Y_Z($strVersaoAtual) { ... }`
  (pontos da versão viram `_`). Extrair por regex + contagem de chaves (há chaves aninhadas).
- Releases anteriores à convenção `versao_X_Y_Z` por método (observado antes de ~3.0.0/3.1.0): a
  lógica fica em `sei/web/rn/VersaoRN.php`, um único método monolítico
  (`atualizarVersaoConectado`) com `if` de versão embutido no meio do código — não há separação
  limpa por versão. Tratar como melhor esforço e sinalizar a limitação na resposta.

### SIP

`sip/scripts/atualizar_versao_sip.php` — às vezes literalmente nomeado `atualizar_versao_sei.php`
mesmo dentro da pasta `sip/` (particularidade do pacote, não confundir com o script do lado SEI).
Mesma convenção `versao_X_Y_Z()`, **mas o SIP tem numeração de versão própria, independente da
versão da pasta/pacote que o contém** — nunca procurar pelo número de versão do nome da pasta;
escanear o arquivo por **todos** os métodos `versao_X_Y_Z` presentes e tratar cada um pela própria
numeração.

## Regras de extração

- **Descartar versão trivial.** Método existe mas fica vazio (só chaves/comentário/espaço em branco
  após remover comentários) → sem mudança de schema, é patch só de código. Não criar entrada;
  omitir por completo.
- **Duplicação entre pacotes.** O método de uma versão já lançada costuma reaparecer, sem mudança,
  em pacotes de patches posteriores (ex.: o método de uma versão X aparece também dentro do pacote
  da versão X+1 código-only). Ao raspar mais de um pacote, preferir o corpo mais completo (maior,
  após remover comentários) entre as cópias encontradas — não assumir que o pacote com o nome da
  própria versão tem a cópia mais fiel.
- **Conferir antes de confiar.** Comparar uma amostra da entrada gerada contra o texto bruto do
  script, caractere a caractere, antes de publicar — inclusive qualificador de SGBD (ex. "no
  Oracle") quando presente no código-fonte.

## Banco ao vivo — validação, nunca fonte

O banco de um ambiente rodando (quando existir e o desenvolvedor disponibilizar acesso) só serve
para **validar** o dicionário já escrito — `comparar_schema.py schema` compara o `dicionario.md`
contra o `information_schema` ao vivo. O mecanismo de acesso (Docker, host remoto, outro) depende
do ambiente corrente — não presumir container, nome de serviço ou protocolo; perguntar ao
desenvolvedor como acessar se for usar esse modo. Nunca tratar o banco como fonte estrutural
primária para SEI/SIP/Julgar — a fonte é sempre o script/DDL do pacote.
