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
    st.markdown(
        '<div class="subtitulo-secao">Leitura compacta do estado, contributo e impacto decisional de cada indicador.</div>',
        unsafe_allow_html=True
    )

    pares = [
        ("I1", contributos["I1"]),
        ("I2", contributos["I2"]),
        ("I3", contributos["I3"]),
        ("I4", contributos["I4"]),
        ("I5", contributos["I5"]),
        ("I6", contributos["I6"])
    ]

    ordenados = sorted(
        pares,
        key=lambda x: (x[1]["Contributo"], x[1]["Pontos"], x[1]["Peso"]),
        reverse=True
    )

    dominantes = [codigo for codigo, info in ordenados if info["Contributo"] > 0][:3]

    if dominantes:
        nomes_dominantes = " | ".join(
            [f"{codigo} — {siglas_indicadores[codigo]}" for codigo in dominantes]
        )
        st.markdown(
            f'<div class="bloco-meta"><b>Indicadores dominantes:</b> {nomes_dominantes}</div>',
            unsafe_allow_html=True
        )

    for i in range(0, len(pares), 2):
        col_a, col_b = st.columns([1, 1], gap="small")

        codigo_a, info_a = pares[i]
        classe_a = classe_cartao_indicador(info_a["Contributo"])
        destaque_a = '<div class="fator-critico">DOMINANTE</div>' if codigo_a in dominantes[:2] else ""

        with col_a:
            html_a = (
                f'<div class="mini-cartao-indicador {classe_a}">'
                f'{destaque_a}'
                f'<div class="mini-cartao-titulo">{codigo_a} — {siglas_indicadores[codigo_a]}</div>'
                f'<div class="mini-cartao-linha"><b>Estado:</b> {info_a["Nível"]}</div>'
                f'<div class="mini-cartao-linha"><b>Contributo:</b> {info_a["Contributo"]}</div>'
                f'<div class="mini-cartao-linha"><b>Impacto:</b> {impacto_textual(info_a["Contributo"])}</div>'
                f'<div class="mini-cartao-linha" style="margin-top:4px; color:#64748b;">'
                f'Pontos: <b>{info_a["Pontos"]}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Peso: <b>{info_a["Peso"]}</b>'
                f'</div>'
                f'</div>'
            )
            st.markdown(html_a, unsafe_allow_html=True)

        codigo_b, info_b = pares[i + 1]
        classe_b = classe_cartao_indicador(info_b["Contributo"])
        destaque_b = '<div class="fator-critico">DOMINANTE</div>' if codigo_b in dominantes[:2] else ""

        with col_b:
            html_b = (
                f'<div class="mini-cartao-indicador {classe_b}">'
                f'{destaque_b}'
                f'<div class="mini-cartao-titulo">{codigo_b} — {siglas_indicadores[codigo_b]}</div>'
                f'<div class="mini-cartao-linha"><b>Estado:</b> {info_b["Nível"]}</div>'
                f'<div class="mini-cartao-linha"><b>Contributo:</b> {info_b["Contributo"]}</div>'
                f'<div class="mini-cartao-linha"><b>Impacto:</b> {impacto_textual(info_b["Contributo"])}</div>'
                f'<div class="mini-cartao-linha" style="margin-top:4px; color:#64748b;">'
                f'Pontos: <b>{info_b["Pontos"]}</b> &nbsp;&nbsp;|&nbsp;&nbsp; Peso: <b>{info_b["Peso"]}</b>'
                f'</div>'
                f'</div>'
            )
            st.markdown(html_b, unsafe_allow_html=True)

        with st.expander("Ver regra de cálculo"):
            st.markdown(
        f"""
**Origem dos indicadores**
- **I1** = Posição/Trajetória
- **I2** = Posição/Trajetória + Radar/Outras fontes
- **I3** = Velocidade/Curso
- **I4** = Posição/Trajetória + Velocidade/Curso
- **I5** = Contexto operacional
- **I6** = Radar/Outras fontes

**Escala de estados**
- **Baixo** = 0
- **Médio** = 1
- **Elevado** = 2

**Fórmula aplicada a este caso**
<div class="formula-caso"><b>{formula_caso_texto(contributos)}</b></div>

**Resultado operacional**
- **Pontuação final ≤ 4** → **Risco Baixo** → **Ignorar**
- **Pontuação final ≤ 8** → **Risco Médio** → **Monitorizar**
- **Pontuação final > 8** → **Risco Elevado** → **Escalar**
""",
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)
