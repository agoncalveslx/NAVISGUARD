import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(
    page_title="NAVISGUARD // NATO RESTRICTED",
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
# Estilo visual NATO / Militar
# -------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

    /* ─── BASE ─────────────────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Rajdhani', 'Share Tech Mono', monospace !important;
    }

    .stApp {
        background-color: #040d06 !important;
        background-image:
            linear-gradient(rgba(0,255,80,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0,255,80,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
    }

    /* Scanline overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0,0,0,0.15) 2px,
            rgba(0,0,0,0.15) 4px
        );
        pointer-events: none;
        z-index: 9999;
    }

    /* ─── CLASSIFICATION BANNER ────────────────────────────────── */
    .classification-banner {
        background: #b80000;
        color: #fff;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.25em;
        padding: 4px 0;
        margin-bottom: 0;
        border-bottom: 2px solid #ff2222;
        text-shadow: 0 0 8px rgba(255,80,80,0.8);
    }

    /* ─── HEADER ────────────────────────────────────────────────── */
    .topo-dashboard {
        background: linear-gradient(180deg, #050f07 0%, #071a0a 100%);
        border: 1px solid #0d5c1e;
        border-top: 3px solid #00ff50;
        padding: 22px 28px;
        border-radius: 4px;
        margin-bottom: 14px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0,255,80,0.12), inset 0 0 60px rgba(0,20,8,0.5);
    }
    .topo-dashboard::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 8px,
            rgba(0,255,80,0.01) 8px,
            rgba(0,255,80,0.01) 16px
        );
        pointer-events: none;
    }
    .topo-dashboard .header-grid {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 16px;
    }
    .topo-dashboard .header-left { flex: 1; }
    .topo-dashboard .system-id {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.65rem;
        color: #00ff5088;
        letter-spacing: 0.18em;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .topo-dashboard h1 {
        margin: 0;
        font-size: 2.6rem;
        font-weight: 700;
        color: #00ff50;
        text-shadow: 0 0 18px rgba(0,255,80,0.7), 0 0 40px rgba(0,255,80,0.3);
        letter-spacing: 0.08em;
        font-family: 'Share Tech Mono', monospace;
    }
    .topo-dashboard .subtitle {
        margin-top: 6px;
        font-size: 0.9rem;
        color: #5aff8a;
        letter-spacing: 0.06em;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    .topo-dashboard .header-right {
        text-align: right;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.7rem;
        color: #00ff5066;
        letter-spacing: 0.1em;
        line-height: 1.9;
        border-left: 1px solid #0d5c1e;
        padding-left: 20px;
        min-width: 180px;
    }
    .topo-dashboard .header-right .live-dot {
        display: inline-block;
        width: 7px; height: 7px;
        background: #00ff50;
        border-radius: 50%;
        margin-right: 5px;
        box-shadow: 0 0 8px #00ff50;
        animation: blink 1.4s infinite;
        vertical-align: middle;
    }
    .corner-tl, .corner-tr, .corner-bl, .corner-br {
        position: absolute;
        width: 16px; height: 16px;
        border-color: #00ff50;
        border-style: solid;
        opacity: 0.6;
    }
    .corner-tl { top: 8px; left: 8px; border-width: 2px 0 0 2px; }
    .corner-tr { top: 8px; right: 8px; border-width: 2px 2px 0 0; }
    .corner-bl { bottom: 8px; left: 8px; border-width: 0 0 2px 2px; }
    .corner-br { bottom: 8px; right: 8px; border-width: 0 2px 2px 0; }

    /* ─── BARRA DE ESTADO ────────────────────────────────────────── */
    .barra-estado-caso {
        background: linear-gradient(90deg, #040d06 0%, #071408 100%);
        color: #5aff8a;
        border-radius: 3px;
        padding: 10px 16px;
        margin-bottom: 14px;
        border: 1px solid #0d4018;
        border-left: 3px solid #00ff50;
        box-shadow: 0 0 12px rgba(0,255,80,0.06);
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.1em;
    }
    .barra-estado-caso b { color: #00ff50; }

    /* ─── CARDS ─────────────────────────────────────────────────── */
    .cartao {
        background: linear-gradient(180deg, #05120a 0%, #040d06 100%);
        padding: 20px;
        border-radius: 4px;
        border: 1px solid #0d4018;
        border-top: 2px solid #1a7a34;
        margin-bottom: 16px;
        position: relative;
        box-shadow: 0 0 20px rgba(0,255,80,0.04), inset 0 0 30px rgba(0,0,0,0.3);
    }
    .cartao-azul {
        background: linear-gradient(180deg, #040e12 0%, #030c10 100%);
        border-color: #0d3d4d;
        border-top-color: #1a7aaa;
    }
    .cartao-verde {
        background: linear-gradient(180deg, #040f06 0%, #051008 100%);
        border-color: #0a4018;
        border-top-color: #00ff50;
    }
    .cartao-amarelo {
        background: linear-gradient(180deg, #100e03 0%, #0d0b02 100%);
        border-color: #3d3300;
        border-top-color: #ffb000;
    }
    .cartao-vermelho {
        background: linear-gradient(180deg, #100303 0%, #0d0202 100%);
        border-color: #3d0a0a;
        border-top-color: #ff3333;
    }

    /* ─── SECTION TITLES ─────────────────────────────────────────── */
    .titulo-secao {
        font-size: 0.8rem;
        font-weight: 700;
        color: #00ff50;
        letter-spacing: 0.2em;
        margin-bottom: 3px;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 10px rgba(0,255,80,0.5);
    }
    .subtitulo-secao {
        font-size: 0.82rem;
        color: #3a8a52;
        letter-spacing: 0.05em;
        margin-bottom: 14px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    .etiqueta {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        color: #3aaa5a;
        letter-spacing: 0.12em;
        margin-top: 10px;
        margin-bottom: 6px;
        text-transform: uppercase;
    }

    /* ─── MINI INDICATORS ────────────────────────────────────────── */
    .mini-indicador {
        background: #040d06;
        border: 1px solid #0d4018;
        border-top: 2px solid #1a7a34;
        border-radius: 3px;
        padding: 14px;
        text-align: center;
        box-shadow: 0 0 16px rgba(0,255,80,0.05);
        position: relative;
        overflow: hidden;
    }
    .mini-indicador::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00ff50, transparent);
        opacity: 0.3;
    }
    .mini-indicador .valor {
        font-size: 2rem;
        font-weight: 700;
        color: #00ff50;
        text-shadow: 0 0 14px rgba(0,255,80,0.7);
        font-family: 'Share Tech Mono', monospace;
    }
    .mini-indicador .rotulo {
        font-size: 0.72rem;
        color: #3a7a52;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-family: 'Share Tech Mono', monospace;
    }

    /* ─── INDICATOR CARDS ────────────────────────────────────────── */
    .mini-cartao-indicador {
        border: 1px solid #0d4018;
        border-left: 3px solid #1a7a34;
        border-radius: 3px;
        padding: 10px 12px;
        margin-bottom: 10px;
        position: relative;
        background: #040d06;
    }
    .mini-cartao-baixo {
        border-left-color: #00ff50;
        background: linear-gradient(90deg, #040f07 0%, #040d06 100%);
    }
    .mini-cartao-medio {
        border-left-color: #ffb000;
        background: linear-gradient(90deg, #0f0d03 0%, #040d06 100%);
    }
    .mini-cartao-elevado {
        border-left-color: #ff3333;
        background: linear-gradient(90deg, #0f0303 0%, #040d06 100%);
    }
    .mini-cartao-titulo {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        color: #5aff8a;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
        text-transform: uppercase;
    }
    .mini-cartao-linha {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.88rem;
        color: #3a8a52;
        line-height: 1.5;
        font-weight: 600;
    }
    .mini-cartao-linha b { color: #8aff9a; }

    /* ─── RESULT BLOCK ────────────────────────────────────────────── */
    .resultado-critico {
        background: linear-gradient(180deg, #040d06 0%, #030c05 100%);
        border-radius: 4px;
        padding: 20px;
        border: 1px solid #0d4018;
        border-top: 3px solid #00ff50;
        box-shadow: 0 0 30px rgba(0,255,80,0.08), inset 0 0 40px rgba(0,0,0,0.3);
        margin-bottom: 16px;
        position: relative;
    }
    .resultado-titulo {
        font-size: 0.8rem;
        font-weight: 700;
        color: #00ff50;
        letter-spacing: 0.2em;
        margin-bottom: 3px;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 10px rgba(0,255,80,0.5);
    }
    .resultado-subtitulo {
        font-size: 0.8rem;
        color: #3a7a52;
        letter-spacing: 0.06em;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
    }
    .resultado-meta {
        background: rgba(0,255,80,0.03);
        border: 1px solid #0d4018;
        border-left: 2px solid #00ff50;
        border-radius: 3px;
        padding: 10px 12px;
        color: #5aff8a;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
        margin-bottom: 14px;
    }

    /* ─── RISK SEALS ─────────────────────────────────────────────── */
    .selo-risco {
        padding: 6px 14px;
        border-radius: 2px;
        font-weight: 700;
        font-size: 0.68rem;
        letter-spacing: 0.2em;
        white-space: nowrap;
        font-family: 'Share Tech Mono', monospace;
        text-align: center;
        text-transform: uppercase;
        border: 1px solid currentColor;
    }
    .selo-baixo {
        background: rgba(0,255,80,0.08);
        color: #00ff50;
        border-color: #00ff50;
        box-shadow: 0 0 10px rgba(0,255,80,0.25), inset 0 0 10px rgba(0,255,80,0.05);
    }
    .selo-medio {
        background: rgba(255,176,0,0.08);
        color: #ffb000;
        border-color: #ffb000;
        box-shadow: 0 0 10px rgba(255,176,0,0.25), inset 0 0 10px rgba(255,176,0,0.05);
    }
    .selo-elevado {
        background: rgba(255,51,51,0.08);
        color: #ff3333;
        border-color: #ff3333;
        box-shadow: 0 0 10px rgba(255,51,51,0.3), inset 0 0 10px rgba(255,51,51,0.05);
        animation: blink-red 1.8s infinite;
    }

    /* ─── ACTION BLOCK ───────────────────────────────────────────── */
    .acao-critica {
        border-radius: 3px;
        padding: 16px;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.22em;
        margin-top: 10px;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    .acao-critica::before {
        content: "";
        position: absolute;
        top: 0; left: -100%;
        width: 60%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
        animation: sweep 3s infinite;
    }
    .acao-baixa {
        background: rgba(0,255,80,0.06);
        color: #00ff50;
        border: 1px solid #00ff50;
        box-shadow: 0 0 20px rgba(0,255,80,0.15), inset 0 0 20px rgba(0,255,80,0.03);
    }
    .acao-media {
        background: rgba(255,176,0,0.06);
        color: #ffb000;
        border: 1px solid #ffb000;
        box-shadow: 0 0 20px rgba(255,176,0,0.15), inset 0 0 20px rgba(255,176,0,0.03);
    }
    .acao-elevada {
        background: rgba(255,51,51,0.06);
        color: #ff3333;
        border: 1px solid #ff3333;
        box-shadow: 0 0 20px rgba(255,51,51,0.2), inset 0 0 20px rgba(255,51,51,0.03);
        animation: blink-red 1.8s infinite;
    }

    /* ─── BLOCO META ─────────────────────────────────────────────── */
    .bloco-meta {
        background: rgba(0,255,80,0.03);
        border: 1px solid #0d4018;
        border-left: 2px solid #1a7a34;
        border-radius: 3px;
        padding: 10px 12px;
        margin-bottom: 12px;
        color: #5aff8a;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.06em;
    }

    /* ─── FACTOR CRITICAL BADGE ──────────────────────────────────── */
    .fator-critico {
        display: inline-block;
        background: transparent;
        color: #ff3333;
        border: 1px solid #ff3333;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 1px;
        margin-bottom: 5px;
        font-family: 'Share Tech Mono', monospace;
        letter-spacing: 0.15em;
        box-shadow: 0 0 6px rgba(255,51,51,0.3);
        animation: blink-red 2s infinite;
    }

    /* ─── DECISION STATE BADGES ─────────────────────────────────── */
    .estado-confirmacao {
        display: inline-block;
        background: rgba(0,255,80,0.08);
        color: #00ff50;
        border: 1px solid #00ff50;
        border-radius: 2px;
        padding: 3px 10px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-top: 6px;
        font-family: 'Share Tech Mono', monospace;
        letter-spacing: 0.12em;
        box-shadow: 0 0 8px rgba(0,255,80,0.2);
    }
    .estado-alteracao {
        display: inline-block;
        background: rgba(255,176,0,0.08);
        color: #ffb000;
        border: 1px solid #ffb000;
        border-radius: 2px;
        padding: 3px 10px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-top: 6px;
        font-family: 'Share Tech Mono', monospace;
        letter-spacing: 0.12em;
        box-shadow: 0 0 8px rgba(255,176,0,0.2);
    }

    /* ─── FORMULA BLOCK ──────────────────────────────────────────── */
    .formula-caso {
        background: #030c05;
        border: 1px dashed #0d4018;
        border-radius: 3px;
        padding: 12px;
        color: #5aff8a;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.78rem;
        margin-top: 10px;
        letter-spacing: 0.06em;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.3);
    }

    /* ─── AÇÃO FINAL ──────────────────────────────────────────────── */
    .acao-final {
        padding: 14px;
        border-radius: 3px;
        font-family: 'Share Tech Mono', monospace;
        font-weight: 700;
        text-align: center;
        margin-top: 12px;
        border: 1px solid #0d4018;
        font-size: 0.88rem;
        letter-spacing: 0.12em;
        color: #5aff8a;
        background: #040d06;
    }

    /* ─── SELECTBOXES ────────────────────────────────────────────── */
    div[data-baseweb="select"] > div {
        border-radius: 3px !important;
        min-height: 44px;
        font-weight: 600;
        font-family: 'Rajdhani', sans-serif !important;
        letter-spacing: 0.05em;
        background: #040d06 !important;
        border-color: #0d4018 !important;
        color: #5aff8a !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #1a7a34 !important;
        box-shadow: 0 0 8px rgba(0,255,80,0.15) !important;
    }
    div[data-baseweb="select"] svg { fill: #1a7a34 !important; }

    .risco-baixo div[data-baseweb="select"] > div {
        background: #030f05 !important;
        border-color: #00ff50 !important;
        color: #00ff50 !important;
        box-shadow: 0 0 8px rgba(0,255,80,0.15) !important;
    }
    .risco-medio div[data-baseweb="select"] > div {
        background: #0d0a02 !important;
        border-color: #ffb000 !important;
        color: #ffb000 !important;
        box-shadow: 0 0 8px rgba(255,176,0,0.15) !important;
    }
    .risco-elevado div[data-baseweb="select"] > div {
        background: #0d0202 !important;
        border-color: #ff3333 !important;
        color: #ff3333 !important;
        box-shadow: 0 0 8px rgba(255,51,51,0.2) !important;
    }
    .risco-neutro div[data-baseweb="select"] > div {
        background: #040d06 !important;
        border-color: #0d4018 !important;
        color: #3a7a52 !important;
    }

    /* ─── BUTTONS ────────────────────────────────────────────────── */
    div.stButton > button {
        background: transparent !important;
        color: #00ff50 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.8rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.18em !important;
        border: 1px solid #00ff50 !important;
        border-radius: 3px !important;
        padding: 0.6rem 1rem !important;
        box-shadow: 0 0 12px rgba(0,255,80,0.15), inset 0 0 12px rgba(0,255,80,0.03) !important;
        text-transform: uppercase !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: rgba(0,255,80,0.06) !important;
        box-shadow: 0 0 20px rgba(0,255,80,0.3), inset 0 0 20px rgba(0,255,80,0.06) !important;
        color: #00ff50 !important;
        border-color: #00ff50 !important;
    }
    div.stButton > button:focus {
        color: #00ff50 !important;
        border-color: #00ff50 !important;
        box-shadow: 0 0 20px rgba(0,255,80,0.3) !important;
    }

    /* ─── TEXT AREA ──────────────────────────────────────────────── */
    textarea {
        background: #030c05 !important;
        color: #5aff8a !important;
        border: 1px solid #0d4018 !important;
        border-radius: 3px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.95rem !important;
    }
    textarea:focus {
        border-color: #1a7a34 !important;
        box-shadow: 0 0 10px rgba(0,255,80,0.1) !important;
    }

    /* ─── LABELS ─────────────────────────────────────────────────── */
    label, .stSelectbox label, .stTextArea label {
        color: #3a8a52 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }

    /* ─── METRIC ─────────────────────────────────────────────────── */
    [data-testid="metric-container"] {
        background: #040d06 !important;
        border: 1px solid #0d4018 !important;
        border-top: 2px solid #1a7a34 !important;
        border-radius: 3px !important;
        padding: 12px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #3a7a52 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.68rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #00ff50 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1.3rem !important;
        text-shadow: 0 0 10px rgba(0,255,80,0.5) !important;
    }

    /* ─── ALERTS / INFO ──────────────────────────────────────────── */
    .stAlert {
        background: rgba(0,0,0,0.3) !important;
        border-radius: 3px !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    .stAlert[data-baseweb="notification"] {
        border-left: 3px solid #00ff50 !important;
        color: #5aff8a !important;
    }
    div[data-testid="stNotification"] {
        border: 1px solid #0d4018 !important;
        background: rgba(0,255,80,0.03) !important;
        color: #5aff8a !important;
    }
    div[data-testid="stNotification"] p {
        color: #5aff8a !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }
    .element-container div[data-testid="stNotification"] > div {
        color: #5aff8a !important;
    }

    /* ─── EXPANDER ───────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: #040d06 !important;
        color: #3a8a52 !important;
        border: 1px solid #0d4018 !important;
        border-radius: 3px !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.1em !important;
    }
    .streamlit-expanderContent {
        background: #030c05 !important;
        border: 1px solid #0a3012 !important;
        border-top: none !important;
        color: #5aff8a !important;
    }
    .streamlit-expanderContent p,
    .streamlit-expanderContent li,
    .streamlit-expanderContent strong {
        color: #5aff8a !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }

    /* ─── MARKDOWN / TEXT ────────────────────────────────────────── */
    .stMarkdown p, .stMarkdown li {
        color: #5aff8a !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }
    .stMarkdown h5 {
        color: #00ff50 !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 0.1em !important;
        font-size: 0.82rem !important;
        text-shadow: 0 0 8px rgba(0,255,80,0.4) !important;
    }
    .stMarkdown strong {
        color: #8aff9a !important;
    }
    h4, h5, h6 {
        font-family: 'Share Tech Mono', monospace !important;
        color: #00ff50 !important;
        letter-spacing: 0.1em !important;
    }

    /* ─── DOWNLOAD BUTTON ────────────────────────────────────────── */
    [data-testid="stDownloadButton"] button {
        background: transparent !important;
        color: #3aaa5a !important;
        border: 1px solid #1a7a34 !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.12em !important;
        border-radius: 3px !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: rgba(0,255,80,0.05) !important;
        color: #00ff50 !important;
        border-color: #00ff50 !important;
        box-shadow: 0 0 12px rgba(0,255,80,0.2) !important;
    }

    /* ─── SCROLLBAR ──────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #030c05; }
    ::-webkit-scrollbar-thumb { background: #1a7a34; border-radius: 2px; }
    ::-webkit-scrollbar-thumb:hover { background: #00ff50; }

    /* ─── SECTION DIVIDER ────────────────────────────────────────── */
    .nato-divider {
        border: none;
        border-top: 1px solid #0d4018;
        margin: 6px 0 14px 0;
    }

    /* ─── THREAT LEVEL BAR ───────────────────────────────────────── */
    .threat-bar {
        display: flex;
        gap: 4px;
        margin-bottom: 14px;
    }
    .threat-seg {
        flex: 1;
        height: 4px;
        border-radius: 1px;
    }
    .threat-seg-active-low   { background: #00ff50; box-shadow: 0 0 6px #00ff50; }
    .threat-seg-active-med   { background: #ffb000; box-shadow: 0 0 6px #ffb000; }
    .threat-seg-active-high  { background: #ff3333; box-shadow: 0 0 6px #ff3333; }
    .threat-seg-inactive     { background: #0d4018; }

    /* ─── KEYFRAMES ──────────────────────────────────────────────── */
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
    }
    @keyframes blink-red {
        0%, 100% { box-shadow: 0 0 10px rgba(255,51,51,0.3); }
        50% { box-shadow: 0 0 20px rgba(255,51,51,0.6); }
    }
    @keyframes sweep {
        0% { left: -100%; }
        100% { left: 200%; }
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
        return "DECISÃO REGISTADA"
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
        return "RECOMENDAÇÃO GERADA"
    return "EM ANÁLISE"

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
    linhas.append("NAVISGUARD // NATO RESTRICTED")
    linhas.append("REGISTO OPERACIONAL")
    linhas.append("=" * 50)
    linhas.append(f"ID DO CASO: {dados['id_caso']}")
    linhas.append(f"PROCESSADO EM: {dados['timestamp']}")
    linhas.append(f"POSIÇÃO/TRAJETÓRIA: {dados['posicao']}")
    linhas.append(f"VELOCIDADE/CURSO: {dados['velocidade']}")
    linhas.append(f"CONCORDÂNCIA COM RADAR/OUTRAS FONTES: {dados['radar']}")
    linhas.append(f"CONTEXTO OPERACIONAL: {dados['contexto']}")
    linhas.append("")
    linhas.append("INDICADORES:")
    for chave in ["I1", "I2", "I3", "I4", "I5", "I6"]:
        info = dados["contributos"][chave]
        linhas.append(
            f"  {chave} - {info['Nome']}: Estado={info['Nível']}, Pontos={info['Pontos']}, Peso={info['Peso']}, Contributo={info['Contributo']}"
        )
    linhas.append("")
    linhas.append(f"PONTUAÇÃO FINAL: {dados['pontuacao_total']}")
    linhas.append(f"NÍVEL DE RISCO: {dados['risco']}")
    linhas.append(f"AÇÃO PROPOSTA: {dados['acao']}")
    linhas.append(f"FÓRMULA APLICADA: {formula_caso_texto(dados['contributos'])}")
    if decisao is not None:
        linhas.append("")
        linhas.append("DECISÃO FINAL:")
        linhas.append(f"  ID DA DECISÃO: {decisao['id_decisao']}")
        linhas.append(f"  REGISTADO EM: {decisao['timestamp_decisao']}")
        linhas.append(f"  TIPO DE DECISÃO: {tipo_decisao(decisao['acao_proposta'], decisao['decisao_final'])}")
        linhas.append(f"  DECISÃO FINAL: {decisao['decisao_final']}")
        linhas.append(f"  JUSTIFICAÇÃO: {decisao['justificacao'] if decisao['justificacao'] else 'Não foi fornecida justificação.'}")
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
    "I2": "Alt. Identidade",
    "I3": "Cinemática",
    "I4": "Espaço-Tempo",
    "I5": "Contexto",
    "I6": "Entre Fontes"
}
pesos = {"I1": 3, "I2": 2, "I3": 2, "I4": 2, "I5": 1, "I6": 3}

# ─────────────────────────────────────────────
# CLASSIFICATION BANNER
# ─────────────────────────────────────────────
st.markdown("""
<div class="classification-banner">
    ⬛ NATO RESTRICTED // NAVISGUARD MARITIME DECISION SUPPORT SYSTEM // ACESSO CONTROLADO ⬛
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
ts_now = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
st.markdown(f"""
<div class="topo-dashboard">
    <div class="corner-tl"></div>
    <div class="corner-tr"></div>
    <div class="corner-bl"></div>
    <div class="corner-br"></div>
    <div class="header-grid">
        <div class="header-left">
            <div class="system-id">SYS // MARITIME TACTICAL COMMAND // v2.0</div>
            <h1>NAVISGUARD</h1>
            <div class="subtitle">Sistema de Apoio e Validação da Decisão em Ambiente Marítimo</div>
        </div>
        <div class="header-right">
            <span class="live-dot"></span>SISTEMA OPERACIONAL<br>
            SESSION: {datetime.now().strftime('%Y%m%d-%H%M')}<br>
            LOCAL: {ts_now}<br>
            PROTOCOLO: NATO STANAG<br>
            CLASSIFICAÇÃO: RESTRICTED
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STATUS BAR
# ─────────────────────────────────────────────
id_atual = st.session_state.dados_resultado["id_caso"] if st.session_state.dados_resultado else "N/A"
st.markdown(
    f"""
    <div class="barra-estado-caso">
        ▶ &nbsp;<b>CASO ATIVO:</b> {id_atual}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>ESTADO:</b> {estado_do_caso()}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <b>UTC:</b> {datetime.utcnow().strftime('%H:%M:%S Z')}
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("◈  ENQUADRAMENTO OPERACIONAL"):
    st.write("""
Este sistema constitui uma **plataforma de apoio à decisão em ambiente marítimo**, desenvolvida para avaliar comportamentos potencialmente anómalos de embarcações com base em dados operacionais.
A aplicação simula a análise de informação proveniente de sistemas como:
- AIS (Automatic Identification System)
- VMS (Vessel Monitoring System)
- Radar e outras fontes externas

Com base nos dados introduzidos pelo operador, o sistema:
1. **Gera indicadores internos de risco (I1–I6)**
2. **Calcula uma pontuação agregada**
3. **Classifica o nível de risco** (Baixo / Médio / Elevado)
4. **Propõe uma ação operacional** (Ignorar / Monitorizar / Escalar)
5. **Permite validação humana da decisão**

⚠️ **NOTA:** Esta aplicação é uma **demo conceptual** e não substitui sistemas reais de vigilância ou comando operacional.
""")

# ─────────────────────────────────────────────
# SECÇÃO 1 — PROCESSAMENTO
# ─────────────────────────────────────────────
st.markdown('<div class="cartao">', unsafe_allow_html=True)
st.markdown('<div class="titulo-secao">◈ 01 // PROCESSAMENTO OPERACIONAL</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo-secao">O sistema calcula indicadores, avalia o risco e emite uma recomendação.</div>', unsafe_allow_html=True)

st.info("BRIEFING: Após clicar em 'GERAR RECOMENDAÇÃO', o sistema processa os indicadores, calcula a pontuação total, determina o nível de risco e emite a ação proposta.")

mini1, mini2, mini3 = st.columns(3)
with mini1:
    st.markdown("""
    <div class="mini-indicador" style="border-top-color:#1a7aaa;">
        <div class="valor" style="color:#5ab4ff; text-shadow:0 0 14px rgba(90,180,255,0.7);">6</div>
        <div class="rotulo">Indicadores Internos</div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("Ver indicadores"):
        st.markdown("""
        **I1 — Identidade** *(Posição/Trajetória)*
        **I2 — Alt. Identidade** *(Posição + Radar)*
        **I3 — Cinemática** *(Velocidade/Curso)*
        **I4 — Espaço-Temporal** *(Posição + Velocidade)*
        **I5 — Contexto** *(Contexto Operacional)*
        **I6 — Entre Fontes** *(Concordância Radar)*
        """)
with mini2:
    st.markdown("""
    <div class="mini-indicador">
        <div class="valor">3</div>
        <div class="rotulo">Níveis de Risco</div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("Ver níveis"):
        st.markdown("""
        **BAIXO** — Sem impacto
        **MÉDIO** — Atenção requerida
        **ELEVADO** — Prioridade máxima
        """)
with mini3:
    st.markdown("""
    <div class="mini-indicador">
        <div class="valor">4</div>
        <div class="rotulo">Ações Possíveis</div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("Ver ações"):
        st.markdown("""
        **IGNORAR** — Sem ação
        **MONITORIZAR** — Vigilância ativa
        **ESCALAR** — Intervenção imediata
        **REVER** — Análise adicional
        """)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
coluna_esquerda, coluna_direita = st.columns([1, 1], gap="large")

# ─────────────────────────────────────────────
# SECÇÃO 2 — DADOS DE ENTRADA
# ─────────────────────────────────────────────
with coluna_esquerda:
    st.markdown('<div class="cartao cartao-azul">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">◈ 02 // DADOS DE ENTRADA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Operador: introduzir dados do caso em análise.</div>', unsafe_allow_html=True)

    col_titulo_entrada, col_botao_reset = st.columns([3, 1])
    with col_titulo_entrada:
        st.markdown('<div class="etiqueta">▸ PREPARAÇÃO DO CASO</div>', unsafe_allow_html=True)
    with col_botao_reset:
        st.button("NOVO CASO", use_container_width=True, on_click=reiniciar_caso)

    st.markdown('<div class="etiqueta">▸ DADOS AIS / VMS</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="etiqueta">Posição / Trajetória</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(posicao) if "posicao" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        posicao = st.selectbox(
            "Posição/Trajetória",
            ["Normal", "Ligeiramente suspeita", "Muito suspeita"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="etiqueta">Velocidade / Curso</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(velocidade) if "velocidade" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        velocidade = st.selectbox(
            "Velocidade/Curso",
            ["Normal", "Ligeiramente suspeito", "Muito suspeito"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="etiqueta">▸ OUTRAS FONTES</div>', unsafe_allow_html=True)
    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="etiqueta">Concordância Radar</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(radar) if "radar" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        radar = st.selectbox(
            "Concordância com radar/outras fontes",
            ["Concordante", "Parcialmente discordante", "Discordante"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with col_f:
        st.markdown('<div class="etiqueta">Contexto Operacional</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="{classe_risco_input(contexto) if "contexto" in locals() else "risco-neutro"}">', unsafe_allow_html=True)
        contexto = st.selectbox(
            "Contexto operacional",
            ["Normal", "Pouco habitual", "Muito suspeito"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    gerar = st.button("◈  GERAR RECOMENDAÇÃO", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Deteção de alterações
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
# SECÇÕES 3 + 4 — COLUNA DIREITA
# ─────────────────────────────────────────────
with coluna_direita:
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not resultado_em_reserva:
        dados = st.session_state.dados_resultado
        contributos = dados["contributos"]
        pontuacao_total = dados["pontuacao_total"]
        risco = dados["risco"]
        acao = dados["acao"]
        fatores_principais = obter_fatores_principais(contributos, top_n=3)

        # Threat level bar
        segs = []
        if risco == "Baixo":
            segs = ["threat-seg-active-low", "threat-seg-inactive", "threat-seg-inactive", "threat-seg-inactive", "threat-seg-inactive"]
        elif risco == "Médio":
            segs = ["threat-seg-active-low", "threat-seg-active-med", "threat-seg-active-med", "threat-seg-inactive", "threat-seg-inactive"]
        else:
            segs = ["threat-seg-active-low", "threat-seg-active-med", "threat-seg-active-high", "threat-seg-active-high", "threat-seg-active-high"]
        seg_html = "".join([f'<div class="threat-seg {s}"></div>' for s in segs])
        st.markdown(f'<div class="threat-bar">{seg_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">◈ 03 // AVALIAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Síntese dos fatores críticos e impacto na recomendação.</div>', unsafe_allow_html=True)

        st.info("▸ BRIEFING OPERACIONAL — Avaliação concluída")
        st.markdown("**ESTADO:** Avaliação concluída")
        st.markdown("**FATORES CRÍTICOS:**")
        for idx, fator in enumerate(fatores_principais):
            prefixo = "  ►  "
            if idx == 0:
                prefixo = "  ◉  PRINCIPAL: "
            st.write(f"{prefixo}{fator['nome']}")

        st.markdown('<div class="etiqueta">▸ AVALIAÇÃO DE RISCO</div>', unsafe_allow_html=True)
        st.write(f"**NÍVEL DE RISCO:** {risco.upper()}")
        st.write(f"**AÇÃO PROPOSTA:** {acao.upper()}")
        st.markdown(
            f"**AVALIAÇÃO:** Situação classificada com risco **{risco.upper()}** pela combinação dos fatores críticos identificados."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # SECÇÃO 4 — PROPOSTA DE AÇÃO
        st.markdown('<div class="resultado-critico">', unsafe_allow_html=True)
        col_res_1, col_res_2 = st.columns([3, 1])
        with col_res_1:
            st.markdown('<div class="resultado-titulo">◈ 04 // PROPOSTA DE AÇÃO</div>', unsafe_allow_html=True)
            st.markdown('<div class="resultado-subtitulo">Recomendação gerada a partir das entradas submetidas.</div>', unsafe_allow_html=True)
        with col_res_2:
            st.markdown(
                f'<div class="selo-risco {classe_selo_risco(risco)}" style="text-align:center; margin-top:6px;">RISCO {risco.upper()}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="resultado-meta">▸ ID CASO: {dados["id_caso"]}<br>▸ TIMESTAMP: {dados["timestamp"]}</div>',
            unsafe_allow_html=True
        )
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Pontuação Total", pontuacao_total)
        with m2:
            st.metric("Nível de Risco", risco)
        with m3:
            st.metric("Ação Proposta", acao)

        st.markdown(
            f'<div class="acao-critica {classe_acao_resultado(risco)}">▸ AÇÃO RECOMENDADA: {acao.upper()}</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.resultado_gerado and resultado_em_reserva:
        st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">◈ 03 // AVALIAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Informação em reserva.</div>', unsafe_allow_html=True)
        st.warning("⚠ ALERTA: Entradas alteradas. Gere nova recomendação para atualizar a avaliação tática.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">◈ 04 // PROPOSTA DE AÇÃO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Resultado anterior invalidado.</div>', unsafe_allow_html=True)
        st.warning("⚠ RESULTADO SUSPENSO: Configuração alterada. Regenerar antes de nova validação.")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">◈ 03 // AVALIAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Aguardando processamento.</div>', unsafe_allow_html=True)
        st.info("◌  STANDBY — A avaliação tática será apresentada após a geração da recomendação.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="cartao">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">◈ 04 // PROPOSTA DE AÇÃO</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Aguardando processamento operacional.</div>', unsafe_allow_html=True)
        st.info("◌  STANDBY — Introduza os dados do caso e clique em 'GERAR RECOMENDAÇÃO'.")
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

    st.markdown('<div class="cartao cartao-azul">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">◈ 05 // CONFIRMAÇÃO DO OPERADOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">O operador pode confirmar ou alterar a recomendação automática.</div>', unsafe_allow_html=True)

    decisao_utilizador = st.selectbox(
        "Decisão final do operador",
        ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"],
        label_visibility="visible"
    )
    justificacao = st.text_area(
        "Justificação operacional",
        placeholder="Descreve o motivo pelo qual confirmas ou alteras a ação proposta...",
        height=150
    )
    alterou_decisao = decisao_utilizador != "Confirmar ação proposta"
    if alterou_decisao:
        st.warning("⚠ PROTOCOLO: A justificação é obrigatória quando a decisão altera a ação proposta pelo sistema.")

    guardar = st.button("◈  REGISTAR DECISÃO FINAL", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if guardar:
        decisao_final = acao if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador
        if alterou_decisao and not justificacao.strip():
            st.error("ERRO DE PROTOCOLO: A justificação é obrigatória quando alteras a ação proposta.")
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

    # ─────────────────────────────────────────────
    # SECÇÃO 6 — DECISÃO FINAL
    # ─────────────────────────────────────────────
    if st.session_state.decisao_guardada is not None:
        reg = st.session_state.decisao_guardada
        tipo = tipo_decisao(reg["acao_proposta"], reg["decisao_final"])
        classe_tipo = "estado-confirmacao" if tipo == "Confirmada" else "estado-alteracao"

        st.markdown('<div class="cartao cartao-verde">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">◈ 06 // DECISÃO FINAL</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">Registo final da decisão humana apoiada pelo sistema.</div>', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="bloco-meta">
                ▸ ID DECISÃO: {reg["id_decisao"]}<br>
                ▸ REGISTADO EM: {reg["timestamp_decisao"]}<br>
                ▸ TIPO: {tipo}<br>
                <span class="{classe_tipo}">{tipo.upper()}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Ação Proposta", reg["acao_proposta"])
        with r2:
            st.metric("Decisão Final", reg["decisao_final"])
        with r3:
            st.metric("Nível de Risco", reg["risco"])
        with r4:
            st.metric("Pontuação", reg["pontuacao_total"])

        st.markdown('<div class="etiqueta">▸ JUSTIFICAÇÃO OPERACIONAL</div>', unsafe_allow_html=True)
        if reg["justificacao"]:
            st.write(reg["justificacao"])
        else:
            st.write("Sem justificação registada.")

        st.success("◉  DECISÃO FINAL REGISTADA COM SUCESSO NO SISTEMA NAVISGUARD.")

        if st.session_state.dados_resultado is not None:
            conteudo_txt = exportar_registo_txt(st.session_state.dados_resultado, reg)
            st.download_button(
                label="◈  EXPORTAR REGISTO OPERACIONAL (TXT)",
                data=conteudo_txt,
                file_name=f"{st.session_state.dados_resultado['id_caso']}_{reg['id_decisao']}.txt",
                mime="text/plain",
                use_container_width=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # ─────────────────────────────────────────────
    # SECÇÃO 7 — QUADRO DE INDICADORES
    # ─────────────────────────────────────────────
    st.markdown('<div class="cartao">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">◈ 07 // QUADRO DE INDICADORES</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Estado, peso e impacto na decisão de cada indicador de risco.</div>', unsafe_allow_html=True)

    fatores_top = {f["codigo"] for f in obter_fatores_principais(contributos, top_n=3)}

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
        destaque_a = '<div class="fator-critico">◉ FATOR CRÍTICO</div>' if codigo_a in fatores_top else ""
        with col_a:
            html_a = f"""<div class="mini-cartao-indicador {classe_a}">
{destaque_a}
<div class="mini-cartao-titulo">{codigo_a} // {siglas_indicadores[codigo_a]}</div>
<div class="mini-cartao-linha">Estado: <b>{info_a['Nível'].upper()}</b></div>
<div class="mini-cartao-linha">Pontos: <b>{info_a['Pontos']}</b> &nbsp;|&nbsp; Peso: <b>{info_a['Peso']}</b></div>
<div class="mini-cartao-linha">Contributo: <b>{info_a['Contributo']}</b></div>
<div class="mini-cartao-linha">Impacto: <b>{impacto_textual(info_a['Contributo']).upper()}</b></div>
</div>"""
            st.markdown(html_a, unsafe_allow_html=True)

        codigo_b, info_b = pares[i + 1]
        classe_b = classe_cartao_indicador(info_b["Contributo"])
        destaque_b = '<div class="fator-critico">◉ FATOR CRÍTICO</div>' if codigo_b in fatores_top else ""
        with col_b:
            html_b = f"""<div class="mini-cartao-indicador {classe_b}">
{destaque_b}
<div class="mini-cartao-titulo">{codigo_b} // {siglas_indicadores[codigo_b]}</div>
<div class="mini-cartao-linha">Estado: <b>{info_b['Nível'].upper()}</b></div>
<div class="mini-cartao-linha">Pontos: <b>{info_b['Pontos']}</b> &nbsp;|&nbsp; Peso: <b>{info_b['Peso']}</b></div>
<div class="mini-cartao-linha">Contributo: <b>{info_b['Contributo']}</b></div>
<div class="mini-cartao-linha">Impacto: <b>{impacto_textual(info_b['Contributo']).upper()}</b></div>
</div>"""
            st.markdown(html_b, unsafe_allow_html=True)

    with st.expander("◈  VER REGRA DE CÁLCULO"):
        st.markdown(f"""
        **ORIGEM DOS INDICADORES**
        - **I1** → Posição/Trajetória
        - **I2** → Posição + Concordância Radar
        - **I3** → Velocidade/Curso
        - **I4** → Posição + Velocidade
        - **I5** → Contexto Operacional
        - **I6** → Concordância Radar/Fontes

        **ESTADOS**  Baixo=0 | Médio=1 | Elevado=2

        **PESOS**  I1=3 | I2=2 | I3=2 | I4=2 | I5=1 | I6=3

        **FÓRMULA:** Pontuação = Σ (pontosᵢ × pesoᵢ)

        **FÓRMULA APLICADA:**
        """, unsafe_allow_html=True)
        st.markdown(
            f'<div class="formula-caso">▸ {formula_caso_texto(contributos)}</div>',
            unsafe_allow_html=True
        )
        st.markdown("""
        **CONVERSÃO**
        - ≤ 4 pts → **BAIXO** → Ignorar
        - ≤ 8 pts → **MÉDIO** → Monitorizar
        - > 8 pts → **ELEVADO** → Escalar
        """)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.resultado_gerado and resultado_em_reserva:
    st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">◈ INFORMAÇÃO EM RESERVA</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-secao">Caso alterado após a última geração.</div>', unsafe_allow_html=True)
    st.warning("⚠ ALERTA: Entradas alteradas. Regenerar antes de nova validação.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER CLASSIFICATION
# ─────────────────────────────────────────────
st.markdown("""
<div class="classification-banner" style="margin-top:20px;">
    ⬛ NATO RESTRICTED // NAVISGUARD MARITIME DECISION SUPPORT SYSTEM // ACESSO CONTROLADO ⬛
</div>
""", unsafe_allow_html=True)
