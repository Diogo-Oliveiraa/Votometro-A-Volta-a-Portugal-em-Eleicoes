import streamlit as st
import pandas as pd
import os
import plotly.express as px

# === Carrega o ficheiro com os partidos e os candidatos ===
df_partidos = pd.read_excel("./Docs/Partidos.xlsx")  # Garante que os nomes das colunas são "Partidos" e "Candidatos"

# === Configuração da página ===
st.set_page_config(page_title="Resultados das Eleições", layout="wide")
st.title("Resultados das Eleições por Distrito e Concelho")

# === Define caminhos para os ficheiros de resultados ===
resultados_excel = "./ResultadoEleicoesDistritos/resultados.xlsx"
resultados_dir = "./ResultadoEleicoesDistritos"

# === Verifica se o ficheiro geral de resultados existe ===
if os.path.exists(resultados_excel):
    df_resultados = pd.read_excel(resultados_excel)

    st.subheader("Tabela Geral de Resultados")
    st.dataframe(df_resultados)  # Mostra a tabela completa

    # === Filtros para seleção do Distrito e Concelho ===
    distritos = df_resultados["Distrito"].unique()
    distrito_sel = st.selectbox("Seleciona o Distrito", distritos)

    concelhos = df_resultados[df_resultados["Distrito"] == distrito_sel]["Concelho"].unique()
    concelho_sel = st.selectbox("Seleciona o Concelho", concelhos)

    # === Caminho para o ficheiro com resultados do concelho selecionado ===
    filename = f"{distrito_sel}_{concelho_sel}.xlsx"
    caminho = os.path.join(resultados_dir, filename)

    # === Verifica se o ficheiro do concelho existe ===
    if os.path.exists(caminho):
        df_resultados = pd.read_excel(caminho)

        st.subheader(f"Resultados para {concelho_sel} ({distrito_sel})")
        st.dataframe(df_resultados)

        # === Identifica colunas dos partidos ===
        colunas_fixas = ["Distrito", "Concelho", "Inscritos", "VV", "VN", "VB", "Abstencao"]
        colunas_partidos = [col for col in df_resultados.columns if col not in colunas_fixas]

        # === Soma os votos por partido ===
        votos_por_partido = df_resultados[colunas_partidos].sum()
        total_votos_validos = votos_por_partido.sum()

        # === Prepara DataFrame para o gráfico ===
        df_grafico = pd.DataFrame({
            "Partido": votos_por_partido.index,
            "Votos": votos_por_partido.values
        })

        # === Calcula as percentagens de votos por partido ===
        if total_votos_validos > 0:
            df_grafico["Percentagem"] = round(df_grafico["Votos"] / total_votos_validos * 100, 2)
        else:
            df_grafico["Percentagem"] = 0

        # === Ordena por número de votos (decrescente) ===
        df_grafico = df_grafico.sort_values(by="Votos", ascending=False)

        # === Seleção do tipo de gráfico ===
        tipo_grafico = st.selectbox(
            "Escolhe o tipo de gráfico",
            ["Barras", "Circular", "Linha"]
        )

        # === Gráfico de barras ===
        if tipo_grafico == "Barras":
            fig = px.bar(
                df_grafico,
                x="Partido",
                y="Votos",
                color="Partido",
                text="Percentagem",
                height=700,
                title=f"Distribuição de Votos por Partido em {concelho_sel} ({distrito_sel})"
            )
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

        # === Gráfico circular ===
        elif tipo_grafico == "Circular":
            fig = px.pie(
                df_grafico,
                names="Partido",
                values="Votos",
                title=f"Distribuição de Votos por Partido em {concelho_sel} ({distrito_sel})",
                hover_data=["Percentagem"]
            )
            fig.update_traces(textinfo='percent+label')

        # === Gráfico de linha ===
        elif tipo_grafico == "Linha":
            fig = px.line(
                df_grafico,
                x="Partido",
                y="Votos",
                markers=True,
                title=f"Distribuição de Votos por Partido em {concelho_sel} ({distrito_sel})",
                hover_data=["Percentagem"]
            )

        # === Mostra o gráfico escolhido ===
        st.plotly_chart(fig, use_container_width=True)

        # === Se o concelho selecionado for "Portugal", mostra o vencedor nacional ===
        if concelho_sel.strip().lower() == "portugal":
            vencedor = df_grafico.iloc[0]
            partido_vencedor = vencedor['Partido']

            # Procura o nome do candidato vencedor no ficheiro Partidos.xlsx
            linha_candidato = df_partidos[df_partidos["Partidos"] == partido_vencedor]
            if not linha_candidato.empty:
                candidatos_vencedor = linha_candidato.iloc[0]["Candidatos"]
            else:
                candidatos_vencedor = "Desconhecido"

            # Mostra os resultados
            st.success(
                f"**Vencedor Nacional:** {partido_vencedor} com {vencedor['Votos']} votos ({vencedor['Percentagem']}%)"
            )
            st.info(
                f"**Novo Primeiro Ministro de Portugal:** {candidatos_vencedor} ({partido_vencedor})"
            )

    else:
        st.warning("Ficheiro Excel do concelho não encontrado.")
else:
    st.error("Ficheiro de resultados não encontrado. Por favor, corra primeiro o script de simulação.")