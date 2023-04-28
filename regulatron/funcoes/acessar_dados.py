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
        with open(arquivo, 'r', encoding='iso-8859-1') as arq:
            dados = json.load(arq)
    else:
        dados = {}
 
    return dados


# def carregar_csv(arquivo):
#     """
#     Função responsável por carregar um arquivo CSV e 
#     retornar um dicionário com os dados contidos no
#     arquivo.

#     Args:
#     arquivo (str): caminho do arquivo CSV a ser
#     carregado.

#     Returns:
#     dict: dicionário contendo os dados do arquivo
#     JSON. Caso o arquivo não exista, retorna um
#     dicionário vazio.
#     """
    
#     if os.path.exists(arquivo):
#         with open(arquivo, 'r', encoding='iso-8859-1') as arq:
#             dados = json.load(arq)
#     else:
#         dados = {}
 
#     return dados

def salvar_json(arquivo, dados):
    with open(arquivo, 'w', encoding='iso-8859-1') as file:
        json.dump(dados, file)




def salvar_dict_para_csv(dicionario, arquivo_csv): 
    import pandas as pd

    df = pd.read_csv(arquivo_csv, sep=';', encoding='iso-8859-1')
    df = df.loc[ ~ df['url'].isin(dicionario['url']) ]
    df_novo = pd.DataFrame(dicionario)
    df = pd.concat([df_novo, df], ignore_index = True)
    df.to_csv(arquivo_csv, sep=';', encoding='iso-8859-1', index = False)

# # Exemplo de uso:
# dicionario = {
#     'produto_pesquisado': ['btv', 'tv'],
#     'titulo_produto': ['Fonte Bivolt 5v 2a Receptor Btv-b8 Btv-b9 Btv-b10 Btv-b11', 'TV LED 50"'],
#     'id_vendedor': ['', ''],
#     'preco': ['', ''],
#     'quantidade': [1, 2],
#     'descricao': ['', ''],
#     'homologado': ['CANDIDATO', ''],
#     'plataforma': ['Carrefour', ''],
#     'url': ['https://www.carrefour.com.br/fontebivolt5v2areceptorbtvb8btvb9btvb10btvb11-mp923947190/p', 'https://www.carrefour.com.br/tv-led-50-mp923947191/p']
# }

# arquivo_csv = 'dados.csv'
# adicionar_atualizar_linhas_csv(dicionario, arquivo_csv)

 
 
    # # Lista das chaves do dicionário
    # colunas = list(dicionario.keys())

    # # Abre o arquivo CSV em modo de escrita
    # with open(arquivo, 'w', newline='', encoding='iso-8859-1') as arquivo_csv:
    #     writer = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=';')
        
    #     # Escreve os cabeçalhos das colunas
    #     writer.writeheader()
        
    #     # Cria uma lista de listas com os valores do dicionário
    #     valores_colunas = list(dicionario.values())

    #     # Obtém o tamanho máximo das colunas
    #     tamanho_maximo = max(len(coluna) for coluna in valores_colunas)

    #     # Preenche as colunas com valores em branco para ter o mesmo tamanho
    #     valores_preenchidos = [coluna + [''] * (tamanho_maximo - len(coluna)) for coluna in valores_colunas]

    #     # Transpõe as colunas preenchidas
    #     colunas_preenchidas = zip(*valores_preenchidos)
        
    #     # Escreve os dados de cada coluna
    #     for coluna in colunas_preenchidas:
    #         coluna_convertida = [valor.encode('latin-1', 'ignore').decode('latin-1') if isinstance(valor, str) else valor for valor in coluna]
    #         writer.writerow(dict(zip(colunas, coluna_convertida)))
    
def carrega_produtos_capturados(arquivo):
    with open(arquivo, 'r', encoding='iso-8859-1') as file:
        reader = csv.reader(file, delimiter = ';')
        data = list(reader)
        data = data[1:]
    
    return data

# def salvar_dict_para_csv(dicionario, arquivo):
#     print(dicionario)
#     # Lista das chaves do dicionário
#     colunas = [ chave for chave in dicionario.keys() ]
#     # 'produto_pesquisado', 'titulo_produto', 'id_vendedor', 'preco', 'quantidade', 'descricao', 'homologado', 'url']
    
#     # Abre o arquivo CSV em modo de escrita
#     with open(arquivo, 'w', newline='', encoding='iso-8859-1') as arquivo_csv:
#         writer = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=';')
        
#         # Escreve os cabeçalhos das colunas
#         writer.writeheader()       
        
#         # Cria uma lista de listas com os valores do dicionário
#         valores = list(dicionario.values())
#         colunas = zip(*valores)

#         for coluna in colunas:
#             writer.writerow(list(coluna))

    
    # print(f'O arquivo CSV "{arquivo}" foi salvo com sucesso!')

