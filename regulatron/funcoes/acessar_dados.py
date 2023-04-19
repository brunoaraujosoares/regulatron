### Carregar Produtos

def carregar_json(arquivo):
    """
    Retorna um dict com os produtos a serem pesquisados
    """
    import os
    import json
    
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as arq:
            dados = json.load(arq,  )
    else:
        dados = {}
 
    return dados