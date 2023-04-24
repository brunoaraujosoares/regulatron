import os
import json

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
    with open(arquivo, 'w') as file:
        json.dump(dados, file)