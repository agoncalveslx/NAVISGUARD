def contar_escalados(historico):
    return sum(1 for caso in historico if caso["acao"] == "Escalar")


def obter_resumo_risco(historico):
    contagem = {"Baixo": 0, "Médio": 0, "Elevado": 0}
    for caso in historico:
        risco = caso["risco"]
        if risco in contagem:
            contagem[risco] += 1
    return contagem


def contar_confirmacoes(historico):
    return sum(
        1 for caso in historico
        if caso.get("tipo_decisao") == "Confirmada"
    )


def contar_alteracoes(historico):
    return sum(
        1 for caso in historico
        if caso.get("tipo_decisao") == "Alterada pelo Especialista"
    )


def total_casos_validados(historico):
    return len(historico)


def adicionar_historico(historico, dados_resultado):
    historico.append({
        "id_caso": dados_resultado["id_caso"],
        "timestamp": dados_resultado["timestamp"],
        "risco": dados_resultado["risco"],
        "acao": dados_resultado["acao"],
        "pontuacao_total": dados_resultado["pontuacao_total"],
        "posicao": dados_resultado["posicao"],
        "velocidade": dados_resultado["velocidade"],
        "radar": dados_resultado["radar"],
        "contexto": dados_resultado["contexto"]
    })


def atualizar_decisao_no_historico(historico, id_caso, acao_proposta, decisao_final, justificacao, timestamp_decisao, tipo_decisao_fn):
    for caso in reversed(historico):
        if caso["id_caso"] == id_caso:
            caso["decisao_final"] = decisao_final
            caso["acao_proposta"] = acao_proposta
            caso["tipo_decisao"] = tipo_decisao_fn(acao_proposta, decisao_final)
            caso["justificacao"] = justificacao
            caso["timestamp_decisao"] = timestamp_decisao
            break
