import streamlit as st


def inicializar_estado():
    defaults = {
        "resultado_gerado": False,
        "dados_resultado": None,
        "contador_casos": 0,
        "decisao_guardada": None,
        "historico_casos": [],
        "posicao": "Normal",
        "velocidade": "Normal",
        "radar": "Concordante",
        "contexto": "Normal",
    }

    for chave, valor in defaults.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor
