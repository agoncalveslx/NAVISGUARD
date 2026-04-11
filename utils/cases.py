import random
from datetime import datetime
import streamlit as st


def novo_id_caso():
    st.session_state.contador_casos += 1
    return f"CASO-{datetime.now().strftime('%Y%m%d')}-{st.session_state.contador_casos:03d}"


def gerar_id_decisao():
    return f"DEC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


def reiniciar_caso():
    st.session_state.resultado_gerado = False
    st.session_state.dados_resultado = None
    st.session_state.decisao_guardada = None
    st.session_state.posicao = "Normal"
    st.session_state.velocidade = "Normal"
    st.session_state.radar = "Concordante"
    st.session_state.contexto = "Normal"


def gerar_caso_aleatorio():
    st.session_state.resultado_gerado = False
    st.session_state.dados_resultado = None
    st.session_state.decisao_guardada = None
    st.session_state.posicao = random.choice(["Normal", "Ligeiramente suspeita", "Muito suspeita"])
    st.session_state.velocidade = random.choice(["Normal", "Ligeiramente suspeito", "Muito suspeito"])
    st.session_state.radar = random.choice(["Concordante", "Parcialmente discordante", "Discordante"])
    st.session_state.contexto = random.choice(["Normal", "Pouco habitual", "Muito suspeito"])


def estado_do_caso():
    if st.session_state.decisao_guardada is not None:
        return "Decisão registada"
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
        return "Recomendação gerada"
    return "Em análise"


def tipo_decisao(acao_proposta_atual, decisao_final):
    if acao_proposta_atual == decisao_final:
        return "Confirmada"
    return "Alterada pelo Especialista"


def resultado_em_reserva():
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
        estado_atual = {
            "posicao": st.session_state.posicao,
            "velocidade": st.session_state.velocidade,
            "radar": st.session_state.radar,
            "contexto": st.session_state.contexto
        }
        ultimo_estado = {
            "posicao": st.session_state.dados_resultado["posicao"],
            "velocidade": st.session_state.dados_resultado["velocidade"],
            "radar": st.session_state.dados_resultado["radar"],
            "contexto": st.session_state.dados_resultado["contexto"]
        }
        return estado_atual != ultimo_estado
    return False
