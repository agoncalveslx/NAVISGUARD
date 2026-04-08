import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(
    page_title="NAVISGUARD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# Estado da sessão
# -------------------------
if "resultado_gerado" not in st.session_state:
    st.session_state.resultado_gerado = False

if "dados_resultado" not in st.session_state:
    st.session_state.dados_resultado = None

if "contador_casos" not in st.session_state:
    st.session_state.contador_casos = 0

if "decisao_guardada" not in st.session_state:
    st.session_state.decisao_guardada = None

# -------------------------
# Estilo visual
# -------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
    }

    .topo-dashboard {
        background: linear-gradient(90deg, #0f172a 0%, #1d4ed8 100%);
        padding: 24px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    }

    .topo-dashboard h1 {
        margin: 0;
        font-size: 2rem;
    }

    .topo-dashboard p {
        margin-top: 8px;
        font-size: 1rem;
        color: #eef4ff;
    }

    .cartao {
        background: white;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    .cartao-azul {
        background: linear-gradient(180deg, #eff6ff 0%, #eef4ff 100%);
        border: 1px solid #bfdbfe;
    }

    .cartao-verde {
        background: linear-gradient(180deg, #ecfdf5 0%, #d1fae5 100%);
        border: 1px solid #a7f3d0;
    }

    .cartao-amarelo {
        background: linear-gradient(180deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
    }

    .cartao-vermelho {
        background: linear-gradient(180deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
    }

    .titulo-secao {
        font-size: 1.3rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }

    .subtitulo-secao {
        font-size: 0.95rem;
        color: #475569;
        margin-bottom: 16px;
    }

    .etiqueta {
        font-weight: 600;
        color: #0f172a;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    .acao-final {
        padding: 16px;
        border-radius: 14px;
        font-weight: 700;
        text-align: center;
        margin-top: 12px;
        border: 1px solid #d1d5db;
        font-size: 1.05rem;
    }

    .mini-indicador {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .mini-indicador .valor {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0f172a;
    }

    .mini-indicador .rotulo {
        font-size: 0.9rem;
        color: #64748b;
    }

    .mini-cartao-indicador {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 10px;
        position: relative;
    }

    .mini-cartao-baixo {
        background: linear-gradient(180deg, #ecfdf5 0%, #d1fae5 100%);
        border: 1px solid #a7f3d0;
    }

    .mini-cartao-medio {
        background: linear-gradient(180deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fde68a;
    }

    .mini-cartao-elevado {
        background: linear-gradient(180deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
    }

    .mini-cartao-titulo {
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 6px;
        font-size: 0.96rem;
    }

    .mini-cartao-linha {
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.4;
    }

    .bloco-meta {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 12px;
        color: #334155;
        font-size: 0.92rem;
    }

    .barra-estado-caso {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 18px;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.18);
    }

    .resultado-critico {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        color: white;
        border-radius: 18px;
        padding: 20px;
        border: 1px solid #1f2937;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.22);
        margin-bottom: 20px;
    }

    .resultado-titulo {
        font-size: 1.25rem;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 4px;
    }

    .resultado-subtitulo {
        font-size: 0.93rem;
        color: #1f2937;
    }

    .selo-risco {
        padding: 8px 12px;
        border-radius: 999px;
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: 0.03em;
        white-space: nowrap;
        border: 1px solid rgba(255,255,255,0.15);
    }

    .selo-baixo {
        background: #14532d;
        color: #dcfce7;
    }

    .selo-medio {
        background: #78350f;
        color: #fef3c7;
    }

    .selo-elevado {
        background: #7f1d1d;
        color: #fee2e2;
    }

    .resultado-meta {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 10px 12px;
        color: #1f2937;
        font-size: 0.9rem;
        margin-bottom: 14px;
    }

    .acao-critica {
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        font-weight: 800;
        font-size: 1.1rem;
        border: 1px solid rgba(255,255,255,0.10);
        margin-top: 10px;
    }

    .acao-baixa {
        background: linear-gradient(90deg, #14532d 0%, #166534 100%);
        color: #dcfce7;
    }

    .acao-media {
        background: linear-gradient(90deg, #78350f 0%, #92400e 100%);
        color: #fef3c7;
    }

    .acao-elevada {
        background: linear-gradient(90deg, #7f1d1d 0%, #991b1b 100%);
        color: #fee2e2;
    }

    .fator-critico {
        display: inline-block;
        background: #0f172a;
        color: white;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 999px;
        margin-bottom: 6px;
    }

    .estado-confirmacao {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        border: 1px solid #86efac;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 6px;
    }

    .estado-alteracao {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fcd34d;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 6px;
    }

    .formula-caso {
        background: #f8fafc;
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        padding: 12px;
        color: #334155;
        font-size: 0.92rem;
        margin-top: 10px;
    }

    /* Botões */
    div.stButton > button {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
        color: white;
        border: none;
    }

    div.stButton > button:focus {
        color: white !important;
        border: none !important;
        box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.25);
    }

    /* Selectbox */
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        min-height: 44px;
        font-weight: 600;
    }

    .risco-baixo div[data-baseweb="select"] > div {
        background: #ecfdf5 !important;
        border: 1px solid #a7f3d0 !important;
        color: #065f46 !important;
    }

    .risco-medio div[data-baseweb="select"] > div {
        background: #fffbeb !important;
        border: 1px solid #fde68a !important;
        color: #92400e !important;
    }

    .risco-elevado div[data-baseweb="select"] > div {
        background: #fef2f2 !important;
        border: 1px solid #fecaca !important;
        color: #991b1b !important;
    }

    .risco-neutro div[data-baseweb="select"] > div {
        background: #f8fafc !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Funções auxiliares
# -------------------------
def nivel_para_pontos(nivel):
    return {"Baixo": 0, "Médio": 1, "Elevado": 2}[nivel]

def nivel_risco(pontuacao):
    if pontuacao <= 4:
        return "Baixo"
    elif pontuacao <= 8:
        return "Médio"
    return "Elevado"

def acao_proposta(pontuacao):
    if pontuacao <= 4:
        return "Ignorar"
    elif pontuacao <= 8:
        return "Monitorizar"
    return "Escalar"

def cor_risco(risco):
    if risco == "Baixo":
        return "#d1fae5", "#065f46", "cartao-verde"
    elif risco == "Médio":
        return "#fef3c7", "#92400e", "cartao-amarelo"
    return "#fee2e2", "#991b1b", "cartao-vermelho"

def classe_cartao_indicador(contributo):
    if contributo >= 5:
        return "mini-cartao-elevado"
    elif contributo >= 2:
        return "mini-cartao-medio"
    return "mini-cartao-baixo"

def classe_risco_input(valor):
    if valor in ["Normal", "Concordante"]:
        return "risco-baixo"
    elif valor in ["Ligeiramente suspeita", "Ligeiramente suspeito", "Parcialmente discordante", "Pouco habitual"]:
        return "risco-medio"
    elif valor in ["Muito suspeita", "Muito suspeito", "Discordante"]:
        return "risco-elevado"
    return "risco-neutro"

def classe_selo_risco(risco):
    if risco == "Baixo":
        return "selo-baixo"
    elif risco == "Médio":
        return "selo-medio"
    return "selo-elevado"

def classe_acao_resultado(risco):
    if risco == "Baixo":
        return "acao-baixa"
    elif risco == "Médio":
        return "acao-media"
    return "acao-elevada"

def calcular_indicadores(posicao, velocidade, radar, contexto):
    if posicao == "Muito suspeita":
        i1 = "Elevado"
    elif posicao == "Ligeiramente suspeita":
        i1 = "Médio"
    else:
        i1 = "Baixo"

    if posicao == "Muito suspeita" and radar == "Discordante":
        i2 = "Elevado"
    elif posicao == "Ligeiramente suspeita" or radar == "Parcialmente discordante":
        i2 = "Médio"
    else:
        i2 = "Baixo"

    if velocidade == "Muito suspeito":
        i3 = "Elevado"
    elif velocidade == "Ligeiramente suspeito":
        i3 = "Médio"
    else:
        i3 = "Baixo"

    if posicao == "Muito suspeita" and velocidade == "Muito suspeito":
        i4 = "Elevado"
    elif posicao == "Ligeiramente suspeita" or velocidade == "Ligeiramente suspeito":
        i4 = "Médio"
    else:
        i4 = "Baixo"

    if contexto == "Muito suspeito":
        i5 = "Elevado"
    elif contexto == "Pouco habitual":
        i5 = "Médio"
    else:
        i5 = "Baixo"

    if radar == "Discordante":
        i6 = "Elevado"
    elif radar == "Parcialmente discordante":
        i6 = "Médio"
    else:
        i6 = "Baixo"

    return {"I1": i1, "I2": i2, "I3": i3, "I4": i4, "I5": i5, "I6": i6}

def impacto_textual(contributo):
    if contributo >= 5:
        return "Elevado"
    elif contributo >= 2:
        return "Moderado"
    elif contributo >= 1:
        return "Reduzido"
    return "Muito reduzido"

def novo_id_caso():
    st.session_state.contador_casos += 1
    return f"CASO-{datetime.now().strftime('%Y%m%d')}-{st.session_state.contador_casos:03d}"

def gerar_id_decisao():
    return f"DEC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

def reiniciar_caso():
    st.session_state.resultado_gerado = False
    st.session_state.dados_resultado = None
    st.session_state.decisao_guardada = None

def estado_do_caso():
    if st.session_state.decisao_guardada is not None:
        return "Decisão registada"
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
        return "Recomendação gerada"
    return "Em análise"

def tipo_decisao(acao_proposta_atual, decisao_final):
    if acao_proposta_atual == decisao_final:
        return "Confirmada"
    return "Alterada pelo operador"

def obter_fatores_principais(contributos, top_n=3):
    ordenados = sorted(contributos.items(), key=lambda x: x[1]["Contributo"], reverse=True)
    return [
        {
            "codigo": item[0],
            "nome": item[1]["Nome"],
            "nivel": item[1]["Nível"],
            "contributo": item[1]["Contributo"]
        }
        for item in ordenados[:top_n]
    ]

def formula_caso_texto(contributos):
    termos = []
    total = 0
    for chave in ["I1", "I2", "I3", "I4", "I5", "I6"]:
        pontos = contributos[chave]["Pontos"]
        peso = contributos[chave]["Peso"]
        contributo = contributos[chave]["Contributo"]
        termos.append(f"({chave}: {pontos}×{peso}={contributo})")
        total += contributo
    return " + ".join(termos) + f" = {total}"

def exportar_registo_txt(dados, decisao=None):
    linhas = []
    linhas.append("NAVISGUARD - REGISTO OPERACIONAL")
    linhas.append("=" * 42)
    linhas.append(f"ID do caso: {dados['id_caso']}")
    linhas.append(f"Processado em: {dados['timestamp']}")
    linhas.append(f"Posição/Trajetória: {dados['posicao']}")
    linhas.append(f"Velocidade/Curso: {dados['velocidade']}")
    linhas.append(f"Concordância com radar/outras fontes: {dados['radar']}")
    linhas.append(f"Contexto operacional: {dados['contexto']}")
    linhas.append("")
    linhas.append("Indicadores:")
    for chave in ["I1", "I2", "I3", "I4", "I5", "I6"]:
        info = dados["contributos"][chave]
        linhas.append(
            f"{chave} - {info['Nome']}: Estado={info['Nível']}, Pontos={info['Pontos']}, Peso={info['Peso']}, Contributo={info['Contributo']}"
        )
    linhas.append("")
    linhas.append(f"Pontuação final: {dados['pontuacao_total']}")
    linhas.append(f"Nível de risco: {dados['risco']}")
    linhas.append(f"Ação proposta: {dados['acao']}")
    linhas.append(f"Fórmula aplicada: {formula_caso_texto(dados['contributos'])}")

    if decisao is not None:
        linhas.append("")
        linhas.append("Decisão final:")
        linhas.append(f"ID da decisão: {decisao['id_decisao']}")
        linhas.append(f"Registado em: {decisao['timestamp_decisao']}")
        linhas.append(f"Tipo de decisão: {tipo_decisao(decisao['acao_proposta'], decisao['decisao_final'])}")
        linhas.append(f"Decisão final: {decisao['decisao_final']}")
        linhas.append(f"Justificação: {decisao['justificacao'] if decisao['justificacao'] else 'Não foi fornecida justificação.'}")

    return "\n".join(linhas)

nomes_indicadores = {
    "I1": "Anomalia de identidade",
    "I2": "Alteração anormal de identidade",
    "I3": "Plausibilidade cinemática",
    "I4": "Consistência espaço-temporal",
    "I5": "Consistência contextual",
    "I6": "Consistência entre fontes"
}

siglas_indicadores = {
    "I1": "Identidade",
    "I2": "Alt. identidade",
    "I3": "Cinemática",
    "I4": "Espaço-tempo",
    "I5": "Contexto",
    "I6": "Entre fontes"
}

pesos = {"I1": 3, "I2": 2, "I3": 2, "I4": 2, "I5": 1, "I6": 3}

# -------------------------
# Cabeçalho
# -------------------------

st.markdown("""<div style="position: relative; border-radius:18px; overflow:hidden;">
<img src="logo.jpg" style="width:100%; display:block;">
<div style="position:absolute; top:0; left:0; width:100%; height:100%; pointer-events:none;">
<div class="radar"></div>
</div>
</div>

<style>
.radar {
    position:absolute;
    width:300px;
    height:300px;
    border-radius:50%;
    top:50%;
    left:85%;
    transform:translate(-50%, -50%);
    background: radial-gradient(circle, rgba(0,255,150,0.15) 0%, rgba(0,255,150,0.05) 40%, transparent 70%);
    border: 1px solid rgba(0,255,150,0.2);
    overflow:hidden;
}

.radar::after {
    content:"";
    position:absolute;
    width:50%;
    height:50%;
    top:50%;
    left:50%;
    transform-origin: left top;
    background: linear-gradient(90deg, rgba(0,255,150,0.6), transparent);
    animation: radarSweep 3s linear infinite;
}

@keyframes radarSweep {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>""", unsafe_allow_html=True)

#st.markdown('<div class="topo-dashboard" style="padding:10px;">', unsafe_allow_html=True)
#st.image("logo.jpg", use_container_width=True)
#st.markdown('</div>', unsafe_allow_html=True)

id_atual = st.session_state.dados_resultado["id_caso"] if st.session_state.dados_resultado else "Não iniciado"
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

Com base nos dados introduzidos pelo operador, o sistema:

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
   O operador pode confirmar ou ajustar a recomendação, garantindo controlo humano no processo.

⚠️ **Nota:**  
Esta aplicação é uma **demo conceptual**, desenvolvida para ilustrar a lógica de um sistema de apoio à decisão em contexto marítimo, não substituindo sistemas reais de vigilância ou comando operacional.
""")

# -------------------------
# 1. Processamento operacional
# -------------------------
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

# -------------------------
# Layout principal
# -------------------------
coluna_esquerda, coluna_direita = st.columns([1, 1], gap="large")

# -------------------------
# 2. Coluna esquerda: dados de entrada
# -------------------------
with coluna_esquerda:
    st.markdown('<div class="cartao cartao-azul">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">2. DADOS DE ENTRADA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Nesta secção, o operador descreve o caso em análise.</div>', unsafe_allow_html=True)

    col_titulo_entrada, col_botao_reset = st.columns([3, 1])
    with col_titulo_entrada:
        st.markdown("##### PREPARAÇÃO DO CASO")
    with col_botao_reset:
        st.button("Novo caso", use_container_width=True, on_click=reiniciar_caso)

    st.markdown("##### Dados AIS/VMS")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="etiqueta">Posição/Trajetória</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(posicao) if "posicao" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        posicao = st.selectbox(
            "Posição/Trajetória",
            ["Normal", "Ligeiramente suspeita", "Muito suspeita"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="etiqueta">Velocidade/Curso</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(velocidade) if "velocidade" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        velocidade = st.selectbox(
            "Velocidade/Curso",
            ["Normal", "Ligeiramente suspeito", "Muito suspeito"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("##### Outras fontes")
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown('<div class="etiqueta">Concordância com radar/outras fontes</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(radar) if "radar" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        radar = st.selectbox(
            "Concordância com radar/outras fontes",
            ["Concordante", "Parcialmente discordante", "Discordante"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f:
        st.markdown('<div class="etiqueta">Contexto operacional</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(contexto) if "contexto" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        contexto = st.selectbox(
            "Contexto operacional",
            ["Normal", "Pouco habitual", "Muito suspeito"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    gerar = st.button("Gerar recomendação", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Deteção de alterações
# -------------------------
estado_atual = {
    "posicao": posicao,
    "velocidade": velocidade,
    "radar": radar,
    "contexto": contexto
}

resultado_em_reserva = False

if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
    ultimo_estado = {
        "posicao": st.session_state.dados_resultado["posicao"],
        "velocidade": st.session_state.dados_resultado["velocidade"],
        "radar": st.session_state.dados_resultado["radar"],
        "contexto": st.session_state.dados_resultado["contexto"]
    }
    if estado_atual != ultimo_estado:
        resultado_em_reserva = True

if gerar:
    indicadores = calcular_indicadores(posicao, velocidade, radar, contexto)

    contributos = {}
    pontuacao_total = 0

    for chave, valor in indicadores.items():
        pontos = nivel_para_pontos(valor)
        contributo = pontos * pesos[chave]
        contributos[chave] = {
            "Código": chave,
            "Nome": nomes_indicadores[chave],
            "Nível": valor,
            "Pontos": pontos,
            "Peso": pesos[chave],
            "Contributo": contributo
        }
        pontuacao_total += contributo

    risco = nivel_risco(pontuacao_total)
    acao = acao_proposta(pontuacao_total)

    st.session_state.dados_resultado = {
        "id_caso": novo_id_caso(),
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "posicao": posicao,
        "velocidade": velocidade,
        "radar": radar,
        "contexto": contexto,
        "indicadores": indicadores,
        "contributos": contributos,
        "pontuacao_total": pontuacao_total,
        "risco": risco,
        "acao": acao
    }
    st.session_state.resultado_gerado = True
    st.session_state.decisao_guardada = None
    resultado_em_reserva = False

# -------------------------
# 3 + 4. Coluna direita: avaliação tática + proposta de ação
# -------------------------
with coluna_direita:
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not resultado_em_reserva:
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

    elif st.session_state.resultado_gerado and resultado_em_reserva:
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

# -------------------------
# 5. Confirmação do operador
# -------------------------
if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not resultado_em_reserva:
    dados = st.session_state.dados_resultado
    contributos = dados["contributos"]
    pontuacao_total = dados["pontuacao_total"]
    risco = dados["risco"]
    acao = dados["acao"]

    st.markdown('<div class="cartao cartao-azul">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">5. CONFIRMAÇÃO DO OPERADOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">O operador pode confirmar ou alterar a recomendação automática com justificação.</div>', unsafe_allow_html=True)

    decisao_utilizador = st.selectbox(
        "Decisão final do operador",
        ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"],
        label_visibility="visible"
    )

    justificacao = st.text_area(
        "Justificação da decisão final",
        placeholder="Explica por que motivo confirmas ou alteras a ação proposta...",
        height=180
    )

    alterou_decisao = decisao_utilizador != "Confirmar ação proposta"
    if alterou_decisao:
        st.warning("A justificação é obrigatória quando a decisão final altera a ação proposta pelo sistema.")

    guardar = st.button("Guardar decisão final", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if guardar:
        decisao_final = acao if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador

        if alterou_decisao and not justificacao.strip():
            st.error("Não é possível guardar: a justificação é obrigatória quando alteras a ação proposta.")
        else:
            id_decisao = gerar_id_decisao()
            timestamp_decisao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            st.session_state.decisao_guardada = {
                "id_decisao": id_decisao,
                "timestamp_decisao": timestamp_decisao,
                "acao_proposta": acao,
                "decisao_final": decisao_final,
                "risco": risco,
                "pontuacao_total": pontuacao_total,
                "justificacao": justificacao.strip()
            }

    # -------------------------
    # 6. Decisão final
    # -------------------------
    if st.session_state.decisao_guardada is not None:
        reg = st.session_state.decisao_guardada
        tipo = tipo_decisao(reg["acao_proposta"], reg["decisao_final"])
        classe_tipo = "estado-confirmacao" if tipo == "Confirmada" else "estado-alteracao"

        st.markdown('<div class="cartao cartao-verde">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">6. DECISÃO FINAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Registo final da decisão humana apoiada pelo sistema.</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="bloco-meta">
                <b>ID da decisão:</b> {reg["id_decisao"]}<br>
                <b>Registado em:</b> {reg["timestamp_decisao"]}<br>
                <b>Tipo de decisão:</b> {tipo}<br>
                <span class="{classe_tipo}">{tipo}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Ação proposta", reg["acao_proposta"])
        with r2:
            st.metric("Decisão final", reg["decisao_final"])
        with r3:
            st.metric("Nível de risco", reg["risco"])
        with r4:
            st.metric("Pontuação total", reg["pontuacao_total"])

        st.markdown("#### Justificação operacional")
        if reg["justificacao"]:
            st.write(reg["justificacao"])
        else:
            st.write("Não foi fornecida justificação.")

        st.success("Decisão final registada com sucesso no sistema.")

        if st.session_state.dados_resultado is not None:
            conteudo_txt = exportar_registo_txt(st.session_state.dados_resultado, reg)
            st.download_button(
                label="Exportar registo TXT",
                data=conteudo_txt,
                file_name=f"{st.session_state.dados_resultado['id_caso']}_{reg['id_decisao']}.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------
    # 7. Quadro de indicadores
    # -------------------------
    st.markdown('<div class="cartao">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">7. QUADRO DE INDICADORES</div>', unsafe_allow_html=True)
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


elif st.session_state.resultado_gerado and resultado_em_reserva:
    st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">Informação em reserva</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">O caso foi alterado após a última geração.</div>', unsafe_allow_html=True)
    st.warning("As entradas foram alteradas. Gere nova recomendação para atualizar a avaliação tática, a rastreabilidade e a confirmação do operador.")
    st.markdown('</div>', unsafe_allow_html=True)
