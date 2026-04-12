import streamlit as st
from utils.cases import estado_do_caso


def render_header():
    col1, col2, col3 = st.columns([1.2, 2.6, 1.2])
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
        st.info("""
**Finalidade:** apoiar a decisão em ambiente marítimo com base na análise de comportamentos potencialmente anómalos.

**Fontes consideradas:** AIS, VMS, radar e outras fontes externas.
""")

        st.markdown("""
### Funções principais
1. **Gerar indicadores internos de risco (I1–I6)**  
   Avalia identidade, comportamento cinemático, coerência espacial e consistência entre fontes.

2. **Calcular uma pontuação agregada**  
   Combina os indicadores numa avaliação global de risco.

3. **Classificar o nível de risco**  
   - Baixo  
   - Médio  
   - Elevado

4. **Propor uma ação operacional**  
   - Ignorar  
   - Monitorizar  
   - Escalar

5. **Permitir validação humana**  
   O Especialista pode confirmar ou ajustar a recomendação proposta.
""")

        st.warning("""
**Nota:** esta aplicação é uma **demo conceptual**, desenvolvida para ilustrar a lógica de um sistema de apoio à decisão em contexto marítimo. Não substitui sistemas reais de vigilância ou comando operacional.
""")
