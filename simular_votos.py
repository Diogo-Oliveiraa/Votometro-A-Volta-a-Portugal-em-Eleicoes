"""Biblioteca para dados random / guardar em ficheiro JSON / localizao do OS"""
import random
import os
import json
import pandas as pd

def gerar_pesos(partidos):
    """Gera pesos fixos para cada partido, com alguns mais fortes"""
    pesos = {}
    partidos_favoritos = random.sample(partidos, k=random.choice([1, 2]))

    for partido in partidos:
        if partido in partidos_favoritos:
            pesos[partido] = random.uniform(4.0, 6.0)
        else:
            pesos[partido] = random.uniform(0.5, 2.0)

    return pesos

def simular_votos(total_votos, pesos):
    """Simula votos com base em pesos para todos os concelhos"""
    partidos = list(pesos.keys())
    valores = list(pesos.values())

    total_peso = sum(valores)
    proporcoes = [v / total_peso for v in valores]

    votos_distribuidos = [int(p * total_votos) for p in proporcoes]
    votos_em_falta = total_votos - sum(votos_distribuidos)

    for _ in range(votos_em_falta):
        idx = random.choices(range(len(partidos)), weights=proporcoes)[0]
        votos_distribuidos[idx] += 1

    return {partidos[i]: votos_distribuidos[i] for i in range(len(partidos))}

def verificar_dados_existentes(caminho_excel, total_esperado=310):
    """ Verificar se já existe dados nas pastas"""
    if os.path.exists(caminho_excel):
        ficheiros = [f for f in os.listdir(caminho_excel) if f.endswith(".xlsx")]
        total_pasta = len(ficheiros)

        if total_esperado > 0:
            mensagem = input(
                f"A pasta contém {total_pasta} ficheiros .xlsx "
                f"(esperado: {total_esperado}).\n"
                "Deseja continuar e sobrescrever os ficheiros existentes? (s/n): ").strip().lower()

            if mensagem == 's':
                for ficheiro in ficheiros:
                    os.remove(os.path.join(caminho_excel, ficheiro))
                    print("Ficheiros eliminados")
            else:
                return False
    return True

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

    pesos = gerar_pesos(partidos)  #Gerar os pesos uma única vez

    for _, row in distritos_concelhos.iterrows():
        distrito = row["Distrito"]
        concelho = row["Concelho"]
        populacao = row["Inscritos"]

        votos = simular_votos(populacao, pesos)  # <--- Usar os pesos fixos

        resultado = {
            "Distrito": distrito,
            "Concelho": concelho,
            "Inscritos": populacao,
        }

        resultado.update(votos)
        resultado.pop("Abstencao", None)

        # Guarda JSON
        filename = f"{concelho}.json"
        caminho = os.path.join("./ResultadoEleicoesDistritos/JSON", filename)
        with open(caminho, "w", encoding="utf-8") as jsonfile:
            json.dump(resultado, jsonfile, indent=2, ensure_ascii=False)

        # Guarda Excel
        filename_excel = f"{distrito}_{concelho}.xlsx"
        caminho_excel = os.path.join("./ResultadoEleicoesDistritos/XLSX", filename_excel)
        df_resultado = pd.DataFrame([resultado])
        df_resultado.to_excel(caminho_excel, index=False)

        print(f"Votos efetuados {distrito}_{concelho}")

    print("Votos concluídos!")

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
    caminho_excel = "./ResultadoEleicoesDistritos/XLSX"

    if not verificar_dados_existentes(caminho_excel):
        print("Operação cancelada!.")
        return

    lerdocs()

if __name__ == "__main__":
    main()
