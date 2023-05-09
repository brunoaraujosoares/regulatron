import os
import json
import csv

def carregar_json(arquivo):
    """
    Função responsável por carregar um arquivo JSON e 
    retornar um dicionário com os dados contidos no
    arquivo.

    Args:
    arquivo (str): caminho do arquivo JSON a ser
    carregado.

    Returns:
    dict: dicionário contendo os dados do arquivo
    JSON. Caso o arquivo não exista, retorna um
    dicionário vazio.
    """
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    else:
        dados = {}
 
    return dados

def salvar_json(arquivo, dados):
    with open(arquivo, 'w', encoding='utf-8') as file:
        json.dump(dados, file)


def salvar_dict_para_csv(dicionario, arquivo_csv): 
    import pandas as pd

    df = pd.read_csv(arquivo_csv, sep=';', encoding='utf-8')
    df = df.loc[ ~ df['url'].isin(dicionario['url']) ]
    df_novo = pd.DataFrame(dicionario)
    df = pd.concat([df_novo, df], ignore_index = True)
    
    try:
        df.to_csv(arquivo_csv, sep=';', encoding='utf-8', index = False)
    except Exception as e:
        print(e)

def carrega_produtos_capturados(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter = ';')
        data = list(reader)
        data = data[1:]
    
    return data


