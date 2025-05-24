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

if __name__ == "__main__":
    main()