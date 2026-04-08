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
# CSS — Clean & Corporativo
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ── FUNDO ── */
.stApp {
    background-color: #f5f7fa !important;
}

/* ── CABEÇALHO ── */
.ng-header {
    background: #ffffff;
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 16px;
    border: 1px solid #e8ecf0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}
.ng-header-left { flex: 1; }
.ng-logo-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 4px;
}
.ng-logo-icon {
    width: 40px; height: 40px;
    background: #1d4ed8;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}
.ng-title {
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    line-height: 1;
}
.ng-subtitle {
    font-size: 0.88rem;
    color: #64748b;
    font-weight: 400;
    margin-left: 54px;
}
.ng-header-right {
    display: flex;
    gap: 20px;
    flex-shrink: 0;
}
.ng-header-stat {
    text-align: right;
    border-left: 1px solid #e8ecf0;
    padding-left: 20px;
}
.ng-header-stat .val {
    font-size: 1.1rem;
    font-weight: 700;
    color: #0f172a;
    display: block;
}
.ng-header-stat .lbl {
    font-size: 0.72rem;
    color: #94a3b8;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.ng-live {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 600;
    color: #15803d;
    margin-bottom: 4px;
}
.ng-live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulse-green 2s infinite;
}

/* ── BARRA DE ESTADO ── */
.ng-status-bar {
    background: #ffffff;
    border: 1px solid #e8ecf0;
    border-radius: 10px;
    padding: 12px 20px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.85rem;
    color: #475569;
    font-weight: 500;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.ng-status-bar .ng-case-id {
    font-weight: 700;
    color: #1d4ed8;
    font-family: 'Inter', monospace;
    font-size: 0.82rem;
}
.ng-status-bar .sep { color: #cbd5e1; }
.ng-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    border: 1px solid;
}
.ng-badge-blue { background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }
.ng-badge-green { background: #f0fdf4; color: #15803d; border-color: #bbf7d0; }
.ng-badge-amber { background: #fffbeb; color: #92400e; border-color: #fde68a; }

/* ── CARDS ── */
.ng-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 24px;
    border: 1px solid #e8ecf0;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 16px;
}
.ng-card-blue {
    background: #ffffff;
    border-top: 3px solid #1d4ed8;
}
.ng-card-green {
    background: #ffffff;
    border-top: 3px solid #16a34a;
}
.ng-card-amber {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-top: 3px solid #d97706;
}
.ng-card-red {
    background: #fff5f5;
    border: 1px solid #fecaca;
    border-top: 3px solid #dc2626;
}

/* ── SECTION HEADER ── */
.ng-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2px;
}
.ng-section-heading {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 2px;
}
.ng-section-sub {
    font-size: 0.83rem;
    color: #64748b;
    margin-bottom: 18px;
    font-weight: 400;
}
.ng-divider {
    border: none;
    border-top: 1px solid #f1f5f9;
    margin: 16px 0;
}

/* ── INPUT LABELS ── */
.ng-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #374151;
    margin-top: 10px;
    margin-bottom: 6px;
    display: block;
}
.ng-group-label {
    font-size: 0.7rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin: 14px 0 8px 0;
    display: block;
}

/* ── SELECTBOX ── */
div[data-baseweb="select"] > div {
    border-radius: 8px !important;
    min-height: 42px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #0f172a !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: #93c5fd !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
}
.risco-baixo div[data-baseweb="select"] > div {
    background: #f0fdf4 !important;
    border-color: #86efac !important;
    color: #15803d !important;
}
.risco-medio div[data-baseweb="select"] > div {
    background: #fffbeb !important;
    border-color: #fcd34d !important;
    color: #92400e !important;
}
.risco-elevado div[data-baseweb="select"] > div {
    background: #fff1f2 !important;
    border-color: #fca5a5 !important;
    color: #dc2626 !important;
}
.risco-neutro div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border-color: #d1d5db !important;
    color: #0f172a !important;
}

