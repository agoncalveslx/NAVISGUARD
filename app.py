import streamlit as st
import pandas as pd
from datetime import datetime
import random
import pydeck as pdk


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

if "historico_casos" not in st.session_state:
    st.session_state.historico_casos = []

# Valores dos inputs
if "posicao" not in st.session_state:
    st.session_state.posicao = "Normal"

if "velocidade" not in st.session_state:
    st.session_state.velocidade = "Normal"

if "radar" not in st.session_state:
    st.session_state.radar = "Concordante"

if "contexto" not in st.session_state:
    st.session_state.contexto = "Normal"

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
        color: #ffffff;
        margin-bottom: 4px;
    }

    .resultado-subtitulo {
        font-size: 0.93rem;
        color: #cbd5e1;
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
        color: #e5e7eb;
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
    st.session_state.posicao = "Normal"
    st.session_state.velocidade = "Normal"
    st.session_state.radar = "Concordante"
    st.session_state.contexto = "Normal"

def gerar_caso_aleatorio():
    st.session_state.resultado_gerado = False
    st.session_state.dados_resultado = None
    st.session_state.decisao_guardada = None
    st.session_state.posicao = random.choice(["Normal", "Ligeiramente suspeita", "Muito suspeita"])
    st.session_state.velocidade = random.choice(["Normal", "Ligeiramente suspeito", "Muito suspeito"])
    st.session_state.radar = random.choice(["Concordante", "Parcialmente discordante", "Discordante"])
    st.session_state.contexto = random.choice(["Normal", "Pouco habitual", "Muito suspeito"])

def estado_do_caso():
    if st.session_state.decisao_guardada is not None:
        return "Decisão registada"
    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None:
        return "Recomendação gerada"
    return "Em análise"

def tipo_decisao(acao_proposta_atual, decisao_final):
    if acao_proposta_atual == decisao_final:
        return "Confirmada"
    return "Alterada pelo Especialista"

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

    return "\\n".join(linhas)

def contar_escalados(historico):
    return sum(1 for caso in historico if caso["acao"] == "Escalar")

def obter_resumo_risco(historico):
    contagem = {"Baixo": 0, "Médio": 0, "Elevado": 0}
    for caso in historico:
        risco = caso["risco"]
        if risco in contagem:
            contagem[risco] += 1
    return contagem

def contar_confirmacoes(historico):
    return sum(
        1 for caso in historico
        if caso.get("tipo_decisao") == "Confirmada"
    )

def contar_alteracoes(historico):
    return sum(
        1 for caso in historico
        if caso.get("tipo_decisao") == "Alterada pelo Especialista"
    )

def total_casos_validados(historico):
    return len(historico)

# -------------------------
# Funções do mapa tático
# -------------------------
def obter_coordenadas_caso(posicao, contexto):
    if contexto == "Muito suspeito":
        if posicao == "Muito suspeita":
            return 37.20, -10.20, "Sul / Algarve Ocidental", "Contacto em área marítima sensível"
        elif posicao == "Ligeiramente suspeita":
            return 38.45, -10.10, "Oeste de Lisboa / Setúbal", "Aproximação a corredor marítimo"
        return 41.15, -9.95, "Noroeste / Norte", "Contacto em aproximação marítima"

    if contexto == "Pouco habitual":
        if posicao == "Muito suspeita":
            return 39.70, -10.35, "Oeste / Centro", "Trajetória pouco habitual em mar aberto"
        elif posicao == "Ligeiramente suspeita":
            return 38.05, -9.95, "Sines / Sudoeste", "Movimento sob observação"
        return 40.50, -9.95, "Figueira da Foz / Oeste", "Tráfego sob observação"

    if posicao == "Muito suspeita":
        return 41.35, -10.05, "Alto Mar / Norte", "Contacto na envolvente marítima"
    elif posicao == "Ligeiramente suspeita":
        return 38.90, -9.95, "Costa Central", "Contacto sob monitorização"
    return 39.45, -9.75, "Costa Portuguesa", "Tráfego regular em espaço marítimo português"

def classe_zona_maritima(zona):
    zona_lower = zona.lower()
    if "norte" in zona_lower:
        return "Zona Norte"
    elif "centro" in zona_lower or "lisboa" in zona_lower or "setúbal" in zona_lower or "sines" in zona_lower or "figueira" in zona_lower:
        return "Zona Centro"
    return "Zona Sul"

def desenhar_bloco_zona_maritima(zona, observacao):
    zona_operacional = classe_zona_maritima(zona)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
            color: white;
            border: 1px solid #334155;
            border-radius: 14px;
            padding: 12px 14px;
            margin-bottom: 12px;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.18);
        ">
            <div style="font-size: 0.82rem; color: #93c5fd; font-weight: 700; letter-spacing: 0.04em;">
                ENQUADRAMENTO MARÍTIMO
            </div>
            <div style="font-size: 1.05rem; font-weight: 800; margin-top: 2px;">
                {zona_operacional} — {zona}
            </div>
            <div style="font-size: 0.9rem; color: #cbd5e1; margin-top: 4px;">
                {observacao}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def cor_risco_mapa(risco):
    if risco == "Baixo":
        return [34, 197, 94, 255]
    elif risco == "Médio":
        return [245, 158, 11, 255]
    return [220, 38, 38, 255]

