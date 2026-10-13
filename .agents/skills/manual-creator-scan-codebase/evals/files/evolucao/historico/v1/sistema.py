"""Sistema fictício de pedidos. Descritores de UI, regras e banco; sem servidor."""
VERSAO = "1.0.0"
PERMISSOES = {"Externo": {"registrar", "consultar"}, "Interno": {"analisar"}, "Administrador": {"configurar"}}
MENUS = {"Externo": {"Pedidos > Registrar pedido": "registrar", "Pedidos > Consultar pedidos": "consultar"}, "Interno": {"Trabalho > Analisar pedidos": "analisar"}, "Administrador": {"Administração > Configurar serviço": "configurar"}}
TELAS = {
    "registrar": {"titulo": "Registrar pedido", "campos": {"assunto": {"label": "Assunto", "limite": 120, "obrigatorio": True, "ajuda": "Descreva o pedido em até 120 caracteres."}, "referencia": {"label": "Referência antiga", "obrigatorio": False, "ajuda": "Informe a referência, se houver."}}, "acao": "Salvar"},
    "consultar": {"titulo": "Consultar pedidos", "campos": {"numero": {"label": "Número"}}, "acao": "Pesquisar"},
    "analisar": {"titulo": "Analisar pedidos", "campos": {"decisao": {"label": "Decisão"}}, "acao": "Concluir análise"},
    "configurar": {"titulo": "Configurar serviço", "campos": {"ativo": {"label": "Serviço ativo"}}, "acao": "Aplicar"},
}

def operar(perfil, tarefa, dados):
    if tarefa not in PERMISSOES.get(perfil, set()):
        return None, "Acesso não permitido."
    if tarefa == "registrar":
        assunto = dados.get("assunto", "")
        if not isinstance(assunto, str) or not assunto.strip():
            return None, "Informe o assunto."
        if len(assunto) > 120:
            return None, "O assunto deve ter até 120 caracteres."
        return {"assunto": assunto, "referencia": dados.get("referencia", ""), "situacao": "Aberto"}, "Pedido registrado."
    if tarefa in {"consultar"}:
        return {"numero": dados.get("numero"), "situacao": "Aberto"}, ""
    return {}, "Operação concluída."

def apresentar(perfil, caminho):
    tarefa = MENUS.get(perfil, {}).get(caminho)
    return TELAS[tarefa] if tarefa in PERMISSOES.get(perfil, set()) else None

# O consumidor UI exibe a mensagem do manipulador no resultado da ação.
def acionar_tela(perfil, tarefa, dados):
    objeto, mensagem = operar(perfil, tarefa, dados)
    return {"objeto": objeto, "mensagem_visivel": mensagem}
