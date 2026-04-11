from datetime import datetime
import streamlit as st

from constants import (
    opcoes_posicao,
    opcoes_velocidade,
    opcoes_radar,
    opcoes_contexto
)
from utils.cases import reiniciar_caso, gerar_caso_aleatorio, novo_id_caso
from utils.risk import classe_risco_input, construir_resultado
from utils.history import adicionar_historico


def render_input_panel():
    st.markdown('<div class="cartao">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">1. PROCESSAMENTO OPERACIONAL</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">O sistema calcula indicadores, avalia o risco e emite uma recomendação.</div>', unsafe_allow_html=True)

    st.info("Após clicar em “Gerar recomendação”, o sistema processa os indicadores, calcula a pontuação total, determina o nível de risco e emite a ação proposta.")

    mini1, mini2, mini3 = st.columns(3)

    with mini1:
        st.markdown("""
        <div class="mini-indicador" style="background: linear-gradient(180deg,#eff6ff,#eef4ff); border:1px solid #bfdbfe;">
            <div class="valor">6</div>
            <div class="rotulo">Indicadores internos</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Ver indicadores"):
            st.markdown("""
            **I1 — Identidade** *(calculado a partir de Posição/Trajetória)*  
            **I2 — Alteração de identidade** *(calculado a partir de Posição/Trajetória + Concordância com radar/outras fontes)*  
            **I3 — Cinemática** *(calculado a partir de Velocidade/Curso)*  
            **I4 — Consistência espaço-temporal** *(calculado a partir de Posição/Trajetória + Velocidade/Curso)*  
            **I5 — Contexto operacional** *(calculado a partir de Contexto operacional)*  
            **I6 — Consistência entre fontes** *(calculado a partir de Concordância com radar/outras fontes)*  
            """)

    with mini2:
        st.markdown("""
        <div class="mini-indicador">
            <div class="valor">3</div>
            <div class="rotulo">Níveis de risco</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Ver níveis de risco"):
            st.markdown("""
            **Baixo** — sem impacto  
            **Médio** — atenção  
            **Elevado** — prioridade  
            """)

    with mini3:
        st.markdown("""
        <div class="mini-indicador">
            <div class="valor">4</div>
            <div class="rotulo">Ações possíveis</div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Ver ações"):
            st.markdown("""
            **Ignorar** — sem ação  
            **Monitorizar** — vigilância  
            **Escalar** — intervenção  
            **Rever** — análise adicional  
            """)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cartao cartao-azul">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">2. DADOS DE ENTRADA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Nesta secção, o especialista descreve o caso em análise.</div>', unsafe_allow_html=True)

    with st.expander("Nota sobre integração futura dos dados"):
        st.write("""
Atualmente, os dados de entrada são introduzidos manualmente para efeitos de demonstração e validação conceptual do sistema.

Numa fase futura, estes dados poderão ser obtidos automaticamente a partir de **fontes externas**, incluindo sistemas operacionais e sensores relevantes, desde que sejam asseguradas as **devidas medidas de proteção**, nomeadamente ao nível da:
- confidencialidade;
- integridade;
- autenticação das fontes;
- controlo de acessos;
- rastreabilidade;
- e transmissão segura da informação.

Esta evolução permitirá reduzir intervenção manual, aumentar a rapidez de processamento e reforçar a ligação do sistema a ambientes operacionais reais.
""")

    col_titulo_entrada, col_botao_reset, col_botao_random = st.columns([3, 1, 1])

    with col_titulo_entrada:
        st.markdown("##### PREPARAÇÃO DO CASO")

    with col_botao_reset:
        st.button("Novo caso", use_container_width=True, on_click=reiniciar_caso)

    with col_botao_random:
        st.button("Caso aleatório", use_container_width=True, on_click=gerar_caso_aleatorio)

    st.markdown("##### Dados AIS/VMS")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="etiqueta">Posição/Trajetória</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(st.session_state.posicao)}">', unsafe_allow_html=True)
        posicao = st.selectbox(
            "Posição/Trajetória",
            opcoes_posicao,
            key="posicao",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="etiqueta">Velocidade/Curso</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(st.session_state.velocidade)}">', unsafe_allow_html=True)
        velocidade = st.selectbox(
            "Velocidade/Curso",
            opcoes_velocidade,
            key="velocidade",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("##### Outras fontes")
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown('<div class="etiqueta">Concordância com radar/outras fontes</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(st.session_state.radar)}">', unsafe_allow_html=True)
        radar = st.selectbox(
            "Concordância com radar/outras fontes",
            opcoes_radar,
            key="radar",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f:
        st.markdown('<div class="etiqueta">Contexto operacional</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(st.session_state.contexto)}">', unsafe_allow_html=True)
        contexto = st.selectbox(
            "Contexto operacional",
            opcoes_contexto,
            key="contexto",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    gerar = st.button("Gerar recomendação", use_container_width=True)

    if gerar:
        dados_resultado = construir_resultado(
            posicao=posicao,
            velocidade=velocidade,
            radar=radar,
            contexto=contexto,
            id_caso=novo_id_caso(),
            timestamp=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )

        st.session_state.dados_resultado = dados_resultado
        adicionar_historico(st.session_state.historico_casos, dados_resultado)
        st.session_state.resultado_gerado = True
        st.session_state.decisao_guardada = None

    st.markdown('</div>', unsafe_allow_html=True)
