from datetime import datetime
import streamlit as st

from utils.cases import resultado_em_reserva, gerar_id_decisao, tipo_decisao
from utils.history import atualizar_decisao_no_historico
from utils.export import exportar_registo_txt


def render_validation_section():
    em_reserva = resultado_em_reserva()

    if st.session_state.resultado_gerado and st.session_state.dados_resultado is not None and not em_reserva:
        dados = st.session_state.dados_resultado
        pontuacao_total = dados["pontuacao_total"]
        risco = dados["risco"]
        acao = dados["acao"]

        st.markdown('<div class="cartao cartao-azul">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">6. VALIDAÇÃO TÁTICA</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">O especialista procede à validação tática da recomendação automática, podendo confirmá-la ou ajustá-la com a devida fundamentação.</div>', unsafe_allow_html=True)

        decisao_utilizador = st.selectbox(
            "Decisão Tática Final",
            ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"],
            label_visibility="visible"
        )

        justificacao = st.text_area(
            "Justificação da decisão final",
            placeholder="Fundamenta a decisão tática adotada com base na situação operacional...",
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

                atualizar_decisao_no_historico(
                    historico=st.session_state.historico_casos,
                    id_caso=dados["id_caso"],
                    acao_proposta=acao,
                    decisao_final=decisao_final,
                    justificacao=justificacao.strip(),
                    timestamp_decisao=timestamp_decisao,
                    tipo_decisao_fn=tipo_decisao
                )

        if st.session_state.decisao_guardada is not None:
            reg = st.session_state.decisao_guardada
            tipo = tipo_decisao(reg["acao_proposta"], reg["decisao_final"])
            classe_tipo = "estado-confirmacao" if tipo == "Confirmada" else "estado-alteracao"

            st.markdown('<div class="cartao cartao-verde">', unsafe_allow_html=True)
            st.markdown('<div class="titulo-secao">7. DECISÃO FINAL</div>', unsafe_allow_html=True)
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

    elif st.session_state.resultado_gerado and em_reserva:
        st.markdown('<div class="cartao cartao-amarelo">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">Informação em reserva</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitulo-secao">O caso foi alterado após a última geração.</div>', unsafe_allow_html=True)
        st.warning("As entradas foram alteradas. Gere nova recomendação para atualizar a avaliação tática, a rastreabilidade, o mapa tático e a confirmação do especialista.")
        st.markdown('</div>', unsafe_allow_html=True)
