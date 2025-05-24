import random
import json
import os

def simular_votos(total_votos, partidos,pesos_partidos):

    votos_nulos = int(total_votos * 0.02)     # 2%
    votos_brancos = int(total_votos * 0.03)   # 3%
    votos_validos = total_votos - votos_nulos - votos_brancos

    distribuicao = {p: 0 for p in partidos}
    pesos = [pesos_partidos[p] for p in partidos]

    votos_simulados = random.choices(partidos, weights=pesos, k=votos_validos)

    for partido in votos_simulados:
        distribuicao[partido] += 1

    return distribuicao, votos_nulos, votos_brancos


def resultado_votos(distritos_concelhos, partidos, pesos_partidos):

    resultadoscsv = []

    for i, row in distritos_concelhos.iterrows():
        distrito = row["Distrito"]
        concelho = row["Concelho"]
        populacao = row["Inscritos"]
        votos, votos_nulos, votos_brancos = simular_votos(populacao, partidos, pesos_partidos)

        resultado = {
            "Distrito": distrito,
            "Concelho": concelho,
            "Votos Nulos": votos_nulos,
            "Votos Brancos": votos_brancos,
        }

        resultado.update(votos)
        resultadoscsv.append(resultado)

        filename = f"{distrito}_{concelho}.json"
        caminho = os.path.join("./ResultadoEleicoesDistritos", filename)

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)

    return resultadoscsv