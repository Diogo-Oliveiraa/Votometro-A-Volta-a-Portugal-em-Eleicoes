"""
Aplicacao Streamlit para visualizacao dos resultados eleitorais por distrito e concelho,
com base em ficheiros Excel de resultados e uma simulacao dos votos.
"""

# === Importações ===
import os
import time
import unicodedata

import pandas as pd
import plotly.express as px
import streamlit as st

# === Constantes de caminho ===
RESULTADOS_EXCEL = "./ResultadosFinais/VotosValidados.xlsx"  # Caminho para o ficheiro principal de resultados
RESULTADOS_DIR = "./ResultadoEleicoesDistritos/XLSX"          # Diretório com ficheiros por concelho
PARTIDOS_PATH = "./Docs/Partidos.xlsx"                        # Caminho para a lista de partidos e candidatos

# === Função para normalizar nomes (acentos, espaços, minúsculas) ===
def normalizar_nome(nome: str) -> str:
    """
    Normaliza um nome, removendo acentuacao, convertendo para minusculas
    e removendo espacos em excesso nas extremidades.
    """
    return unicodedata.normalize('NFKD', str(nome)).encode('ASCII', 'ignore').decode('ASCII').lower().strip()

# === Função para identificar se é "Fora de Portugal" ===
def eh_fora_de_portugal(nome: str) -> bool:
    """Verifica se o nome corresponde a 'Fora de Portugal'."""
    return normalizar_nome(nome) in ["fora de portugal", "fora portugal"]

# === Função para mostrar resultados com gráfico ===
def mostra_resultados(df_resultados: pd.DataFrame, titulo: str) -> pd.DataFrame:
    """
    Mostra no Streamlit uma tabela com os resultados eleitorais e um grafico interativo
    com os votos por partido.
    """
    st.subheader(titulo)
    st.dataframe(df_resultados)  # Mostrar os dados numa tabela

    # Colunas que não representam partidos
    colunas_fixas = ["Distrito", "Concelho", "Inscritos", "VV", "VN", "VB", "Abstencao"]

    # Detetar colunas com votos dos partidos
    colunas_partidos = [col for col in df_resultados.columns if col not in colunas_fixas]

    # Somatório de votos por partido
    votos_por_partido = df_resultados[colunas_partidos].sum()
    total_votos_validos = votos_por_partido.sum()

    # Criar DataFrame para gráfico
    df_grafico = pd.DataFrame({
        "Partido": votos_por_partido.index,
        "Votos": votos_por_partido.values
    })

    # Calcular percentagem de votos
    df_grafico["Percentagem"] = (
        round(df_grafico["Votos"] / total_votos_validos * 100, 2)
        if total_votos_validos > 0 else 0
    )
    df_grafico = df_grafico.sort_values(by="Votos", ascending=False)  # Ordenar por votos

    # Escolha do tipo de gráfico (barras, circular, linha)
    tipo_grafico = st.selectbox(
        "Escolhe o tipo de grafico",
        ["Barras", "Circular", "Linha"],
        key=f"grafico_{titulo}"
    )

    # Criar gráfico de barras
    if tipo_grafico == "Barras":
        fig = px.bar(df_grafico, x="Partido", y="Votos", color="Partido",
                     text="Percentagem", height=700, title=titulo)
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    # Criar gráfico circular
    elif tipo_grafico == "Circular":
        fig = px.pie(df_grafico, names="Partido", values="Votos", title=titulo,
                     hover_data=["Percentagem"])
        fig.update_traces(textinfo='percent+label')

    # Criar gráfico de linha
    else:
        fig = px.line(df_grafico, x="Partido", y="Votos", markers=True,
                      title=titulo, hover_data=["Percentagem"])

    st.plotly_chart(fig, use_container_width=True)  # Mostrar gráfico
    return df_grafico  # Retornar dataframe com dados para possível análise extra

# === Configuração inicial do Streamlit ===
st.set_page_config(page_title="Resultados das Eleicoes", layout="wide")
st.title("Resultados das Eleicoes por Distrito e Concelho")

# === Carregar dados dos partidos ===
df_partidos = pd.read_excel(PARTIDOS_PATH)

# Verifica se o ficheiro de resultados existe
if not os.path.exists(RESULTADOS_EXCEL):
    st.error(f"O ficheiro de resultados '{RESULTADOS_EXCEL}' nao foi encontrado.")
    st.stop()

# Estado da simulação guardado na sessão
if "simulacao" not in st.session_state:
    st.session_state.simulacao = False

# Se ainda não foi feita a simulação, mostrar botão
if not st.session_state.simulacao:
    if st.button("🗳️ Simular Eleicoes"):
        with st.spinner("A simular os resultados..."):
            time.sleep(2)  # Simula tempo de processamento
            st.session_state.simulacao = True
            st.rerun()  # Recarrega a aplicação
    else:
        st.info("Clique no botao acima para simular as eleicoes.")
        st.stop()

# === Carrega os resultados gerais ===
df_resultados_geral = pd.read_excel(RESULTADOS_EXCEL)

# Filtra apenas os distritos nacionais (exclui Fora de Portugal e "Portugal")
distritos_nacionais = [d for d in df_resultados_geral["Distrito"].unique() if not eh_fora_de_portugal(d) and normalizar_nome(d) != "portugal"]
df_nacional = df_resultados_geral[df_resultados_geral["Distrito"].isin(distritos_nacionais)]

