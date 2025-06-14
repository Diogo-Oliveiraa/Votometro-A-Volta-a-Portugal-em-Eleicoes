"""Localizao do ficheiros no OS / Manipulação e análise de dados"""
import os
import pandas as pd

def ler_docs():
    """Verificação dos ficheiros dos Concelhos e Resultados"""
    caminho_concelhos = "./Docs/Distritos_Concelhos.xlsx"
    caminho_resultados = "./ResultadoEleicoesDistritos/XLSX"
    erros = []

    if not os.path.isfile(caminho_concelhos):
        erros.append(f"Ficheiro não encontrado: {caminho_concelhos}")

    if not os.path.isdir(caminho_resultados):
        erros.append(f"Pasta não encontrada: {caminho_resultados}")

    if erros:
        for erro in erros:
            print(erro)
        return False

    return caminho_concelhos, caminho_resultados

def criar_pasta():
    """ Criação da pasta ResultadosFinais para guardar o XLSX"""
    try:
        os.makedirs("./ResultadosFinais/", exist_ok=True)
        return True
    except OSError as e:
        print(f"Pasta não criada! {e}")
        return False

def ficheiros_por_nome_base(ficheiros, nome_base):
    """Filtra ficheiros que contenham o nome base (exato) no início do nome"""
    return [f for f in ficheiros if f.startswith(nome_base) and f.endswith(".xlsx")]

def validar_ficheiros(distritos_concelhos, caminho_resultados):
    """Confirma que existe apenas um ficheiro por Distrito/Concelho"""
    ficheiros = os.listdir(caminho_resultados)
    resultados_validados = []
    erros = []

    distritos = distritos_concelhos["Distrito"].unique() # Extrai apenas os Distritos do dataframe

    for distrito in distritos:
        concelhos_distrito = distritos_concelhos[distritos_concelhos["Distrito"] == distrito]
        distrito_ok = True  # Assume que tudo corre bem neste distrito

        for _, row in concelhos_distrito.iterrows():
            concelho = str(row["Concelho"]).strip()
            nome_base = f"{distrito}_{concelho}"

            ficheiros_encontrados = ficheiros_por_nome_base(ficheiros, nome_base)

            if len(ficheiros_encontrados) == 0:
                erros.append(f"Ficheiro em falta para: {nome_base}.xlsx")
                distrito_ok = False
            elif len(ficheiros_encontrados) > 1:
                erros.append(f"Vários ficheiros encontrados para: {nome_base} -> {ficheiros_encontrados}")
                distrito_ok = False
            else:
                caminho_ficheiro = os.path.join(caminho_resultados, ficheiros_encontrados[0])
                try:
                    df = pd.read_excel(caminho_ficheiro)
                    calcular_abstencao(df)
                    resultados_validados.append(df)
                except Exception as e:
                    erros.append(f"\033[31mErro ao processar {nome_base}: {e}\033[0m")
                    distrito_ok = False

        if distrito_ok:
            print(f"\033[32mValidação concluída {distrito}\033[0m")

    return resultados_validados, erros

def guardar_resultado_final(resultados_validados):
    """Guarda num único ficheiro Excel"""
    criar_pasta()
    caminho_saida = "./ResultadosFinais/VotosValidados.xlsx"
    df_final = pd.concat(resultados_validados, ignore_index=True)
    df_final.to_excel(caminho_saida, index=False)
    print(f"Ficheiro final guardado em: {caminho_saida}")

def calcular_abstencao(df):
    """Calcula abstenção por concelho/distrito"""
    colunas = list(df.columns)

    idx_adn = colunas.index("ADN")
    idx_brancos = colunas.index("Brancos")

    colunas_para_somar = colunas[idx_adn:idx_brancos + 1]
    total_votos = df[colunas_para_somar].sum(axis=1)

    df["Abtenção"] = df["Inscritos"] - total_votos

def main():
    """ Executa a leitura dos ficheiros, caso seja TRUE executa o resto do programa"""
    leitura_docs = ler_docs()

    if leitura_docs:
            caminho_concelhos, caminho_resultados = ler_docs()
            distritos_concelhos = pd.read_excel(caminho_concelhos)
            resultados_validados, documentos_erros = validar_ficheiros(distritos_concelhos, caminho_resultados)

            if documentos_erros:
                print("\033[31mErros encontrados durante a validação:\033[0m")
                for erro in documentos_erros:
                    print(erro)
            else:
                print("\033[32mTodos os ficheiros foram validados com sucesso.\033[0m")
                guardar_resultado_final(resultados_validados)

if __name__ == "__main__":
    print("A iniciar Validação...")
    main()
