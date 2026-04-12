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
        return "SETOR NORTE"
    elif "centro" in zona_lower or "lisboa" in zona_lower or "setúbal" in zona_lower or "sines" in zona_lower or "figueira" in zona_lower:
        return "SETOR CENTRO"
    return "SETOR SUL"


def desenhar_bloco_zona_maritima(zona, observacao):
    zona_operacional = classe_zona_maritima(zona)
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
            color: white;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 10px 12px;
            margin-bottom: 10px;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.14);
        ">
            <div style="font-size: 0.76rem; color: #93c5fd; font-weight: 800; letter-spacing: 0.05em;">
                ENQUADRAMENTO MARÍTIMO
            </div>
            <div style="font-size: 1rem; font-weight: 800; margin-top: 2px;">
                {zona_operacional} | {zona}
            </div>
            <div style="font-size: 0.84rem; color: #cbd5e1; margin-top: 3px;">
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
        return 12000
    elif risco == "Médio":
        return 19000
    return 26000


def gerar_trajetoria(lat, lon, velocidade, posicao):
    if velocidade == "Muito suspeito":
        desloc_lon = 1.35
        desloc_lat = 0.24
    elif velocidade == "Ligeiramente suspeito":
        desloc_lon = 0.98
        desloc_lat = 0.15
    else:
        desloc_lon = 0.65
        desloc_lat = 0.10

    if posicao == "Muito suspeita":
        desloc_lat *= 1.15

    return [
        [lon - desloc_lon, lat + desloc_lat],
        [lon - desloc_lon * 0.78, lat + desloc_lat * 0.58],
        [lon - desloc_lon * 0.50, lat + desloc_lat * 0.26],
        [lon - desloc_lon * 0.23, lat + desloc_lat * 0.10],
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
        <div style="display:flex; gap:12px; flex-wrap:wrap; margin-top:6px; margin-bottom:2px;">
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:11px; height:11px; border-radius:50%; background:#ef4444;"></div>
                <span style="font-size:0.82rem; color:#475569;"><b>Elevado</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:11px; height:11px; border-radius:50%; background:#f59e0b;"></div>
                <span style="font-size:0.82rem; color:#475569;"><b>Médio</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:11px; height:11px; border-radius:50%; background:#22c55e;"></div>
                <span style="font-size:0.82rem; color:#475569;"><b>Baixo</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:18px; height:3px; background:#2563eb;"></div>
                <span style="font-size:0.82rem; color:#475569;"><b>Trajetória</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <div style="width:11px; height:11px; border-radius:50%; background:#64748b;"></div>
                <span style="font-size:0.82rem; color:#475569;"><b>Referência</b></span>
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
        get_color=[37, 99, 235, 235],
        width_scale=20,
        width_min_pixels=5,
        get_width=8 if velocidade == "Muito suspeito" else 7 if velocidade == "Ligeiramente suspeito" else 6,
        pickable=False
    )

    layer_contactos_ref = pdk.Layer(
        "ScatterplotLayer",
        data=df_referencia,
        get_position="[lon, lat]",
        get_fill_color=[100, 116, 139, 85],
        get_radius=2000,
        pickable=False
    )

    layer_perimetro_atencao = pdk.Layer(
        "ScatterplotLayer",
        data=df_contacto,
        get_position="[lon, lat]",
        get_fill_color=[cor[0], cor[1], cor[2], 20],
        get_line_color=[cor[0], cor[1], cor[2], 70],
        line_width_min_pixels=1,
        stroked=True,
        filled=True,
        get_radius=raio + 6000,
        pickable=False
    )

    layer_anel_risco = pdk.Layer(
        "ScatterplotLayer",
        data=df_contacto,
        get_position="[lon, lat]",
        get_fill_color=[0, 0, 0, 0],
        get_line_color=cor,
        line_width_min_pixels=3,
        stroked=True,
        filled=False,
        get_radius=raio,
        pickable=False
    )

    layer_contacto_principal = pdk.Layer(
        "ScatterplotLayer",
        data=df_contacto,
        get_position="[lon, lat]",
        get_fill_color=cor,
        get_line_color=[255, 255, 255, 240],
        line_width_min_pixels=2,
        stroked=True,
        filled=True,
        get_radius=5800,
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
        get_size=14,
        get_color=[255, 255, 255, 245],
        get_angle=0,
        get_text_anchor="'middle'",
        get_alignment_baseline="'center'"
    )

    view_state = pdk.ViewState(
        latitude=lat + 0.01,
        longitude=lon - 0.78,
        zoom=7.0,
        pitch=0
    )

    deck = pdk.Deck(
        map_provider="carto",
        map_style="light",
        initial_view_state=view_state,
        layers=[
            layer_trajetoria,
            layer_contactos_ref,
            layer_perimetro_atencao,
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