# Adiciona linha com total nacional (Portugal)
if not df_nacional.empty:
    soma_total = df_nacional.select_dtypes(include='number').sum()
    linha_portugal = {"Distrito": "Portugal", "Concelho": "Portugal"}
    linha_portugal.update(soma_total.to_dict())
    df_resultados_geral = pd.concat([df_resultados_geral, pd.DataFrame([linha_portugal])], ignore_index=True)

# === Interface de seleção ===
st.subheader("Selecao por Distrito e Concelho")

# Lista de distritos ordenada e limpa
distritos = sorted(df_resultados_geral["Distrito"].unique(), key=normalizar_nome)
distrito_sel = st.selectbox("Seleciona o Distrito", distritos)

# Define os concelhos disponíveis conforme o distrito selecionado
if normalizar_nome(distrito_sel) == "portugal":
    concelhos = ["Portugal"]
elif eh_fora_de_portugal(distrito_sel):
    # Para Fora de Portugal, procura EUROPA e FORA EUROPA
    linhas_fora = df_resultados_geral[df_resultados_geral["Distrito"].apply(eh_fora_de_portugal)]
    concelhos_fora = [str(c).strip() for c in linhas_fora["Concelho"].dropna().unique()]
    concelhos = [c for nome in ["EUROPA", "FORA EUROPA"] for c in concelhos_fora if normalizar_nome(c) == normalizar_nome(nome)]
    concelhos.insert(0, "Total")
    if len(concelhos) == 1:
        st.warning("Nao foram encontrados os concelhos 'EUROPA' e 'FORA EUROPA'.")
else:
    # Para distritos normais, lista os concelhos válidos
    concelhos_validos = df_resultados_geral[df_resultados_geral["Distrito"] == distrito_sel]["Concelho"].unique()
    concelhos = sorted([
        c.strip() for c in concelhos_validos
        if normalizar_nome(c) not in ["portugal", "fora de portugal", "fora portugal", "europa", "fora europa"]
    ], key=normalizar_nome)
    concelhos.insert(0, "TOTAL DISTRITO")

# Caixa de seleção de concelho
concelho_sel = st.selectbox("Seleciona o Concelho", concelhos)

# === Mostrar resultados conforme seleção ===
if normalizar_nome(distrito_sel) == "portugal" and normalizar_nome(concelho_sel) == "portugal":
    # Caso Nacional
    df_resultados = df_resultados_geral[
        (df_resultados_geral["Distrito"] == "Portugal") &
        (df_resultados_geral["Concelho"] == "Portugal")
    ]
    df_grafico = mostra_resultados(df_resultados, "Resultados Nacionais (Portugal)")
    vencedor = df_grafico.iloc[0]
    linha_candidato = df_partidos[df_partidos["Partidos"] == vencedor['Partido']]
    candidatos_vencedor = linha_candidato.iloc[0]["Candidatos"] if not linha_candidato.empty else "Desconhecido"
    st.success(f"**Vencedor Nacional:** {vencedor['Partido']} com {vencedor['Votos']} votos ({vencedor['Percentagem']}%)")
    st.info(f"**Novo Primeiro Ministro de Portugal:** {candidatos_vencedor} ({vencedor['Partido']})")

elif eh_fora_de_portugal(distrito_sel):
    # Caso de votação fora de Portugal
    if concelho_sel == "Total":
        df_total = df_resultados_geral[
            df_resultados_geral["Distrito"].apply(eh_fora_de_portugal) &
            df_resultados_geral["Concelho"].apply(lambda x: normalizar_nome(x) in ["europa", "fora europa"])
        ]
        if not df_total.empty:
            campos_numericos = df_total.select_dtypes(include='number').columns
            total_row = df_total[campos_numericos].sum()
            total_row["Distrito"] = "Fora de Portugal"
            total_row["Concelho"] = "Total"
            outras_colunas = [col for col in df_total.columns if col not in campos_numericos and col not in ["Distrito", "Concelho"]]
            total_row = total_row.reindex(["Distrito", "Concelho"] + list(campos_numericos) + outras_colunas)
            df_resultados = pd.DataFrame([total_row])
            mostra_resultados(df_resultados, "Total Fora de Portugal (EUROPA + FORA EUROPA)")
        else:
            st.warning("Nao existem dados para EUROPA e FORA EUROPA.")
    else:
        df_resultados = df_resultados_geral[
            df_resultados_geral["Distrito"].apply(eh_fora_de_portugal) &
            (df_resultados_geral["Concelho"] == concelho_sel)
        ]
        mostra_resultados(df_resultados, f"Resultados para {concelho_sel} (Fora de Portugal)")

elif concelho_sel == "TOTAL DISTRITO":
    # Linha de total do distrito
    df_totais = df_resultados_geral[
        (df_resultados_geral["Distrito"] == distrito_sel) &
        (df_resultados_geral["Concelho"] == distrito_sel)
    ]
    if not df_totais.empty:
        idx_max = df_totais["Inscritos"].idxmax()
        df_resultados = df_totais.loc[[idx_max]]
        mostra_resultados(df_resultados, f"Total do Distrito de {distrito_sel}")
    else:
        st.warning("Nao existe linha de total do distrito no ficheiro.")
else:
    # Caso de concelho específico dentro de distrito
    filename = f"{distrito_sel}_{concelho_sel}.xlsx"
    caminho = os.path.join(RESULTADOS_DIR, filename)
    if os.path.exists(caminho):
        df_resultados = pd.read_excel(caminho)
        mostra_resultados(df_resultados, f"Resultados para {concelho_sel} ({distrito_sel})")
    else:
        st.warning(f"Ficheiro de resultados nao encontrado para {concelho_sel} ({distrito_sel}).")