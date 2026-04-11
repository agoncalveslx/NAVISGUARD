import streamlit as st
import pandas as pd
import pydeck as pdk


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
