import os
import random
import json
import pandas as pd

from simular_votos import simular_votos, resultado_votos


def carregar_dados_partidos(path_partidos: str) -> tuple[list, dict]:
    """
    Carrega os dados dos partidos a partir de um ficheiro Excel.

    :param path_partidos: Caminho para o ficheiro Excel com partidos e candidatos.
    :return: Lista com nomes dos partidos e dicionário com pesos ou candidatos por partido.
    """
    df_partidos = pd.read_excel(path_partidos)
    partidos = df_partidos["Partidos"].tolist()
    pesos_partidos = dict(zip(df_partidos["Partidos"], df_partidos["Candidatos"]))
    return partidos, pesos_partidos


def adicionar_total_nacional(df_resultados: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona uma linha com os totais nacionais ao DataFrame.

    :param df_resultados: DataFrame com os resultados por concelho.
    :return: DataFrame com linha adicional de totais nacionais.
    """
    colunas_numericas = df_resultados.select_dtypes(include='number').columns
    total_nacional = df_resultados[colunas_numericas].sum(numeric_only=True)

    linha_portugal = {
        "Distrito": "PORTUGAL",
        "Concelho": "PORTUGAL",
        **total_nacional
    }
    return pd.concat([df_resultados, pd.DataFrame([linha_portugal])], ignore_index=True)


def adicionar_totais_por_distrito(df_resultados: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona linhas com os totais por distrito (com Concelho = nome do Distrito).

    :param df_resultados: DataFrame com resultados por concelho.
    :return: DataFrame com linhas adicionais de totais por distrito.
    """
    distritos = df_resultados["Distrito"].unique()
    colunas_numericas = df_resultados.select_dtypes(include='number').columns

    linhas_totais_distritos = []

    for distrito in distritos:
        if distrito.strip().lower() == "portugal":
            continue

        df_distrito = df_resultados[df_resultados["Distrito"] == distrito]
        soma_distrito = df_distrito[colunas_numericas].sum(numeric_only=True)

        linha_distrito = {
            "Distrito": distrito,
            "Concelho": distrito,
            **soma_distrito
        }
        linhas_totais_distritos.append(linha_distrito)

    return pd.concat([df_resultados, pd.DataFrame(linhas_totais_distritos)], ignore_index=True)


def main():
    """
    Função principal que simula votos, gera os resultados e adiciona totais
    por distrito e nacional.
    """
    # === Caminhos ===
    path_partidos = "./Docs/partidos.xlsx"
    path_distritos = "./Docs/Distritos_Concelhos.xlsx"
    path_resultados = "./ResultadoEleicoesDistritos/resultados.xlsx"

    # === Carrega dados dos partidos e distritos ===
    partidos, _ = carregar_dados_partidos(path_partidos)
    df_distritos = pd.read_excel(path_distritos)

    # === Simula os votos ===
    resultados = resultado_votos(df_distritos, partidos)
    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel(path_resultados, index=False)

    # === Adiciona totais ===
    df_resultados = pd.read_excel(path_resultados)
    df_resultados = adicionar_total_nacional(df_resultados)
    df_resultados = adicionar_totais_por_distrito(df_resultados)

    # === Guarda os resultados finais ===
    df_resultados.to_excel(path_resultados, index=False)


if __name__ == "__main__":
    main()