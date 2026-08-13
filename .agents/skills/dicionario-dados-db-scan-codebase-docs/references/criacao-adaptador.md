# Criação de adaptador

Carregue esta referência somente quando nenhum adaptador cobrir o alvo e o desenvolvedor autorizar explicitamente sua criação.

## Composição

Um adaptador pode ser autocontido ou combinar:

- **Base de família:** convenções realmente compartilhadas por dois ou mais alvos.
- **Overlay do alvo:** reconhecimento, caminhos e exceções próprios do alvo.

O overlay declara a família e o caminho da base. Para cada grupo obrigatório, pode herdar o valor sem repeti-lo, substituí-lo nomeando a exceção ou declará-lo inaplicável com justificativa. Omitir um grupo nos dois documentos não constitui herança.

## Contrato obrigatório

Considere o conjunto base mais overlay:

| Grupo | Conteúdo exigido |
|---|---|
| Reconhecimento e herança | Pistas que identificam ou excluem o alvo; família, base aplicada e exceções do overlay |
| Estrutura e versão | Fonte estrutural, definição de dados do código, gramática e ordenação de versões, extração dos blocos, alcance histórico e fonte da versão-alvo |
| Busca e semântica | Codificação, camadas, extensões, exclusões, identificadores, âncoras, linguagem, persistência e estratégias concretas de busca |
| Publicação e validação | Títulos, destinos, fórmula aplicável, checks automatizados e checks manuais necessários |
| Exceções e bloqueios | Particularidades comprovadas, lacunas da fonte e condições que exigem decisão humana |

A fonte estrutural atribui mudanças a versões; a definição de dados confere o estado implementado. Ausência de definição correspondente é lacuna de conferência, não conflito automático. Divergência material é conflito estrutural.

## Registro

Antes de criar o arquivo, inspecione a codebase e pergunte somente pelos grupos que continuarem indeterminados. Registre o adaptador em `../registro-adaptadores.md`, na raiz desta skill, conforme `contrato-de-adaptador.md`, apenas depois de completar o contrato. Não altere regras centrais somente para reconhecer o novo alvo.
