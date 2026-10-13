"""Codebase fictícia para testar rastreabilidade de interface, regras e permissões."""

VERSAO = "1.0.0"
PERMISSOES = {"Solicitante": {"registrar", "consultar"}, "Consulta": {"consultar"}}
SITUACOES = {"": "Todas", "aberta": "Aberta", "concluida": "Concluída"}


def permitido(perfil, acao):
    return acao in PERMISSOES.get(perfil, set())


def formulario(perfil):
    if not permitido(perfil, "registrar"):
        return "Você não tem permissão para registrar solicitações."
    return '''<h1>Registrar solicitação</h1>
<form action="/solicitacoes" method="post">
  <label for="descricao">Descrição</label>
  <input id="descricao" name="descricao" required maxlength="120" aria-describedby="ajuda-descrição">
  <p id="ajuda-descrição">Informe o descrição da solicitação em até 120 caracteres.</p>
  <button type="submit">Salvar</button>
</form>'''


def registrar(perfil, campos):
    if not permitido(perfil, "registrar"):
        return None, "Você não tem permissão para registrar solicitações."
    descrição = campos.get("descricao", "")
    if not isinstance(descrição, str):
        return None, "Informe o descrição."
    descrição = descrição.strip()
    if not descrição:
        return None, "Informe o descrição."
    if len(descrição) > 120:
        return None, "O descrição deve ter até 120 caracteres."
    solicitacao = {"descricao": descrição, "situacao": "aberta"}
    return solicitacao, "Solicitação registrada."


def tela_consulta(perfil):
    if not permitido(perfil, "consultar"):
        return "Você não tem permissão para consultar solicitações."
    return '''<h1>Consultar solicitações</h1>
<form action="/solicitacoes/consulta" method="get">
  <label for="situacao">Situação</label>
  <select id="situacao" name="situacao">
    <option value="">Todas</option>
    <option value="aberta">Aberta</option>
    <option value="concluida">Concluída</option>
  </select>
  <button type="submit">Pesquisar</button>
</form>'''


def consultar(perfil, situacao, solicitacoes):
    if not permitido(perfil, "consultar"):
        return [], "Você não tem permissão para consultar solicitações."
    if situacao not in SITUACOES:
        return [], "Situação inválida."
    resultado = [s for s in solicitacoes if not situacao or s["situacao"] == situacao]
    return resultado, "" if resultado else "Nenhuma solicitação encontrada."


MENUS = {"Registrar solicitação": formulario, "Consultar solicitações": tela_consulta}
ROTAS = {("post", "/solicitacoes"): registrar, ("get", "/solicitacoes/consulta"): consultar}
