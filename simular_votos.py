"""Biblioteca para dados random / guardar em ficheiro JSON / localizao do OS"""
import random
import os
import json
import pandas as pd

def simular_votos(total_votos, partidos):
    """ Função para simular uma distribuição aleatoria dos votos"""
    distribuicao = {p: 0 for p in partidos}
    votos_simulados = random.choices(partidos, k=total_votos)

    for partido in votos_simulados:
        distribuicao[partido] += 1
    return distribuicao

def criar_pastas():
    """ Criação das pastas para guardar os ficheiros"""
    try:
        os.makedirs("./ResultadoEleicoesDistritos/JSON", exist_ok=True)
        os.makedirs("./ResultadoEleicoesDistritos/XLSX", exist_ok=True)
        return True
    except OSError as e:
        print(f"Pastas não criadas! {e}")
        return False

def resultado_votos(distritos_concelhos, partidos):
    """ Função para guardar os votos por concelho em ficheiro JSON e Excel """
    criar_pastas()

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

        #Cria um ficheiro JSON com as votações dos partidos
        filename = f"{concelho}.json"
        caminho = os.path.join("./ResultadoEleicoesDistritos/JSON", filename)

        with open(caminho, "w", encoding="utf-8") as jsonfile:
            json.dump(resultado, jsonfile, indent=2, ensure_ascii=False)

        #Cria um ficheiro excel com as votacoes dos partidos
        filename_excel = f"{distrito}_{concelho}.xlsx"
        caminho_excel = os.path.join("./ResultadoEleicoesDistritos/XLSX", filename_excel)
        df_resultado = pd.DataFrame([resultado])
        df_resultado.to_excel(caminho_excel, index=False)

        print(f"Votos efetuados {distrito}_{concelho}")

    print("Votos concluidos!")

def lerdocs():
    """Verificação dos ficheiros e inicio da simulação"""
    try:
        df_partidos = pd.read_excel("./Docs/partidos.xlsx")
        distritos_concelhos = pd.read_excel("./Docs/Distritos_Concelhos.xlsx")
    except FileNotFoundError as erro:
        print(f"Ficheiros não encontrados : {erro}")
        return False

    partidos = df_partidos["Partidos"].tolist()
    resultado_votos(distritos_concelhos, partidos)
    return None


def main():
    """Função principal"""
    lerdocs()

if __name__ == "__main__":
    main()
