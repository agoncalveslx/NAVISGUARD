import streamlit as st

from config import configurar_pagina
from state import inicializar_estado
from styles import aplicar_estilos

from components.header import render_header
from components.dashboard import render_dashboard
from components.input_panel import render_input_panel
from components.tactical_view import render_tactical_sections
from components.validation import render_validation_section
from components.indicators import render_indicators_section


def main():
    configurar_pagina()
    inicializar_estado()
    aplicar_estilos()

    render_header()
    render_dashboard()

    coluna_esquerda, coluna_direita = st.columns([1, 1], gap="large")

    with coluna_esquerda:
        render_input_panel()

    with coluna_direita:
        render_tactical_sections()

    render_validation_section()
    render_indicators_section()


if __name__ == "__main__":
    main()
