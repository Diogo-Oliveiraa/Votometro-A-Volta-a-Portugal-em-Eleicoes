import pandas as pd
import random
import json
import os

from Simular_Votos import simular_votos
from Simular_Votos import resultado_votos


df_partidos = pd.read_excel("./Docs/partidos.xlsx")

partidos = df_partidos["Partidos"].tolist()

pesospartidos = dict(zip(df_partidos["Partidos"], df_partidos["Peso"]))

distritos_concelhos = pd.read_excel("./Docs/Distritos_Concelhos.xlsx")

def main():
    resultadoscsv = resultado_votos(distritos_concelhos, partidos, pesospartidos)
    df_resultados = pd.DataFrame(resultadoscsv)
    df_resultados.to_excel("./ResultadoEleicoesDistritos/resultados.xlsx")

    # === ADICIONAR TOTAL NACIONAL ("Portugal") ===
    df_resultados = pd.read_excel("./ResultadoEleicoesDistritos/resultados.xlsx")
    colunas_soma = [col for col in df_resultados.columns if col not in ["Distrito", "Concelho"]]
    total_nacional = df_resultados[colunas_soma].sum(numeric_only=True)
    linha_portugal = {
        "Distrito": "PORTUGAL",
        "Concelho": "PORTUGAL"
    }
    linha_portugal.update(total_nacional)
    df_resultados = pd.concat([
        df_resultados,
        pd.DataFrame([linha_portugal])
    ], ignore_index=True)
    df_resultados.to_excel("./ResultadoEleicoesDistritos/resultados.xlsx", index=False)

    # == Para cada distrito, soma todos os concelhos == #
    distritos = df_resultados["Distrito"].unique()
    linhas_distritos = []
    for distrito in distritos:
        if distrito.lower() == "portugal":
            continue
        df_distrito = df_resultados[df_resultados["Distrito"] == distrito]
        colunas_soma = [col for col in df_resultados.columns if col not in ["Distrito", "Concelho"]]
        soma_distrito = df_distrito[colunas_soma].sum(numeric_only=True)
        linha_distrito = {"Distrito": distrito, "Concelho": distrito}
        linha_distrito.update(soma_distrito)
        linhas_distritos.append(linha_distrito)

    # Junta as linhas dos distritos ao DataFrame
    df_resultados = pd.concat([df_resultados, pd.DataFrame(linhas_distritos)], ignore_index=True)
    df_resultados.to_excel("./ResultadoEleicoesDistritos/resultados.xlsx", index=False)


if __name__ == "__main__":
    main()