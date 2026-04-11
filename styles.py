import streamlit as st


def aplicar_estilos():
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
            color: white;
            margin-bottom: 4px;
        }

        .resultado-subtitulo {
            font-size: 0.93rem;
            color: #e5e7eb;
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
            color: white;
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
