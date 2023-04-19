from funcoes.acessar_dados import *
from funcoes.interfaces import *

# carrega o arquivo com os produtos para serem pesquisados nas plataformas
produtos = carregar_json('dados/produtos.json')

# exibe a interface
tela_inicial(produtos)