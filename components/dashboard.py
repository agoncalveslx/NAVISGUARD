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
    st.markdown('<div class="titulo-secao">QUADRO DE SITUAÇÃO DE RISCO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Síntese operacional dos casos processados pelo sistema.</div>', unsafe_allow_html=True)

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
        percentagem_escalados = round((total_escalados / total_casos) * 100, 1) if total_casos > 0 else 0

        valores_risco = {
            "Baixo": resumo_risco["Baixo"],
            "Médio": resumo_risco["Médio"],
            "Elevado": resumo_risco["Elevado"]
        }
        risco_predominante = max(valores_risco, key=valores_risco.get)

        if resumo_risco["Elevado"] > 0:
            estado_quadro = "Risco Elevado"
            mensagem_quadro = f"Situação operacional com {resumo_risco['Elevado']} caso(s) de risco elevado e {total_escalados} escalamento(s) registado(s)."
            st.error(f"**Estado do quadro:** {estado_quadro} — {mensagem_quadro}")
        elif resumo_risco["Médio"] > 0:
            estado_quadro = "Risco Médio"
            mensagem_quadro = f"Situação operacional com predominância de risco médio. Total de casos: {total_casos}."
            st.warning(f"**Estado do quadro:** {estado_quadro} — {mensagem_quadro}")
        else:
            estado_quadro = "Risco Baixo"
            mensagem_quadro = f"Situação operacional estável. Total de casos processados: {total_casos}."
            st.success(f"**Estado do quadro:** {estado_quadro} — {mensagem_quadro}")

        st.markdown("#### Resumo da Situação")

        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.metric("Total de casos", total_casos)
        with d2:
            st.metric("Casos escalados", total_escalados)
        with d3:
            st.metric("Taxa de escalamento", f"{percentagem_escalados}%")
        with d4:
            st.metric("Risco predominante", risco_predominante)

        if total_validados > 0:
            a1, a2 = st.columns(2)
            with a1:
                st.metric("Taxa de confirmação", f"{taxa_confirmacao}%")
            with a2:
                st.metric("Taxa de alteração", f"{taxa_alteracao}%")

            if taxa_alteracao >= 40:
                st.warning("A taxa de alteração pelo especialista está elevada. Pode justificar revisão das regras automáticas.")
            elif taxa_confirmacao >= 80:
                st.success("A recomendação automática apresenta elevada taxa de confirmação pelo especialista.")

        st.markdown("#### Distribuição por Nível de Risco")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="mini-indicador" style="background:#e8f3ee;border:1px solid #3d8b5f;">
                <div class="valor">{resumo_risco['Baixo']}</div>
                <div class="rotulo">Risco Baixo</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="mini-indicador" style="background:#f4efe2;border:1px solid #b7791f;">
                <div class="valor">{resumo_risco['Médio']}</div>
                <div class="rotulo">Risco Médio</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="mini-indicador" style="background:#f3e8e8;border:1px solid #b91c1c;">
                <div class="valor">{resumo_risco['Elevado']}</div>
                <div class="rotulo">Risco Elevado</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Registo Operacional Recente")

        historico_df = historico_df.sort_values(by="timestamp", ascending=False)

        with st.expander("Ver histórico resumido"):
            st.dataframe(
                historico_df[["id_caso", "timestamp", "risco", "acao", "pontuacao_total"]],
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)
