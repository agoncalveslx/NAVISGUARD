import streamlit as st
import pandas as pd

from utils.history import (
    obter_resumo_risco,
    contar_escalados,
    contar_confirmacoes,
    contar_alteracoes,
    total_casos_validados
)


def render_dashboard():
    st.markdown('<div class="cartao">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">DASHBOARD DE RISCO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Síntese estatística dos casos processados pelo sistema.</div>', unsafe_allow_html=True)

    if len(st.session_state.historico_casos) == 0:
        st.info("Ainda não existem casos registados para análise estatística.")
    else:
        historico_df = pd.DataFrame(st.session_state.historico_casos)
        resumo_risco = obter_resumo_risco(st.session_state.historico_casos)
        total_casos = len(st.session_state.historico_casos)
        total_escalados = contar_escalados(st.session_state.historico_casos)
        total_confirmacoes = contar_confirmacoes(st.session_state.historico_casos)
        total_alteracoes = contar_alteracoes(st.session_state.historico_casos)
        total_validados = total_casos_validados(st.session_state.historico_casos)

        taxa_confirmacao = round((total_confirmacoes / total_validados) * 100, 1) if total_validados > 0 else 0
        taxa_alteracao = round((total_alteracoes / total_validados) * 100, 1) if total_validados > 0 else 0

        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.metric("Total de casos", total_casos)
        with d2:
            st.metric("Risco baixo", resumo_risco["Baixo"])
        with d3:
            st.metric("Risco médio", resumo_risco["Médio"])
        with d4:
            st.metric("Risco elevado", resumo_risco["Elevado"])

        e1, e2 = st.columns(2)
        with e1:
            st.metric("Casos escalados", total_escalados)
        with e2:
            percentagem_escalados = round((total_escalados / total_casos) * 100, 1) if total_casos > 0 else 0
            st.metric("% escalados", f"{percentagem_escalados}%")

        if total_validados > 0:
            if taxa_alteracao >= 40:
                st.warning("A taxa de alteração pelo especialista está elevada. Pode justificar revisão das regras automáticas.")
            elif taxa_confirmacao >= 80:
                st.success("A recomendação automática apresenta elevada taxa de confirmação pelo especialista.")

        st.markdown("#### Distribuição por nível de risco")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="mini-indicador" style="background:#ecfdf5;border:1px solid #22c55e;">
                <div class="valor">{resumo_risco['Baixo']}</div>
                <div class="rotulo">Risco Baixo</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="mini-indicador" style="background:#fffbeb;border:1px solid #f59e0b;">
                <div class="valor">{resumo_risco['Médio']}</div>
                <div class="rotulo">Risco Médio</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="mini-indicador" style="background:#fef2f2;border:1px solid #ef4444;">
                <div class="valor">{resumo_risco['Elevado']}</div>
                <div class="rotulo">Risco Elevado</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Ver histórico resumido"):
            st.dataframe(
                historico_df[["id_caso", "timestamp", "risco", "acao", "pontuacao_total"]],
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