def raio_risco(risco):
    if risco == "Baixo":
        return 14000
    elif risco == "Médio":
        return 24000
    return 34000

def gerar_trajetoria(lat, lon, velocidade, posicao):
    if velocidade == "Muito suspeito":
        desloc_lon = 1.10
        desloc_lat = 0.18
    elif velocidade == "Ligeiramente suspeito":
        desloc_lon = 0.80
        desloc_lat = 0.12
    else:
        desloc_lon = 0.45
        desloc_lat = 0.08

    if posicao == "Muito suspeita":
        desloc_lat *= 1.15

    return [
        [lon - desloc_lon, lat + desloc_lat],
        [lon - desloc_lon * 0.66, lat + desloc_lat * 0.45],
        [lon - desloc_lon * 0.33, lat + desloc_lat * 0.15],
        [lon, lat]
    ]

def obter_contactos_referencia():
    return pd.DataFrame([
        {"lat": 41.05, "lon": -9.85, "tipo": "Tráfego regular"},
        {"lat": 39.95, "lon": -10.05, "tipo": "Tráfego regular"},
        {"lat": 38.55, "lon": -9.95, "tipo": "Tráfego regular"},
        {"lat": 37.45, "lon": -9.45, "tipo": "Tráfego regular"},
    ])

def desenhar_legenda_tatica():
    st.markdown(
        """
        <div style="display:flex; gap:18px; flex-wrap:wrap; margin-top:8px; margin-bottom:6px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:14px; height:14px; border-radius:50%; background:#22c55e;"></div>
                <span style="font-size:0.9rem; color:#334155;"><b>Baixo</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:14px; height:14px; border-radius:50%; background:#f59e0b;"></div>
                <span style="font-size:0.9rem; color:#334155;"><b>Médio</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:14px; height:14px; border-radius:50%; background:#ef4444;"></div>
                <span style="font-size:0.9rem; color:#334155;"><b>Elevado</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:18px; height:3px; background:#60a5fa;"></div>
                <span style="font-size:0.9rem; color:#334155;"><b>Trajetória estimada</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <div style="width:18px; height:12px; background:#334155; border:1px solid #94a3b8;"></div>
                <span style="font-size:0.9rem; color:#334155;"><b>Costa continental</b></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def desenhar_mapa_tatico(posicao, velocidade, contexto, risco):
    lat, lon, zona, observacao = obter_coordenadas_caso(posicao, contexto)
    cor = cor_risco_mapa(risco)
    trajetoria = gerar_trajetoria(lat, lon, velocidade, posicao)
    raio = raio_risco(risco)

    desenhar_bloco_zona_maritima(zona, observacao)

    df_contacto = pd.DataFrame([{
        "lat": lat,
        "lon": lon,
        "zona": zona,
        "risco": risco,
        "observacao": observacao
    }])

    df_trajetoria = pd.DataFrame([{
        "path": trajetoria,
        "nome": "Trajetória estimada"
    }])

    df_referencia = obter_contactos_referencia()

    layer_trajetoria = pdk.Layer(
        "PathLayer",
        data=df_trajetoria,
        get_path="path",
        get_color=[59, 130, 246, 220],
        width_scale=20,
        width_min_pixels=3,
        get_width=5 if velocidade == "Muito suspeito" else 4 if velocidade == "Ligeiramente suspeito" else 3,
        pickable=False
    )

    layer_contactos_ref = pdk.Layer(
        "ScatterplotLayer",
        data=df_referencia,
        get_position="[lon, lat]",
        get_fill_color=[120, 140, 160, 70],
        get_radius=3000,
        pickable=False
    )

    layer_anel_risco = pdk.Layer(
        "ScatterplotLayer",
        data=df_contacto,
        get_position="[lon, lat]",
        get_fill_color=[0, 0, 0, 0],
        get_line_color=cor,
        line_width_min_pixels=4,
        stroked=True,
        filled=False,
        get_radius=raio,
        pickable=False
    )

    layer_anel_secundario = pdk.Layer(
        "ScatterplotLayer",
        data=df_contacto,
        get_position="[lon, lat]",
        get_fill_color=[0, 0, 0, 0],
        get_line_color=[cor[0], cor[1], cor[2], 80],
        line_width_min_pixels=1,
        stroked=True,
        filled=False,
        get_radius=raio + 8000,
        pickable=False
    )

    layer_contacto_principal = pdk.Layer(
        "ScatterplotLayer",
        data=df_contacto,
        get_position="[lon, lat]",
        get_fill_color=cor,
        get_line_color=[255, 255, 255, 255],
        line_width_min_pixels=3,
        stroked=True,
        filled=True,
        get_radius=14000,
        pickable=True
    )

    layer_centro = pdk.Layer(
        "TextLayer",
        data=pd.DataFrame([{
            "lat": lat,
            "lon": lon,
            "texto": "▲"
        }]),
        get_position="[lon, lat]",
        get_text="texto",
        get_size=18,
        get_color=[255, 255, 255, 240],
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'"
    )

    view_state = pdk.ViewState(
        latitude=39.30,
        longitude=-9.20,
        zoom=6.0,
        pitch=0
    )

    deck = pdk.Deck(
        map_provider="carto",
        map_style="light",
        initial_view_state=view_state,
        layers=[
            layer_trajetoria,
            layer_contactos_ref,
            layer_anel_secundario,
            layer_anel_risco,
            layer_contacto_principal,
            layer_centro
        ],
        tooltip={
            "html": """
                <b>Zona:</b> {zona}<br/>
                <b>Risco:</b> {risco}<br/>
                <b>Observação:</b> {observacao}
            """,
            "style": {
                "backgroundColor": "#0f172a",
                "color": "white",
                "fontSize": "12px",
                "border": "1px solid #334155"
            }
        }
    )

    st.pydeck_chart(deck, use_container_width=True)
    desenhar_legenda_tatica()

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
st.markdown('<div class="topo-dashboard" style="padding:10px;">', unsafe_allow_html=True)
st.image("logo.jpg", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

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

Com base nos dados introduzidos pelo Especialista, o sistema:

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
   O Especialista pode confirmar ou ajustar a recomendação, garantindo controlo humano no processo.

⚠️ **Nota:**  
Esta aplicação é uma **demo conceptual**, desenvolvida para ilustrar a lógica de um sistema de apoio à decisão em contexto marítimo, não substituindo sistemas reais de vigilância ou comando operacional.
""")

# -------------------------
# Dashboard de risco
# -------------------------
st.markdown('<div class="cartao">', unsafe_allow_html=True)
st.markdown('<div class="titulo-secao">DASHBOARD DE RISCO</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo-secao">Síntese estatística dos casos processados pelo sistema.</div>', unsafe_allow_html=True)

if len(st.session_state.historico_casos) == 0:
    st.info("Ainda não existem casos registados para análise estatística.")
else:
    historico_df = pd.DataFrame(st.session_state.historico_casos)
    resumo_risco = obter_resumo_risco(st.session_state.historico_casos)
    total_casos = len(st.session_state.historico_casos)
    total_escalados = contar_escalados(st.session_state.historico_casos)
    total_confirmacoes = contar_confirmacoes(st.session_state.historico_casos)
    total_alteracoes = contar_alteracoes(st.session_state.histor
