import streamlit as st
from utils.cases import estado_do_caso


def render_header():
    col1, col2, col3 = st.columns([1, 2.4, 1])
    with col2:
        st.image("logo.jpg", use_container_width=True)

    id_atual = (
        st.session_state.dados_resultado["id_caso"]
        if st.session_state.dados_resultado
        else "Não iniciado"
    )

    st.markdown(
        f"""
        <div class="barra-estado-caso">
            <b>Caso atual:</b> {id_atual} &nbsp;&nbsp;|&nbsp;&nbsp;
            <b>Estado:</b> {estado_do_caso()}
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("Enquadramento Operacional"):
        st.write("""
Este sistema constitui uma **plataforma de apoio à decisão em ambiente marítimo**, desenvolvida para avaliar comportamentos potencialmente anómalos de embarcações com base em dados operacionais.

A aplicação simula a análise de informação proveniente de sistemas como:
- AIS (Automatic Identification System)
- VMS (Vessel Monitoring System)
- Radar e outras fontes externas

Com base nos dados introduzidos pelo Especialista, o sistema:

1. **Gera indicadores internos de risco (I1–I6)**
   Avalia dimensões como identidade, comportamento cinemático, coerência espacial e consistência entre fontes.

2. **Calcula uma pontuação agregada**
   Cada indicador contribui de forma ponderada para o risco global.

3. **Classifica o nível de risco**
   - Baixo
   - Médio
   - Elevado

4. **Propõe uma ação operacional**
   - Ignorar
   - Monitorizar
   - Escalar

5. **Permite validação humana da decisão**
   O Especialista pode confirmar ou ajustar a recomendação, garantindo controlo humano no processo.

⚠️ **Nota:**
Esta aplicação é uma **demo conceptual**, desenvolvida para ilustrar a lógica de um sistema de apoio à decisão em contexto marítimo, não substituindo sistemas reais de vigilância ou comando operacional.
""")
