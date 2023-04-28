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




def salvar_dict_para_csv(dicionario, arquivo): 

    # identificando produtos que já foram capturados
    set_url = set(dicionario['url']) 

    with open(arquivo, 'r', newline='', encoding='iso-8859-1') as arquivo_csv:
        leitor_csv = csv.DictReader(arquivo_csv)
        linhas_existentes = []

        for linha in leitor_csv:
            
            if not linha['url'] in set_url:
                print(f"A URL {url} existe no conjunto de URLs!", linha)
                # Atualiza a linha, se necessário
                linhas_existentes.append(linha)

    print(linhas_existentes)

    return

    # Lista das chaves do dicionário
    colunas = list(dicionario.keys())

    # Abre o arquivo CSV em modo de escrita
    with open(arquivo, 'w', newline='', encoding='iso-8859-1') as arquivo_csv:
        writer = csv.DictWriter(arquivo_csv, fieldnames=colunas, delimiter=';')
        
        # Escreve os cabeçalhos das colunas
        writer.writeheader()
        
        # Cria uma lista de listas com os valores do dicionário
        valores_colunas = list(dicionario.values())

        # Obtém o tamanho máximo das colunas
        tamanho_maximo = max(len(coluna) for coluna in valores_colunas)

        # Preenche as colunas com valores em branco para ter o mesmo tamanho
        valores_preenchidos = [coluna + [''] * (tamanho_maximo - len(coluna)) for coluna in valores_colunas]

        # Transpõe as colunas preenchidas
        colunas_preenchidas = zip(*valores_preenchidos)
        
        # Escreve os dados de cada coluna
        for coluna in colunas_preenchidas:
            coluna_convertida = [valor.encode('latin-1', 'ignore').decode('latin-1') if isinstance(valor, str) else valor for valor in coluna]
            writer.writerow(dict(zip(colunas, coluna_convertida)))
    
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

