import streamlit as st

from utils.cases import resultado_em_reserva
from utils.risk import (
    obter_fatores_principais,
    classe_selo_risco,
    classe_acao_resultado
)
from components.map_view import desenhar_mapa_tatico


def render_tactical_sections():
    em_reserva = resultado_em_reserva()

    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not em_reserva:
        dados = st.session_state.dados_resultado
        contributos = dados["contributos"]
        pontuacao_total = dados["pontuacao_total"]
        risco = dados["risco"]
        acao = dados["acao"]

        fatores_principais = obter_fatores_principais(contributos, top_n=3)

        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">3. AVALIAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Síntese dos fatores críticos e impacto na recomendação.</div>', unsafe_allow_html=True)

        st.info("BRIEFING OPERACIONAL")
        st.markdown("**Estado:** Avaliação concluída")

        st.markdown("**Fatores críticos:**")
        for idx, fator in enumerate(fatores_principais):
            prefixo = "• "
            if idx == 0:
                prefixo = "• Principal fator: "
            st.write(f"{prefixo}{fator['nome']}")

        st.markdown("##### AVALIAÇÃO DE RISCO")
        st.write(f"**Nível de risco:** {risco}")
        st.write(f"**Ação proposta:** {acao}")
        st.markdown(
            f"**Avaliação:** Situação classificada com risco **{risco.lower()}** devido à combinação dos fatores críticos identificados."
        )
        st.markdown("**Fundamento principal:** inconsistência entre fatores com maior contributo e necessidade de resposta proporcional ao risco.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="resultado-critico">', unsafe_allow_html=True)

        col_res_1, col_res_2 = st.columns([3, 1])

        with col_res_1:
            st.markdown('<div class="resultado-titulo">4. PROPOSTA DE AÇÃO</div>', unsafe_allow_html=True)
            st.markdown('<div class="resultado-subtitulo">Recomendação do sistema gerada a partir das entradas submetidas.</div>', unsafe_allow_html=True)

        with col_res_2:
            st.markdown(
                f'<div class="selo-risco {classe_selo_risco(risco)}" style="text-align:center;">RISCO {risco.upper()}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="resultado-meta"><b>ID do caso:</b> {dados["id_caso"]}<br><b>Processado em:</b> {dados["timestamp"]}</div>',
            unsafe_allow_html=True
        )

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Pontuação total", pontuacao_total)
        with m2:
            st.metric("Nível de risco", risco)
        with m3:
            st.metric("Ação proposta", acao)

        st.markdown(
            f'<div class="acao-critica {classe_acao_resultado(risco)}">AÇÃO RECOMENDADA: {acao.upper()}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">5. MAPA TÁTICO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Representação do contacto, trajetória estimada e perímetro de atenção no espaço marítimo adjacente à costa continental portuguesa.</div>', unsafe_allow_html=True)
        desenhar_mapa_tatico(
            dados["posicao"],
            dados["velocidade"],
            dados["contexto"],
            dados["risco"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.resultado_gerado and em_reserva:
        st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">3. AVALIAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Informação em reserva.</div>', unsafe_allow_html=True)
        st.warning("As entradas foram alteradas. Gere nova recomendação para atualizar a avaliação tática.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">4. PROPOSTA DE AÇÃO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Resultado anterior invalidado.</div>', unsafe_allow_html=True)
        st.warning("Configuração alterada. O resultado anterior ficou em reserva e deve ser regenerado antes de nova validação.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">5. MAPA TÁTICO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Visualização em espera.</div>', unsafe_allow_html=True)
        st.warning("O mapa tático será atualizado após a geração de nova recomendação.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">3. AVALIAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Aguardando processamento.</div>', unsafe_allow_html=True)
        st.info("A avaliação tática será apresentada após a geração da recomendação.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">4. PROPOSTA DE AÇÃO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Aguardando processamento operacional.</div>', unsafe_allow_html=True)
        st.info("Introduza os dados do caso e clique em “Gerar recomendação”.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">5. MAPA TÁTICO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Aguardando geração do caso.</div>', unsafe_allow_html=True)
        st.info("O mapa tático será apresentado após a geração da recomendação.")
        st.markdown('</div>', unsafe_allow_html=True)
