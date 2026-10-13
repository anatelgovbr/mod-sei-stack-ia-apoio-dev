"""Sistema fictício de pedidos. Descritores de UI, regras e banco; sem servidor."""
VERSAO = "2.0.0"
PERMISSOES = {"Externo": {"registrar", "consultar", "acompanhar"}, "Interno": {"analisar"}, "Administrador": {"configurar"}}
MENUS = {"Externo": {"Pedidos > Registrar pedido": "registrar", "Pedidos > Consultar pedidos": "consultar", "Pedidos > Acompanhar pedido": "acompanhar"}, "Interno": {"Trabalho > Analisar pedidos": "analisar"}, "Administrador": {"Administração > Configurar serviço": "configurar"}}
TELAS = {
    "registrar": {"titulo": "Registrar pedido", "campos": {"assunto": {"label": "Assunto", "limite": 200, "obrigatorio": True, "ajuda": "Informe o assunto em até 200 caracteres."}, "prioridade": {"label": "Prioridade", "opcoes": ["Normal", "Alta"], "obrigatorio": True, "ajuda": "Selecione a prioridade do pedido."}}, "acao": "Salvar"},
    "consultar": {"titulo": "Consultar pedidos", "campos": {"numero": {"label": "Número"}}, "acao": "Pesquisar"},
    "acompanhar": {"titulo": "Acompanhar pedido", "campos": {"numero": {"label": "Número"}}, "resultado": "Situação", "acao": "Consultar andamento"},
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
        if len(assunto) > 200:
            return None, "O assunto deve ter até 200 caracteres."
        prioridade = dados.get("prioridade")
        if prioridade not in ["Normal", "Alta"]:
            return None, "Selecione uma prioridade válida."
        return {"assunto": assunto, "prioridade": prioridade, "situacao": "Aberto"}, "Pedido registrado."
    if tarefa in {"consultar", "acompanhar"}:
        return {"numero": dados.get("numero"), "situacao": "Aberto"}, ""
    return {}, "Operação concluída."

def apresentar(perfil, caminho):
    tarefa = MENUS.get(perfil, {}).get(caminho)
    return TELAS[tarefa] if tarefa in PERMISSOES.get(perfil, set()) else None

# O consumidor UI exibe a mensagem do manipulador no resultado da ação.
def acionar_tela(perfil, tarefa, dados):
    objeto, mensagem = operar(perfil, tarefa, dados)
    return {"objeto": objeto, "mensagem_visivel": mensagem}
