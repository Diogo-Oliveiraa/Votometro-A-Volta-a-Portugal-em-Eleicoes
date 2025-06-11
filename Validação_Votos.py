import os
import pandas as pd

# Caminhos
CAMINHO_CONCELHOS = "./Docs/Distritos_Concelhos.xlsx"
CAMINHO_RESULTADOS = "./ResultadoEleicoesDistritos/XLSX"
CAMINHO_SAIDA = "./ResultadosFinais/VotosValidados.xlsx"

def ficheiros_por_nome_base(ficheiros, nome_base):
    """Filtra ficheiros que contenham o nome base (exato) no início do nome"""
    return [f for f in ficheiros if f.startswith(nome_base) and f.endswith(".xlsx")]

def validar_ficheiros(distritos_concelhos):
    ficheiros = os.listdir(CAMINHO_RESULTADOS)
    resultados_validados = []
    erros = []

    for _, row in distritos_concelhos.iterrows():
        distrito = str(row["Distrito"]).strip()
        concelho = str(row["Concelho"]).strip()
        nome_base = f"{distrito}_{concelho}"

        ficheiros_encontrados = ficheiros_por_nome_base(ficheiros, nome_base)

        if len(ficheiros_encontrados) == 0:
            erros.append(f"❌ Ficheiro em falta para: {nome_base}.xlsx")
        elif len(ficheiros_encontrados) > 1:
            erros.append(f"❌ Vários ficheiros encontrados para: {nome_base} -> {ficheiros_encontrados}")
        else:
            caminho_ficheiro = os.path.join(CAMINHO_RESULTADOS, ficheiros_encontrados[0])
            df = pd.read_excel(caminho_ficheiro)
            resultados_validados.append(df)

    return resultados_validados, erros

def guardar_resultado_final(resultados_validados):
    """Guarda todos os resultados num único ficheiro Excel"""
    df_final = pd.concat(resultados_validados, ignore_index=True)
    df_final.to_excel(CAMINHO_SAIDA, index=False)
    print(f"Ficheiro final guardado em: {CAMINHO_SAIDA}")

def main():
    distritos_concelhos = pd.read_excel(CAMINHO_CONCELHOS)
    resultados_validados, erros = validar_ficheiros(distritos_concelhos)

    if erros:
        print("Erros encontrados durante a validação:")
        for erro in erros:
            print(erro)
    else:
        print("Todos os ficheiros foram validados com sucesso.")

    if resultados_validados:
        guardar_resultado_final(resultados_validados)
    else:
        print("Nenhum resultado foi validado com sucesso.")

if __name__ == "__main__":
    main()