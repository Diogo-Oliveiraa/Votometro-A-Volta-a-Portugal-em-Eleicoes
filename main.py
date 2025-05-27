import streamlit as st
import pandas as pd
import os
import json

st.set_page_config(page_title="Resultados das Eleições", layout="wide")

st.title("Resultados das Eleições por Distrito e Concelho")

# Caminho para o ficheiro de resultados
resultados_excel = "./ResultadoEleicoesDistritos/resultados.xlsx"
resultados_dir = "./ResultadoEleicoesDistritos"

if os.path.exists(resultados_excel):
    df_resultados = pd.read_excel(resultados_excel)
    st.subheader("Tabela Geral de Resultados")
    st.dataframe(df_resultados)

    # Filtro por Distrito e Concelho
    distritos = df_resultados["Distrito"].unique()
    distrito_sel = st.selectbox("Seleciona o Distrito", distritos)
    concelhos = df_resultados[df_resultados["Distrito"] == distrito_sel]["Concelho"].unique()
    concelho_sel = st.selectbox("Seleciona o Concelho", concelhos)

    # Mostrar resultados do concelho selecionado
    filename = f"{distrito_sel}_{concelho_sel}.json"
    caminho = os.path.join(resultados_dir, filename)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            resultado = json.load(f)
        st.subheader(f"Resultados para {concelho_sel} ({distrito_sel})")
        st.json(resultado)
    else:
        st.warning("Ficheiro JSON do concelho não encontrado.")

    # Download do Excel
    st.download_button(
        label="Descarregar Resultados em Excel",
        data=df_resultados.to_excel(index=False),
        file_name="resultados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.error("Ficheiro de resultados não encontrado. Por favor, corre primeiro o script de simulação.")


