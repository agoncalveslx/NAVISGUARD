import streamlit as st


def aplicar_estilos():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
        }

        .topo-dashboard {
            background: linear-gradient(90deg, #0f172a 0%, #1d4ed8 100%);
            padding: 12px 18px;
            border-radius: 12px;
            color: white;
            margin-bottom: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.10);
        }

        .topo-dashboard h1 {
            margin: 0;
            font-size: 1.3rem;
            line-height: 1.1;
        }

        .topo-dashboard p {
            margin-top: 4px;
            margin-bottom: 0;
            font-size: 0.86rem;
            color: #eef4ff;
        }

        .cartao {
            background: white;
            padding: 16px 18px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
            border: 1px solid #e5e7eb;
            margin-bottom: 16px;
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
            font-size: 1.2rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 2px;
        }

        .subtitulo-secao {
            font-size: 0.9rem;
            color: #475569;
            margin-bottom: 10px;
        }

        .etiqueta {
            font-weight: 700;
            color: #0f172a;
            margin-top: 8px;
            margin-bottom: 4px;
        }

        .acao-final {
            padding: 14px;
            border-radius: 10px;
            font-weight: 800;
            text-align: center;
            margin-top: 10px;
            border: 1px solid #d1d5db;
            font-size: 1rem;
        }

        .mini-indicador {
            background: white;
            border: 1px solid #d7dde5;
            border-radius: 8px;
            padding: 10px 12px;
            text-align: center;
            box-shadow: none;
        }

        .mini-indicador .valor {
            font-size: 1.5rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.1;
        }

        .mini-indicador .rotulo {
            font-size: 0.82rem;
            color: #475569;
            font-weight: 600;
            margin-top: 2px;
        }

        .mini-cartao-indicador {
            border: 1px solid #d7dde5;
            border-radius: 8px;
            padding: 10px 12px;
            margin-bottom: 8px;
            position: relative;
            box-shadow: none;
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
            margin-bottom: 5px;
            font-size: 0.92rem;
        }

        .mini-cartao-linha {
            font-size: 0.88rem;
            color: #334155;
            line-height: 1.35;
        }

        .bloco-meta {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 10px 12px;
            margin-bottom: 10px;
            color: #334155;
            font-size: 0.9rem;
        }

        .barra-estado-caso {
            background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
            color: white;
            border-radius: 10px;
            padding: 10px 14px;
            margin-bottom: 14px;
            border: 1px solid #334155;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.14);
        }

        .resultado-critico {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
            color: white;
            border-radius: 12px;
            padding: 18px;
            border: 1px solid #1f2937;
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.18);
            margin-bottom: 16px;
        }

        .resultado-titulo {
            font-size: 1.18rem;
            font-weight: 800;
            color: white;
            margin-bottom: 4px;
        }

        .resultado-subtitulo {
            font-size: 0.9rem;
            color: #e5e7eb;
        }

        .selo-risco {
            padding: 7px 11px;
            border-radius: 999px;
            font-weight: 800;
            font-size: 0.78rem;
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
            border-radius: 8px;
            padding: 10px 12px;
            color: white;
            font-size: 0.88rem;
            margin-bottom: 12px;
        }

        .acao-critica {
            border-radius: 10px;
            padding: 14px;
            text-align: center;
            font-weight: 800;
            font-size: 1.02rem;
            border: 1px solid rgba(255,255,255,0.10);
            margin-top: 8px;
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
            font-size: 0.7rem;
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
            font-size: 0.76rem;
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
            font-size: 0.76rem;
            font-weight: 700;
            margin-top: 6px;
        }

        .formula-caso {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 8px;
            padding: 10px 12px;
            color: #334155;
            font-size: 0.9rem;
            margin-top: 8px;
        }

        div.stButton > button {
            background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
            color: white;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 0.58rem 0.95rem;
            box-shadow: 0 3px 8px rgba(37, 99, 235, 0.20);
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
            color: white;
            border: none;
        }

        div.stButton > button:focus {
            color: white !important;
            border: none !important;
            box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.22);
        }

        div[data-baseweb="select"] > div {
            border-radius: 8px !important;
            min-height: 42px;
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

        /* Afinar st.metric */
        div[data-testid="stMetric"] {
            background: #f8fafc;
            border: 1px solid #dbe2ea;
            border-radius: 8px;
            padding: 10px 12px;
            box-shadow: none;
        }

        div[data-testid="stMetricLabel"] {
            color: #475569;
            font-weight: 700;
            font-size: 0.82rem;
        }

        div[data-testid="stMetricValue"] {
            color: #0f172a;
            font-weight: 800;
            font-size: 1.45rem;
            line-height: 1.1;
        }

        div[data-testid="stMetricDelta"] {
            font-size: 0.78rem;
        }

        /* Afinar expander */
        div[data-testid="stExpander"] {
            border: 1px solid #dbe2ea;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: none;
        }

        div[data-testid="stExpander"] details {
            border-radius: 8px;
        }

        div[data-testid="stExpander"] summary {
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
            font-weight: 700;
            color: #0f172a;
        }

        /* Afinar dataframe */
        div[data-testid="stDataFrame"] {
            border: 1px solid #dbe2ea;
            border-radius: 8px;
            overflow: hidden;
        }

        div[data-testid="stDataFrame"] [role="columnheader"] {
            background: #e2e8f0 !important;
            color: #0f172a !important;
            font-weight: 800 !important;
            border-bottom: 1px solid #cbd5e1 !important;
        }

        div[data-testid="stDataFrame"] [role="gridcell"] {
            font-size: 0.88rem;
            color: #334155;
        }

        /* Faixa de estado do quadro */
        .faixa-estado {
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 12px;
            border: 1px solid;
            font-weight: 800;
            font-size: 0.95rem;
            letter-spacing: 0.02em;
        }

        .faixa-estado-linha-secundaria {
            margin-top: 4px;
            font-size: 0.84rem;
            font-weight: 600;
            letter-spacing: 0;
        }

        .faixa-vermelha {
            background: #7f1d1d;
            color: #fee2e2;
            border-color: #991b1b;
        }

        .faixa-amarela {
            background: #78350f;
            color: #fef3c7;
            border-color: #92400e;
        }

        .faixa-verde {
            background: #14532d;
            color: #dcfce7;
            border-color: #166534;
        }
    </style>
    """, unsafe_allow_html=True)
