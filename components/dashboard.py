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
    st.markdown('<div class="subtitulo-secao">Síntese operacional dos casos processados.</div>', unsafe_allow_html=True)

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

        esquerda, direita = st.columns([1, 2], gap="large")

        with esquerda:
            st.markdown("#### Painel de Comando")

            if resumo_risco["Elevado"] > 0:
                st.error(
                    f"**ESTADO DO QUADRO: RISCO ELEVADO**\n\n"
                    f"Casos elevados: {resumo_risco['Elevado']}  \n"
                    f"Escalamentos: {total_escalados}"
                )
            elif resumo_risco["Médio"] > 0:
                st.warning(
                    f"**ESTADO DO QUADRO: RISCO MÉDIO**\n\n"
                    f"Casos médios: {resumo_risco['Médio']}  \n"
                    f"Total de casos: {total_casos}"
                )
            else:
                st.success(
                    f"**ESTADO DO QUADRO: RISCO BAIXO**\n\n"
                    f"Total de casos: {total_casos}  \n"
                    f"Escalamentos: {total_escalados}"
                )

            st.metric("Risco predominante", risco_predominante)
            st.metric("Casos escalados", total_escalados)
            st.metric("Taxa de escalamento", f"{percentagem_escalados}%")

            if not historico_df.empty:
                historico_ordenado = historico_df.sort_values(by="timestamp", ascending=False)
                ultimo = historico_ordenado.iloc[0]

                st.markdown("#### Último Caso")
                st.markdown(
                    f"""
**Caso:** {ultimo['id_caso']}  
**Risco:** {ultimo['risco']}  
**Ação:** {ultimo['acao']}  
**Pontuação:** {ultimo['pontuacao_total']}
"""
                )

            if total_validados > 0:
                st.markdown("#### Validação")
                st.metric("Taxa de confirmação", f"{taxa_confirmacao}%")
                st.metric("Taxa de alteração", f"{taxa_alteracao}%")

                if taxa_alteracao >= 40:
                    st.warning("Taxa de alteração elevada.")
                elif taxa_confirmacao >= 80:
                    st.success("Confirmação elevada da recomendação automática.")

        with direita:
            st.markdown("#### Resumo da Situação")

            d1, d2 = st.columns(2)
            with d1:
                st.metric("Total de casos", total_casos)
            with d2:
                st.metric("Casos validados", total_validados)

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
            historico_recente = historico_df[
                ["id_caso", "timestamp", "risco", "acao", "pontuacao_total"]
            ].head(10)

            with st.expander("Ver histórico resumido"):
                st.dataframe(
                    historico_recente,
                    use_container_width=True,
                    hide_index=True
                )

    st.markdown('</div>', unsafe_allow_html=True)