/* ── BUTTONS ── */
div.stButton > button {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    box-shadow: 0 1px 3px rgba(29,78,216,0.3) !important;
    transition: background 0.15s, box-shadow 0.15s !important;
    letter-spacing: 0.01em !important;
}
div.stButton > button:hover {
    background: #1e40af !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.35) !important;
    color: #ffffff !important;
}
div.stButton > button:focus {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.25) !important;
}

/* ── TEXTAREA ── */
textarea {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    color: #0f172a !important;
    background: #ffffff !important;
}
textarea:focus {
    border-color: #1d4ed8 !important;
    box-shadow: 0 0 0 3px rgba(29,78,216,0.1) !important;
}

/* ── LABELS STREAMLIT ── */
label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: #f8fafc !important;
    border: 1px solid #e8ecf0 !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.35rem !important;
    font-weight: 800 !important;
    color: #0f172a !important;
}

/* ── ALERTS ── */
div[data-testid="stNotification"] {
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── EXPANDER ── */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    background: #f8fafc !important;
    border-radius: 8px !important;
    border: 1px solid #e8ecf0 !important;
}
.streamlit-expanderContent {
    background: #fafafa !important;
    border: 1px solid #e8ecf0 !important;
    border-top: none !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    color: #374151 !important;
}

/* ── INDICATOR MINI CARD ── */
.ng-stat {
    background: #f8fafc;
    border: 1px solid #e8ecf0;
    border-radius: 10px;
    padding: 14px 16px;
    text-align: center;
}
.ng-stat .v { font-size: 1.6rem; font-weight: 800; color: #0f172a; }
.ng-stat .l { font-size: 0.72rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; }

/* ── INDICATOR ROW CARD ── */
.ng-ind {
    background: #f8fafc;
    border: 1px solid #e8ecf0;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: 12px;
}
.ng-ind-low  { border-left: 3px solid #22c55e; }
.ng-ind-med  { border-left: 3px solid #f59e0b; }
.ng-ind-high { border-left: 3px solid #ef4444; }
.ng-ind-code {
    font-size: 0.72rem;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.08em;
    min-width: 26px;
}
.ng-ind-name { font-size: 0.88rem; font-weight: 600; color: #0f172a; }
.ng-ind-sub  { font-size: 0.76rem; color: #64748b; font-weight: 400; }
.ng-ind-right { text-align: right; }
.ng-ind-score {
    font-size: 1rem;
    font-weight: 800;
    color: #0f172a;
}
.ng-ind-weight { font-size: 0.7rem; color: #94a3b8; }

/* ── RISK PILL ── */
.ng-risk {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.ng-risk-low  { background: #f0fdf4; color: #15803d; border: 1px solid #86efac; }
.ng-risk-med  { background: #fffbeb; color: #92400e; border: 1px solid #fcd34d; }
.ng-risk-high { background: #fff1f2; color: #dc2626; border: 1px solid #fca5a5; }

/* ── ACTION BOX ── */
.ng-action {
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 12px;
    letter-spacing: 0.02em;
}
.ng-action-low  { background: #f0fdf4; color: #15803d; border: 1px solid #86efac; }
.ng-action-med  { background: #fffbeb; color: #92400e; border: 1px solid #fcd34d; }
.ng-action-high { background: #fff1f2; color: #dc2626; border: 1px solid #fca5a5; }

/* ── RESULT HEADER CARD ── */
.ng-result-header {
    background: #f8fafc;
    border: 1px solid #e8ecf0;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.ng-result-header .meta-id {
    font-size: 0.78rem;
    font-weight: 700;
    color: #1d4ed8;
    font-family: 'Inter', monospace;
}
.ng-result-header .meta-ts {
    font-size: 0.75rem;
    color: #94a3b8;
    margin-top: 2px;
}

/* ── CRITICAL BADGE ── */
.ng-critical {
    display: inline-block;
    background: #fff1f2;
    color: #dc2626;
    border: 1px solid #fca5a5;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* ── FORMULA ── */
.ng-formula {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px 14px;
    font-family: 'Inter', monospace;
    font-size: 0.8rem;
    color: #334155;
    margin-top: 8px;
}

/* ── DECISION BADGE ── */
.ng-dec-confirmed { background:#f0fdf4; color:#15803d; border:1px solid #86efac; border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700; }
.ng-dec-changed   { background:#fffbeb; color:#92400e; border:1px solid #fcd34d; border-radius:999px; padding:3px 10px; font-size:0.72rem; font-weight:700; }

/* ── DOWNLOAD BUTTON ── */
[data-testid="stDownloadButton"] button {
    background: #ffffff !important;
    color: #374151 !important;
    border: 1px solid #d1d5db !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: #f8fafc !important;
    border-color: #9ca3af !important;
    color: #111827 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── ANIMATIONS ── */
@keyframes pulse-green {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
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

def classe_cartao_indicador(contributo):
    if contributo >= 5:
        return "ng-ind-high"
    elif contributo >= 2:
        return "ng-ind-med"
    return "ng-ind-low"

def classe_risco_input(valor):
    if valor in ["Normal", "Concordante"]:
        return "risco-baixo"
    elif valor in ["Ligeiramente suspeita", "Ligeiramente suspeito", "Parcialmente discordante", "Pouco habitual"]:
        return "risco-medio"
    elif valor in ["Muito suspeita", "Muito suspeito", "Discordante"]:
        return "risco-elevado"
    return "risco-neutro"

def classe_risco_pill(risco):
    if risco == "Baixo": return "ng-risk-low"
    elif risco == "Médio": return "ng-risk-med"
    return "ng-risk-high"

def classe_acao_box(risco):
    if risco == "Baixo": return "ng-action-low"
    elif risco == "Médio": return "ng-action-med"
    return "ng-action-high"

def calcular_indicadores(posicao, velocidade, radar, contexto):
    i1 = "Elevado" if posicao == "Muito suspeita" else ("Médio" if posicao == "Ligeiramente suspeita" else "Baixo")
    i2 = "Elevado" if (posicao == "Muito suspeita" and radar == "Discordante") else ("Médio" if (posicao == "Ligeiramente suspeita" or radar == "Parcialmente discordante") else "Baixo")
    i3 = "Elevado" if velocidade == "Muito suspeito" else ("Médio" if velocidade == "Ligeiramente suspeito" else "Baixo")
    i4 = "Elevado" if (posicao == "Muito suspeita" and velocidade == "Muito suspeito") else ("Médio" if (posicao == "Ligeiramente suspeita" or velocidade == "Ligeiramente suspeito") else "Baixo")
    i5 = "Elevado" if contexto == "Muito suspeito" else ("Médio" if contexto == "Pouco habitual" else "Baixo")
    i6 = "Elevado" if radar == "Discordante" else ("Médio" if radar == "Parcialmente discordante" else "Baixo")
    return {"I1": i1, "I2": i2, "I3": i3, "I4": i4, "I5": i5, "I6": i6}

def impacto_textual(c):
    if c >= 5: return "Elevado"
    elif c >= 2: return "Moderado"
    elif c >= 1: return "Reduzido"
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

def tipo_decisao(acao_prop, dec_final):
    return "Confirmada" if acao_prop == dec_final else "Alterada pelo operador"

def obter_fatores_principais(contributos, top_n=3):
    ordenados = sorted(contributos.items(), key=lambda x: x[1]["Contributo"], reverse=True)
    return [{"codigo": k, "nome": v["Nome"], "nivel": v["Nível"], "contributo": v["Contributo"]} for k, v in ordenados[:top_n]]

def formula_caso_texto(contributos):
    termos, total = [], 0
    for c in ["I1","I2","I3","I4","I5","I6"]:
        p, w, cont = contributos[c]["Pontos"], contributos[c]["Peso"], contributos[c]["Contributo"]
        termos.append(f"({c}: {p}×{w}={cont})")
        total += cont
    return " + ".join(termos) + f" = {total}"

def exportar_registo_txt(dados, decisao=None):
    linhas = ["NAVISGUARD — REGISTO OPERACIONAL", "=" * 44,
              f"ID do caso: {dados['id_caso']}", f"Processado em: {dados['timestamp']}",
              f"Posição/Trajetória: {dados['posicao']}", f"Velocidade/Curso: {dados['velocidade']}",
              f"Concordância radar: {dados['radar']}", f"Contexto operacional: {dados['contexto']}", ""]
    linhas.append("Indicadores:")
    for c in ["I1","I2","I3","I4","I5","I6"]:
        info = dados["contributos"][c]
        linhas.append(f"  {c} — {info['Nome']}: {info['Nível']} | Pontos={info['Pontos']} | Peso={info['Peso']} | Contributo={info['Contributo']}")
    linhas += ["", f"Pontuação final: {dados['pontuacao_total']}", f"Nível de risco: {dados['risco']}", f"Ação proposta: {dados['acao']}", f"Fórmula: {formula_caso_texto(dados['contributos'])}"]
    if decisao:
        linhas += ["", "Decisão final:", f"  ID: {decisao['id_decisao']}", f"  Registado em: {decisao['timestamp_decisao']}",
                   f"  Tipo: {tipo_decisao(decisao['acao_proposta'], decisao['decisao_final'])}",
                   f"  Decisão: {decisao['decisao_final']}",
                   f"  Justificação: {decisao['justificacao'] or 'Não fornecida.'}"]
    return "\n".join(linhas)

nomes_indicadores = {
    "I1": "Anomalia de identidade", "I2": "Alteração anormal de identidade",
    "I3": "Plausibilidade cinemática", "I4": "Consistência espaço-temporal",
    "I5": "Consistência contextual", "I6": "Consistência entre fontes"
}
siglas_indicadores = {
    "I1": "Identidade", "I2": "Alt. Identidade", "I3": "Cinemática",
    "I4": "Espaço-Tempo", "I5": "Contexto", "I6": "Entre Fontes"
}
pesos = {"I1": 3, "I2": 2, "I3": 2, "I4": 2, "I5": 1, "I6": 3}

# ─────────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────────
ts_now = datetime.now().strftime("%d %b %Y  %H:%M")
st.markdown(f"""
<div class="ng-header">
    <div class="ng-header-left">
        <div class="ng-logo-row">
            <div class="ng-logo-icon">🛡️</div>
            <span class="ng-title">NAVISGUARD</span>
        </div>
        <div class="ng-subtitle">Sistema de Apoio e Validação da Decisão em Ambiente Marítimo</div>
    </div>
    <div class="ng-header-right">
        <div class="ng-header-stat">
            <span class="val">AIS · VMS · RAD</span>
            <span class="lbl">Fontes ativas</span>
        </div>
        <div class="ng-header-stat">
            <div class="ng-live"><div class="ng-live-dot"></div> Online</div>
            <span class="lbl">{ts_now}</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# BARRA DE ESTADO
# ─────────────────────────────────────────────
id_atual = st.session_state.dados_resultado["id_caso"] if st.session_state.dados_resultado else "—"
estado_str = estado_do_caso()
badge_class = "ng-badge-green" if "registada" in estado_str.lower() else ("ng-badge-blue" if "gerada" in estado_str.lower() else "ng-badge-amber")

st.markdown(f"""
<div class="ng-status-bar">
    <span>Caso ativo:</span>
    <span class="ng-case-id">{id_atual}</span>
    <span class="sep">·</span>
    <span class="ng-badge {badge_class}">{estado_str}</span>
</div>
""", unsafe_allow_html=True)

with st.expander("Sobre o sistema"):
    st.write("""
Esta plataforma avalia comportamentos potencialmente anómalos de embarcações com base em dados de AIS, VMS, radar e contexto operacional.

O sistema gera 6 indicadores internos (I1–I6), calcula uma pontuação ponderada, classifica o nível de risco (**Baixo / Médio / Elevado**) e propõe uma ação (**Ignorar / Monitorizar / Escalar**). O operador pode confirmar ou ajustar a recomendação.

⚠️ **Demo conceptual** — não substitui sistemas reais de vigilância ou comando operacional.
""")

# ─────────────────────────────────────────────
# SECÇÃO 1 — PROCESSAMENTO
# ─────────────────────────────────────────────
st.markdown('<div class="ng-card">', unsafe_allow_html=True)
st.markdown('<div class="ng-section-title">Secção 01</div>', unsafe_allow_html=True)
st.markdown('<div class="ng-section-heading">Processamento operacional</div>', unsafe_allow_html=True)
st.markdown('<div class="ng-section-sub">O sistema gera indicadores, calcula o risco e emite uma recomendação automática.</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="ng-stat"><div class="v">6</div><div class="l">Indicadores internos</div></div>', unsafe_allow_html=True)
    with st.expander("Ver indicadores"):
        st.markdown("""
**I1** — Identidade *(Posição/Trajetória)*
**I2** — Alt. Identidade *(Posição + Radar)*
**I3** — Cinemática *(Velocidade/Curso)*
**I4** — Espaço-Temporal *(Posição + Velocidade)*
**I5** — Contexto *(Contexto operacional)*
**I6** — Entre Fontes *(Concordância Radar)*
""")
with c2:
    st.markdown('<div class="ng-stat"><div class="v">3</div><div class="l">Níveis de risco</div></div>', unsafe_allow_html=True)
    with st.expander("Ver níveis"):
        st.markdown("**Baixo** — Sem impacto  \n**Médio** — Atenção  \n**Elevado** — Prioridade máxima")
with c3:
    st.markdown('<div class="ng-stat"><div class="v">4</div><div class="l">Ações possíveis</div></div>', unsafe_allow_html=True)
    with st.expander("Ver ações"):
        st.markdown("**Ignorar** — Sem ação  \n**Monitorizar** — Vigilância  \n**Escalar** — Intervenção  \n**Rever** — Análise adicional")
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
col_esq, col_dir = st.columns([1, 1], gap="large")

# ─────────────────────────────────────────────
# SECÇÃO 2 — DADOS DE ENTRADA
# ─────────────────────────────────────────────
with col_esq:
    st.markdown('<div class="ng-card ng-card-blue">', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-title">Secção 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-heading">Dados de entrada</div>', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-sub">Descreve o caso em análise com base nos dados disponíveis.</div>', unsafe_allow_html=True)

    col_t, col_r = st.columns([3, 1])
    with col_r:
        st.button("Novo caso", use_container_width=True, on_click=reiniciar_caso)

    st.markdown('<span class="ng-group-label">Dados AIS / VMS</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.markdown('<span class="ng-label">Posição / Trajetória</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(posicao) if "posicao" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        posicao = st.selectbox("Posição/Trajetória", ["Normal", "Ligeiramente suspeita", "Muito suspeita"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<span class="ng-label">Velocidade / Curso</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(velocidade) if "velocidade" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        velocidade = st.selectbox("Velocidade/Curso", ["Normal", "Ligeiramente suspeito", "Muito suspeito"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<span class="ng-group-label">Outras fontes</span>', unsafe_allow_html=True)
    ce, cf = st.columns(2)
    with ce:
        st.markdown('<span class="ng-label">Concordância com radar</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(radar) if "radar" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        radar = st.selectbox("Radar", ["Concordante", "Parcialmente discordante", "Discordante"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
    with cf:
        st.markdown('<span class="ng-label">Contexto operacional</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(contexto) if "contexto" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        contexto = st.selectbox("Contexto", ["Normal", "Pouco habitual", "Muito suspeito"], label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    gerar = st.button("Gerar recomendação", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Deteção de alterações
# ─────────────────────────────────────────────
estado_atual = {"posicao": posicao, "velocidade": velocidade, "radar": radar, "contexto": contexto}
resultado_em_reserva = False
if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
    ultimo_estado = {k: st.session_state.dados_resultado[k] for k in ["posicao","velocidade","radar","contexto"]}
    if estado_atual != ultimo_estado:
        resultado_em_reserva = True

if gerar:
    indicadores = calcular_indicadores(posicao, velocidade, radar, contexto)
    contributos = {}
    pontuacao_total = 0
    for chave, valor in indicadores.items():
        pontos = nivel_para_pontos(valor)
        contributo = pontos * pesos[chave]
        contributos[chave] = {"Código": chave, "Nome": nomes_indicadores[chave], "Nível": valor,
                               "Pontos": pontos, "Peso": pesos[chave], "Contributo": contributo}
        pontuacao_total += contributo
    risco = nivel_risco(pontuacao_total)
    acao = acao_proposta(pontuacao_total)
    st.session_state.dados_resultado = {
        "id_caso": novo_id_caso(), "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "posicao": posicao, "velocidade": velocidade, "radar": radar, "contexto": contexto,
        "indicadores": indicadores, "contributos": contributos,
        "pontuacao_total": pontuacao_total, "risco": risco, "acao": acao
    }
    st.session_state.resultado_gerado = True
    st.session_state.decisao_guardada = None
    resultado_em_reserva = False

# ─────────────────────────────────────────────
# SECÇÕES 3 + 4 — COLUNA DIREITA
# ─────────────────────────────────────────────
with col_dir:
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not resultado_em_reserva:
        dados = st.session_state.dados_resultado
        contributos = dados["contributos"]
        pontuacao_total = dados["pontuacao_total"]
        risco = dados["risco"]
        acao = dados["acao"]
        fatores_principais = obter_fatores_principais(contributos, top_n=3)

        # ── SECÇÃO 3
        st.markdown('<div class="ng-card">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 03</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-heading">Avaliação tática</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-sub">Síntese dos fatores críticos e impacto na recomendação.</div>', unsafe_allow_html=True)

        st.info("Avaliação concluída.")
        st.markdown(f"**Nível de risco:** {risco} &nbsp;&nbsp; **Ação proposta:** {acao}")
        st.markdown("**Fatores críticos identificados:**")
        for idx, f in enumerate(fatores_principais):
            pref = "Principal —" if idx == 0 else "        —"
            st.write(f"{pref} {f['nome']}")
        st.markdown('</div>', unsafe_allow_html=True)

        # ── SECÇÃO 4
        st.markdown('<div class="ng-card">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 04</div>', unsafe_allow_html=True)

        col_h1, col_h2 = st.columns([3,1])
        with col_h1:
            st.markdown('<div class="ng-section-heading">Proposta de ação</div>', unsafe_allow_html=True)
            st.markdown('<div class="ng-section-sub">Recomendação automática baseada nas entradas submetidas.</div>', unsafe_allow_html=True)
        with col_h2:
            st.markdown(f'<div style="text-align:right; padding-top:4px;"><span class="ng-risk {classe_risco_pill(risco)}">Risco {risco}</span></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ng-result-header">
            <div>
                <div class="meta-id">{dados['id_caso']}</div>
                <div class="meta-ts">{dados['timestamp']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Pontuação", pontuacao_total)
        with m2: st.metric("Nível de risco", risco)
        with m3: st.metric("Ação proposta", acao)

        st.markdown(f'<div class="ng-action {classe_acao_box(risco)}">Ação recomendada: {acao}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.resultado_gerado and resultado_em_reserva:
        st.markdown('<div class="ng-card ng-card-amber">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 03</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-heading">Avaliação tática</div>', unsafe_allow_html=True)
        st.warning("As entradas foram alteradas. Gere nova recomendação para atualizar a avaliação.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-card ng-card-amber">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 04</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-heading">Proposta de ação</div>', unsafe_allow_html=True)
        st.warning("Resultado anterior suspenso. Regenere para nova validação.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="ng-card">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 03</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-heading">Avaliação tática</div>', unsafe_allow_html=True)
        st.info("A avaliação tática será apresentada após gerar a recomendação.")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-card">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 04</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-heading">Proposta de ação</div>', unsafe_allow_html=True)
        st.info('Introduza os dados do caso e clique em "Gerar recomendação".')
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SECÇÃO 5 — CONFIRMAÇÃO DO OPERADOR
# ─────────────────────────────────────────────
if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not resultado_em_reserva:
    dados = st.session_state.dados_resultado
    contributos = dados["contributos"]
    pontuacao_total = dados["pontuacao_total"]
    risco = dados["risco"]
    acao = dados["acao"]

    st.markdown('<div class="ng-card ng-card-blue">', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-title">Secção 05</div>', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-heading">Confirmação do operador</div>', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-sub">O operador pode confirmar ou ajustar a recomendação automática.</div>', unsafe_allow_html=True)

    decisao_utilizador = st.selectbox(
        "Decisão final do operador",
        ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"]
    )
    justificacao = st.text_area(
        "Justificação da decisão",
        placeholder="Explica o motivo da confirmação ou da alteração da ação proposta...",
        height=140
    )
    alterou_decisao = decisao_utilizador != "Confirmar ação proposta"
    if alterou_decisao:
        st.warning("A justificação é obrigatória quando a decisão altera a ação proposta pelo sistema.")

    guardar = st.button("Registar decisão final", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if guardar:
        decisao_final = acao if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador
        if alterou_decisao and not justificacao.strip():
            st.error("A justificação é obrigatória quando alteras a ação proposta.")
        else:
            st.session_state.decisao_guardada = {
                "id_decisao": gerar_id_decisao(),
                "timestamp_decisao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "acao_proposta": acao, "decisao_final": decisao_final,
                "risco": risco, "pontuacao_total": pontuacao_total,
                "justificacao": justificacao.strip()
            }

    # ─────────────────────────────────────────────
    # SECÇÃO 6 — DECISÃO FINAL
    # ─────────────────────────────────────────────
    if st.session_state.decisao_guardada is not None:
        reg = st.session_state.decisao_guardada
        tipo = tipo_decisao(reg["acao_proposta"], reg["decisao_final"])
        classe_dec = "ng-dec-confirmed" if tipo == "Confirmada" else "ng-dec-changed"

        st.markdown('<div class="ng-card ng-card-green">', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-title">Secção 06</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-heading">Decisão final</div>', unsafe_allow_html=True)
        st.markdown('<div class="ng-section-sub">Registo da decisão humana validada pelo operador.</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ng-result-header">
            <div>
                <div class="meta-id">{reg['id_decisao']}</div>
                <div class="meta-ts">{reg['timestamp_decisao']}</div>
            </div>
            <span class="{classe_dec}">{tipo}</span>
        </div>
        """, unsafe_allow_html=True)

        r1, r2, r3, r4 = st.columns(4)
        with r1: st.metric("Ação proposta", reg["acao_proposta"])
        with r2: st.metric("Decisão final", reg["decisao_final"])
        with r3: st.metric("Nível de risco", reg["risco"])
        with r4: st.metric("Pontuação", reg["pontuacao_total"])

        st.markdown("**Justificação operacional**")
        st.write(reg["justificacao"] if reg["justificacao"] else "Sem justificação registada.")
        st.success("Decisão final registada com sucesso.")

        if st.session_state.dados_resultado is not None:
            conteudo_txt = exportar_registo_txt(st.session_state.dados_resultado, reg)
            st.download_button(
                label="Exportar registo operacional (.txt)",
                data=conteudo_txt,
                file_name=f"{st.session_state.dados_resultado['id_caso']}_{reg['id_decisao']}.txt",
                mime="text/plain",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECÇÃO 7 — QUADRO DE INDICADORES
    # ─────────────────────────────────────────────
    st.markdown('<div class="ng-card">', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-title">Secção 07</div>', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-heading">Quadro de indicadores</div>', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-sub">Estado, peso e contributo de cada indicador para a decisão.</div>', unsafe_allow_html=True)

    fatores_top = {f["codigo"] for f in obter_fatores_principais(contributos, top_n=3)}
    pares = [(c, contributos[c]) for c in ["I1","I2","I3","I4","I5","I6"]]

    for i in range(0, len(pares), 2):
        cod_a, info_a = pares[i]
        cod_b, info_b = pares[i+1]
        cls_a = classe_cartao_indicador(info_a["Contributo"])
        cls_b = classe_cartao_indicador(info_b["Contributo"])
        badge_a = '<span class="ng-critical">Fator crítico</span><br>' if cod_a in fatores_top else ""
        badge_b = '<span class="ng-critical">Fator crítico</span><br>' if cod_b in fatores_top else ""

        html_a = (
            f'<div class="ng-ind {cls_a}">' +
            f'<div><div class="ng-ind-code">{cod_a}</div></div>' +
            f'<div>{badge_a}<div class="ng-ind-name">{siglas_indicadores[cod_a]}</div>' +
            f'<div class="ng-ind-sub">{info_a["Nível"]} · Impacto {impacto_textual(info_a["Contributo"]).lower()}</div></div>' +
            f'<div class="ng-ind-right"><div class="ng-ind-score">{info_a["Contributo"]}</div>' +
            f'<div class="ng-ind-weight">×{info_a["Peso"]}</div></div></div>'
        )
        html_b = (
            f'<div class="ng-ind {cls_b}">' +
            f'<div><div class="ng-ind-code">{cod_b}</div></div>' +
            f'<div>{badge_b}<div class="ng-ind-name">{siglas_indicadores[cod_b]}</div>' +
            f'<div class="ng-ind-sub">{info_b["Nível"]} · Impacto {impacto_textual(info_b["Contributo"]).lower()}</div></div>' +
            f'<div class="ng-ind-right"><div class="ng-ind-score">{info_b["Contributo"]}</div>' +
            f'<div class="ng-ind-weight">×{info_b["Peso"]}</div></div></div>'
        )

        ca, cb = st.columns(2, gap="small")
        with ca:
            st.markdown(html_a, unsafe_allow_html=True)
        with cb:
            st.markdown(html_b, unsafe_allow_html=True)

    with st.expander("Ver regra de cálculo"):
        st.markdown(f"""
**Pesos dos indicadores:** I1=3 · I2=2 · I3=2 · I4=2 · I5=1 · I6=3

**Estados:** Baixo = 0 pts · Médio = 1 pt · Elevado = 2 pts

**Fórmula:** Pontuação = Σ (pontosᵢ × pesoᵢ)

**Limiares:** ≤ 4 → Baixo / Ignorar · ≤ 8 → Médio / Monitorizar · > 8 → Elevado / Escalar
""")
        st.markdown(f'<div class="ng-formula">{formula_caso_texto(contributos)}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.resultado_gerado and resultado_em_reserva:
    st.markdown('<div class="ng-card ng-card-amber">', unsafe_allow_html=True)
    st.markdown('<div class="ng-section-heading">Informação em reserva</div>', unsafe_allow_html=True)
    st.warning("As entradas foram alteradas. Gere nova recomendação para atualizar a avaliação e os indicadores.")
    st.markdown('</div>', unsafe_allow_html=True)
