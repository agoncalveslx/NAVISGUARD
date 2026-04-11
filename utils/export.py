from utils.cases import tipo_decisao
from utils.risk import formula_caso_texto


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
        linhas.append(
            f"Justificação: {decisao['justificacao'] if decisao['justificacao'] else 'Não foi fornecida justificação.'}"
        )

    return "\n".join(linhas)
