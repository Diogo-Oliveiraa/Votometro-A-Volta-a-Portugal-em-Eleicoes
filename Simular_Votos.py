"""Biblioteca para dados random / guardar em ficheiro JSON / localizao do OS"""
import random
import json
import os
import pandas as pd

def simular_votos(total_votos, partidos):
    """ Função para simular uma distribuição aleatoria dos votos"""
    distribuicao = {p: 0 for p in partidos}
    votos_simulados = random.choices(partidos, k=total_votos)

    for partido in votos_simulados:
        distribuicao[partido] += 1

    return distribuicao

def resultado_votos(distritos_concelhos, partidos):
    """ Função para guardar os votos por concelho em ficheiro JSON e Excel """
    os.makedirs("./ResultadoEleicoesDistritos/JSON", exist_ok=True)
    os.makedirs("./ResultadoEleicoesDistritos/XLSX", exist_ok=True)

    for _, row in distritos_concelhos.iterrows():
        distrito = row["Distrito"]
        concelho = row["Concelho"]
        populacao = row["Inscritos"]

        votos = simular_votos(populacao, partidos)

        resultado = {
            "Distrito": distrito,
            "Concelho": concelho,
            "Inscritos": populacao,
        }

        resultado.update(votos)
        resultado.pop("NaoVotantes",None)

        """ Cria um ficheiro JSON com as votações dos partidos"""
        filename = f"{concelho}.json"
        caminho = os.path.join("./ResultadoEleicoesDistritos/JSON", filename)

        with open(caminho, "w", encoding="utf-8") as file:
            json.dump(resultado, file, indent=2, ensure_ascii=False)

        """ Cria um ficheiro excel com as votações dos partidos"""
        filename_excel = f"{distrito}_{concelho}.xlsx"
        caminho_excel = os.path.join("./ResultadoEleicoesDistritos/XLSX", filename_excel)
        df_resultado = pd.DataFrame([resultado])
        df_resultado.to_excel(caminho_excel, index=False)


def main():
    """Simulação a partir dos ficheiros de entrada"""
    df_partidos = pd.read_excel("./Docs/partidos.xlsx")
    partidos = df_partidos["Partidos"].tolist()
    distritos_concelhos = pd.read_excel("./Docs/Distritos_Concelhos.xlsx")
    resultado_votos(distritos_concelhos, partidos)


if __name__ == "__main__":
    main()
