import streamlit as st

from constants import siglas_indicadores
from utils.cases import resultado_em_reserva
from utils.risk import classe_cartao_indicador, impacto_textual, formula_caso_texto


def render_indicators_section():
    em_reserva = resultado_em_reserva()

    if not (st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not em_reserva):
        return

    dados = st.session_state.dados_resultado
    contributos = dados["contributos"]

    st.markdown('<div class="cartao">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">8. QUADRO DE INDICADORES</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Visualização compacta do estado, peso e impacto na decisão de cada indicador.</div>', unsafe_allow_html=True)

    fatores_top = {
        k for k, v in contributos.items() if v["Contributo"] > 0
    }

    pares = [
        ("I1", contributos["I1"]),
        ("I2", contributos["I2"]),
        ("I3", contributos["I3"]),
        ("I4", contributos["I4"]),
        ("I5", contributos["I5"]),
        ("I6", contributos["I6"])
    ]

    for i in range(0, len(pares), 2):
        col_a, col_b = st.columns([1, 1], gap="small")

        codigo_a, info_a = pares[i]
        classe_a = classe_cartao_indicador(info_a["Contributo"])
        destaque_a = '<div class="fator-critico">FATOR CRÍTICO</div>' if codigo_a in fatores_top else ""

        with col_a:
            html_a = f"""<div class="mini-cartao-indicador {classe_a}">
{destaque_a}
<div class="mini-cartao-titulo">{codigo_a} — {siglas_indicadores[codigo_a]}</div>
<div class="mini-cartao-linha">Estado: <b>{info_a['Nível']}</b></div>
<div class="mini-cartao-linha">Pontos do estado: <b>{info_a['Pontos']}</b></div>
<div class="mini-cartao-linha">Peso: <b>{info_a['Peso']}</b></div>
<div class="mini-cartao-linha">Contributo: <b>{info_a['Contributo']}</b></div>
<div class="mini-cartao-linha">Impacto na decisão: <b>{impacto_textual(info_a['Contributo'])}</b></div>
</div>"""
            st.markdown(html_a, unsafe_allow_html=True)

        codigo_b, info_b = pares[i + 1]
        classe_b = classe_cartao_indicador(info_b["Contributo"])
        destaque_b = '<div class="fator-critico">FATOR CRÍTICO</div>' if codigo_b in fatores_top else ""

        with col_b:
            html_b = f"""<div class="mini-cartao-indicador {classe_b}">
{destaque_b}
<div class="mini-cartao-titulo">{codigo_b} — {siglas_indicadores[codigo_b]}</div>
<div class="mini-cartao-linha">Estado: <b>{info_b['Nível']}</b></div>
<div class="mini-cartao-linha">Pontos do estado: <b>{info_b['Pontos']}</b></div>
<div class="mini-cartao-linha">Peso: <b>{info_b['Peso']}</b></div>
<div class="mini-cartao-linha">Contributo: <b>{info_b['Contributo']}</b></div>
<div class="mini-cartao-linha">Impacto na decisão: <b>{impacto_textual(info_b['Contributo'])}</b></div>
</div>"""
            st.markdown(html_b, unsafe_allow_html=True)

    with st.expander("Ver regra de cálculo"):
        st.markdown(f"""
        **Origem dos indicadores**
        - **I1** = calculado a partir de **Posição/Trajetória**
        - **I2** = calculado a partir de **Posição/Trajetória + Concordância com radar/outras fontes**
        - **I3** = calculado a partir de **Velocidade/Curso**
        - **I4** = calculado a partir de **Posição/Trajetória + Velocidade/Curso**
        - **I5** = calculado a partir de **Contexto operacional**
        - **I6** = calculado a partir de **Concordância com radar/outras fontes**

        **Estados dos indicadores**
        - **Baixo** = 0 pontos
        - **Médio** = 1 ponto
        - **Elevado** = 2 pontos

        **Pesos dos indicadores**
        - **I1** = 3
        - **I2** = 2
        - **I3** = 2
        - **I4** = 2
        - **I5** = 1
        - **I6** = 3

        **Fórmula de cálculo**
        - **Pontuação final = Σ (pontosᵢ × pesoᵢ), i ∈ {{I1, I2, I3, I4, I5, I6}}**
        - **Pontuação final = (pontos_I1 × 3) + (pontos_I2 × 2) + (pontos_I3 × 2) + (pontos_I4 × 2) + (pontos_I5 × 1) + (pontos_I6 × 3)**

        **Fórmula aplicada a este caso**
        <div class="formula-caso"><b>{formula_caso_texto(contributos)}</b></div>

        **Conversão da pontuação em risco e ação**
        - **Pontuação final ≤ 4** → **Risco Baixo** → **Ignorar**
        - **Pontuação final ≤ 8** → **Risco Médio** → **Monitorizar**
        - **Pontuação final > 8** → **Risco Elevado** → **Escalar**
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
