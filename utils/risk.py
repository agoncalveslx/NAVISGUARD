from constants import pesos, nomes_indicadores


def nivel_para_pontos(nivel):
    return {"Baixo": 0, "Médio": 1, "Elevado": 2}[nivel]


def nivel_risco(pontuacao):
    if pontuacao <= 4:
        return "Baixo"
    elif pontuacao <= 8:
        return "Médio"
    return "Elevado"


def acao_proposta(pontuacao):
    if pontuacao <= 4:
        return "Ignorar"
    elif pontuacao <= 8:
        return "Monitorizar"
    return "Escalar"


def cor_risco(risco):
    if risco == "Baixo":
        return "#d1fae5", "#065f46", "cartao-verde"
    elif risco == "Médio":
        return "#fef3c7", "#92400e", "cartao-amarelo"
    return "#fee2e2", "#991b1b", "cartao-vermelho"


def classe_cartao_indicador(contributo):
    if contributo >= 5:
        return "mini-cartao-elevado"
    elif contributo >= 2:
        return "mini-cartao-medio"
    return "mini-cartao-baixo"


def classe_risco_input(valor):
    if valor in ["Normal", "Concordante"]:
        return "risco-baixo"
    elif valor in [
        "Ligeiramente suspeita",
        "Ligeiramente suspeito",
        "Parcialmente discordante",
        "Pouco habitual"
    ]:
        return "risco-medio"
    elif valor in ["Muito suspeita", "Muito suspeito", "Discordante"]:
        return "risco-elevado"
    return "risco-neutro"


def classe_selo_risco(risco):
    if risco == "Baixo":
        return "selo-baixo"
    elif risco == "Médio":
        return "selo-medio"
    return "selo-elevado"


def classe_acao_resultado(risco):
    if risco == "Baixo":
        return "acao-baixa"
    elif risco == "Médio":
        return "acao-media"
    return "acao-elevada"


def calcular_indicadores(posicao, velocidade, radar, contexto):
    if posicao == "Muito suspeita":
        i1 = "Elevado"
    elif posicao == "Ligeiramente suspeita":
        i1 = "Médio"
    else:
        i1 = "Baixo"

    if posicao == "Muito suspeita" and radar == "Discordante":
        i2 = "Elevado"
    elif posicao == "Ligeiramente suspeita" or radar == "Parcialmente discordante":
        i2 = "Médio"
    else:
        i2 = "Baixo"

    if velocidade == "Muito suspeito":
        i3 = "Elevado"
    elif velocidade == "Ligeiramente suspeito":
        i3 = "Médio"
    else:
        i3 = "Baixo"

    if posicao == "Muito suspeita" and velocidade == "Muito suspeito":
        i4 = "Elevado"
    elif posicao == "Ligeiramente suspeita" or velocidade == "Ligeiramente suspeito":
        i4 = "Médio"
    else:
        i4 = "Baixo"

    if contexto == "Muito suspeito":
        i5 = "Elevado"
    elif contexto == "Pouco habitual":
        i5 = "Médio"
    else:
        i5 = "Baixo"

    if radar == "Discordante":
        i6 = "Elevado"
    elif radar == "Parcialmente discordante":
        i6 = "Médio"
    else:
        i6 = "Baixo"

    return {"I1": i1, "I2": i2, "I3": i3, "I4": i4, "I5": i5, "I6": i6}


def impacto_textual(contributo):
    if contributo >= 5:
        return "Elevado"
    elif contributo >= 2:
        return "Moderado"
    elif contributo >= 1:
        return "Reduzido"
    return "Muito reduzido"


def obter_fatores_principais(contributos, top_n=3):
    ordenados = sorted(contributos.items(), key=lambda x: x[1]["Contributo"], reverse=True)
    return [
        {
            "codigo": item[0],
            "nome": item[1]["Nome"],
            "nivel": item[1]["Nível"],
            "contributo": item[1]["Contributo"]
        }
        for item in ordenados[:top_n]
    ]


def formula_caso_texto(contributos):
    termos = []
    total = 0
    for chave in ["I1", "I2", "I3", "I4", "I5", "I6"]:
        pontos = contributos[chave]["Pontos"]
        peso = contributos[chave]["Peso"]
        contributo = contributos[chave]["Contributo"]
        termos.append(f"({chave}: {pontos}×{peso}={contributo})")
        total += contributo
    return " + ".join(termos) + f" = {total}"


def construir_resultado(posicao, velocidade, radar, contexto, id_caso, timestamp):
    indicadores = calcular_indicadores(posicao, velocidade, radar, contexto)

    contributos = {}
    pontuacao_total = 0

    for chave, valor in indicadores.items():
        pontos = nivel_para_pontos(valor)
        contributo = pontos * pesos[chave]
        contributos[chave] = {
            "Código": chave,
            "Nome": nomes_indicadores[chave],
            "Nível": valor,
            "Pontos": pontos,
            "Peso": pesos[chave],
            "Contributo": contributo
        }
        pontuacao_total += contributo

    risco = nivel_risco(pontuacao_total)
    acao = acao_proposta(pontuacao_total)

    return {
        "id_caso": id_caso,
        "timestamp": timestamp,
        "posicao": posicao,
        "velocidade": velocidade,
        "radar": radar,
        "contexto": contexto,
        "indicadores": indicadores,
        "contributos": contributos,
        "pontuacao_total": pontuacao_total,
        "risco": risco,
        "acao": acao
    }
