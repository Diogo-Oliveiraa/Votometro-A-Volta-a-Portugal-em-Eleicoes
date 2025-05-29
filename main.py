import streamlit as st
import pandas as pd
import os
import plotly.express as px
import unicodedata

def normalizar_nome(nome):
    return unicodedata.normalize('NFKD', str(nome)).encode('ASCII', 'ignore').decode('ASCII').lower().strip()

# === Carrega o ficheiro com os partidos e os candidatos ===
df_partidos = pd.read_excel("./Docs/Partidos.xlsx")  # Colunas: "Partidos" e "Candidatos"

# === Configuração da página ===
st.set_page_config(page_title="Resultados das Eleições", layout="wide")
st.title("Resultados das Eleições por Distrito e Concelho")

# === Caminhos dos ficheiros ===
resultados_excel = "./ResultadoEleicoesDistritos/resultados.xlsx"
resultados_dir = "./ResultadoEleicoesDistritos"

if os.path.exists(resultados_excel):
    df_resultados_geral = pd.read_excel(resultados_excel)
    st.subheader("Tabela Geral de Resultados")
    st.dataframe(df_resultados_geral)

    # === Identifica distritos, Portugal e Fora de Portugal ===
    distritos_raw = df_resultados_geral["Distrito"].unique()
    distritos_nacionais = sorted(
        [d for d in distritos_raw if normalizar_nome(d) not in ["portugal", "fora de portugal", "fora portugal"]],
        key=normalizar_nome
    )
    portugal_nomes = [d for d in distritos_raw if normalizar_nome(d) == "portugal"]
    fora_nomes = [d for d in distritos_raw if normalizar_nome(d) in ["fora de portugal", "fora portugal"]]
    distritos = distritos_nacionais
    if portugal_nomes:
        distritos.append(portugal_nomes[0])
    if fora_nomes:
        distritos.append(fora_nomes[0])

    distrito_sel = st.selectbox("Seleciona o Distrito", distritos)

    # === Lista de concelhos filtrados para o distrito ===
    if normalizar_nome(distrito_sel) == "portugal":
        concelhos = ["Portugal"]

    elif normalizar_nome(distrito_sel) in ["fora de portugal", "fora portugal"]:
        # Filtra todas as linhas do distrito "FORA PORTUGAL" (com ou sem DE)
        linhas_fora = df_resultados_geral[
            df_resultados_geral["Distrito"].apply(lambda x: normalizar_nome(x) in ["fora de portugal", "fora portugal"])
        ]
        # Extrai os concelhos únicos, removendo nulos e espaços
        concelhos_fora = [str(c).strip() for c in linhas_fora["Concelho"].dropna().unique()]
        # Só apresenta EUROPA e FORA EUROPA, pela ordem do ficheiro
        concelhos = []
        for nome in ["EUROPA", "FORA EUROPA"]:
            for c in concelhos_fora:
                if normalizar_nome(c) == normalizar_nome(nome):
                    concelhos.append(c)
        # Adiciona a opção "Total" no início
        concelhos.insert(0, "Total")
        # Se não encontrar, apresenta mensagem de erro
        if len(concelhos) == 1:  # Só tem "Total"
            st.warning("Não foram encontrados os concelhos 'EUROPA' e 'FORA EUROPA' para 'FORA PORTUGAL'.")

    else:
        concelhos_validos = df_resultados_geral[
            (df_resultados_geral["Distrito"] == distrito_sel)
        ]["Concelho"].unique()
        # Remover concelhos especiais se existirem
        concelhos_validos = [
            c for c in concelhos_validos
            if normalizar_nome(c) not in [
                "portugal", "fora de portugal", "fora portugal", "europa", "fora europa"
            ]
        ]
        concelhos = sorted([c.strip() for c in concelhos_validos], key=normalizar_nome)
        concelhos.insert(0, "TOTAL DISTRITO")

    concelho_sel = st.selectbox("Seleciona o Concelho", concelhos)

    # === Função para mostrar tabela e gráfico ===
    def mostra_resultados(df_resultados, titulo):
        st.subheader(titulo)
        st.dataframe(df_resultados)

        colunas_fixas = ["Distrito", "Concelho", "Inscritos", "VV", "VN", "VB", "Abstencao"]
        colunas_partidos = [col for col in df_resultados.columns if col not in colunas_fixas]

        votos_por_partido = df_resultados[colunas_partidos].sum()
        total_votos_validos = votos_por_partido.sum()

        df_grafico = pd.DataFrame({
            "Partido": votos_por_partido.index,
            "Votos": votos_por_partido.values
        })

        if total_votos_validos > 0:
            df_grafico["Percentagem"] = round(df_grafico["Votos"] / total_votos_validos * 100, 2)
        else:
            df_grafico["Percentagem"] = 0

        df_grafico = df_grafico.sort_values(by="Votos", ascending=False)

        tipo_grafico = st.selectbox(
            "Escolhe o tipo de gráfico",
            ["Barras", "Circular", "Linha"],
            key=f"grafico_{titulo}"
        )

        if tipo_grafico == "Barras":
            fig = px.bar(df_grafico, x="Partido", y="Votos", color="Partido",
                         text="Percentagem", height=700, title=titulo)
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        elif tipo_grafico == "Circular":
            fig = px.pie(df_grafico, names="Partido", values="Votos", title=titulo,
                         hover_data=["Percentagem"])
            fig.update_traces(textinfo='percent+label')
        elif tipo_grafico == "Linha":
            fig = px.line(df_grafico, x="Partido", y="Votos", markers=True,
                          title=titulo, hover_data=["Percentagem"])

        st.plotly_chart(fig, use_container_width=True)
        return df_grafico

    # === MOSTRA RESULTADOS NACIONAIS (PORTUGAL) ===
    if normalizar_nome(distrito_sel) == "portugal" and normalizar_nome(concelho_sel) == "portugal":
        df_resultados = df_resultados_geral[
            (df_resultados_geral["Distrito"].apply(normalizar_nome) == "portugal") &
            (df_resultados_geral["Concelho"].apply(normalizar_nome) == "portugal")
        ]
        df_grafico = mostra_resultados(df_resultados, "Resultados Nacionais (Portugal)")

        vencedor = df_grafico.iloc[0]
        partido_vencedor = vencedor['Partido']
        linha_candidato = df_partidos[df_partidos["Partidos"] == partido_vencedor]
        candidatos_vencedor = linha_candidato.iloc[0]["Candidatos"] if not linha_candidato.empty else "Desconhecido"

        st.success(
            f"**Vencedor Nacional:** {partido_vencedor} com {vencedor['Votos']} votos ({vencedor['Percentagem']}%)"
        )
        st.info(
            f"**Novo Primeiro Ministro de Portugal:** {candidatos_vencedor} ({partido_vencedor})"
        )

    # === MOSTRA RESULTADOS FORA DE PORTUGAL ===
    elif normalizar_nome(distrito_sel) in ["fora de portugal", "fora portugal"]:
        if concelho_sel == "Total":
            # Agrega os dados de EUROPA e FORA EUROPA (uma só linha)
            df_total = df_resultados_geral[
                (df_resultados_geral["Distrito"].apply(lambda x: normalizar_nome(x) in ["fora de portugal", "fora portugal"])) &
                (df_resultados_geral["Concelho"].apply(lambda x: normalizar_nome(x) in ["europa", "fora europa"]))
            ]
            if not df_total.empty:
                # Soma todos os campos numéricos
                campos_numericos = df_total.select_dtypes(include='number').columns
                total_row = df_total[campos_numericos].sum()
                # Preenche os campos de texto
                total_row["Distrito"] = "Fora de Portugal"
                total_row["Concelho"] = "Total"
                # Coloca os campos na ordem correta
                outras_colunas = [col for col in df_total.columns if col not in campos_numericos and col not in ["Distrito", "Concelho"]]
                total_row = total_row.reindex(["Distrito", "Concelho"] + list(campos_numericos) + outras_colunas)
                # Cria DataFrame de uma linha
                df_resultados = pd.DataFrame([total_row])
                mostra_resultados(df_resultados, "Total Fora de Portugal (EUROPA + FORA EUROPA)")
            else:
                st.warning("Não existem dados para EUROPA e FORA EUROPA em Fora de Portugal.")
        else:
            df_resultados = df_resultados_geral[
                (df_resultados_geral["Distrito"].apply(lambda x: normalizar_nome(x) in ["fora de portugal", "fora portugal"])) &
                (df_resultados_geral["Concelho"] == concelho_sel)
            ]
            mostra_resultados(df_resultados, f"Resultados para {concelho_sel} (Fora de Portugal)")

    # === MOSTRA RESULTADOS TOTAIS DO DISTRITO ===
    elif concelho_sel == "TOTAL DISTRITO":
        df_totais = df_resultados_geral[
            (df_resultados_geral["Distrito"] == distrito_sel) &
            (df_resultados_geral["Concelho"] == distrito_sel)
        ]
        if not df_totais.empty:
            idx_max = df_totais["Inscritos"].idxmax()
            df_resultados = df_totais.loc[[idx_max]]
            mostra_resultados(df_resultados, f"Total do Distrito de {distrito_sel}")
        else:
            st.warning("Não existe linha de total do distrito no ficheiro de resultados.")

    # === MOSTRA RESULTADOS DO CONCELHO INDIVIDUAL ===
    else:
        filename = f"{distrito_sel}_{concelho_sel}.xlsx"
        caminho = os.path.join(resultados_dir, filename)
        if os.path.exists(caminho):
            df_resultados = pd.read_excel(caminho)
            mostra_resultados(df_resultados, f"Resultados para {concelho_sel} ({distrito_sel})")
        else:
            st.warning("Ficheiro Excel do concelho não encontrado.")
else:
    st.error("Ficheiro de resultados não encontrado. Por favor, corra primeiro o script de simulação.")
