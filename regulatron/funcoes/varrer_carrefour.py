from funcoes.acessar_dados import *
from modelos.testar_palavras import *
from util.util import *
from driver.driver import *
from time import sleep
import urllib
from bs4 import BeautifulSoup


def varrer_carrefour(produtos_selecionados):

    # carregar os produtos a serem pesquisados
    produtos_para_pesquisa = carregar_json('dados/produtos.json')
    qtde_produtos = carregar_json('dados/relatorio_produtos.json')

    # carregar configurações de tempo de espera e limite de produtos
    dados_configuracoes = carregar_json('dados/config.json')
    tempo_de_espera     = dados_configuracoes.get('tempo_de_espera')
    limite_de_produtos  = dados_configuracoes.get('limite_de_produtos')
    
    produtos_para_pesquisa = filter_dict_by_set_keys(produtos_para_pesquisa, produtos_selecionados)
    
    dict_produtos   = {}    # vai guardar todas as informações dos produtos
    set_produtos = set() # vai guardar os links dos produtos
    driver = get_driver()
    
    for chave_ext, valor_ext in produtos_para_pesquisa.items():
        
        yes_words = produtos_para_pesquisa[chave_ext]["yes-words"]
        no_words  = produtos_para_pesquisa[chave_ext]["no-words"]
        set_produtos = set() # vai guardar os links dos produtos
    
        query = urllib.parse.quote(chave_ext)
        
        navigate_to_page(driver, f'https://www.carrefour.com.br/busca/{query}')
        sleep(tempo_de_espera)


        qtde_produto_pesquisado =  driver.find_element(
                By.CLASS_NAME,'vtex-search-result-3-x-totalProducts--layout'
            ).get_attribute('innerText').split(' ')[0]
    

        if chave_ext in qtde_produtos: # se o produto já existe no dict
            qtde_produtos[chave_ext]['Carrefour'] =  qtde_produto_pesquisado

        else:
            qtde_produtos[chave_ext] = {'Carrefour' : qtde_produto_pesquisado }

    
    ### descobrir a última página

        try:
            ultima_pagina = driver.find_elements(By.CLASS_NAME, 'carrefourbr-carrefour-components-0-x-Pagination_ItemsList')
            ultima_pagina = ultima_pagina[0].find_elements(By.TAG_NAME, 'a')
            ultima_pagina = ultima_pagina[-1].get_attribute('href') 
            ultima_pagina = int(ultima_pagina[ultima_pagina.find('=')+1:])

        except:
            ultima_pagina = 1

        for pagina in range(ultima_pagina):
            if ( len(set_produtos) == limite_de_produtos ) and ( limite_de_produtos > 0 ) :
                break
            
            try:
                # print('pesquisando página ', pagina+1, 'de', ultima_pagina)
                wait_for_element(driver, 'styles_iconpack', 5 )
                # sleep(3)

                #descobrir os links dos produtos
                # grid_produtos = driver.find_elements(By.CLASS_NAME, 'carrefourbr-carrefour-components-0-x-gallery')
                # a_elements = grid_produtos[0].find_elements(By.TAG_NAME, 'a')
                a_elements = driver.find_elements(By.TAG_NAME, 'a')
                for element in a_elements:
                    if ( len(set_produtos) == limite_de_produtos ) and ( limite_de_produtos > 0 ) :
                        break

                    if element.get_attribute('href')[-2:] == '/p':
                        # print(element.get_attribute('href'))
                        set_produtos.add(element.get_attribute('href'))

                if pagina < ultima_pagina-1:
                    navigate_to_page(driver, f'https://www.carrefour.com.br/busca/{query}?page={pagina+2}')
                    
            except:
                pass

        dict_produtos[chave_ext] = list(set_produtos)

    # salvar o resultado dos produtos
    salvar_json('dados/relatorio_produtos.json', qtde_produtos)

    capturar_detalhes_produtos_carrefour(dict_produtos, driver)
    driver.quit()


def capturar_detalhes_produtos_carrefour(dicionario, driver):

    # carregar os produtos a serem pesquisados
    produtos_para_pesquisa = carregar_json('dados/produtos.json')

    # carregar configurações de tempo de espera e limite de produtos
    dados_configuracoes = carregar_json('dados/config.json')
    tempo_de_espera     = dados_configuracoes.get('tempo_de_espera')

    dict_produtos = { # vai guardar todas as informações dos produtos
        'produto_pesquisado' : [],
        'titulo_produto' : [],
        # 'marca' : marca,
        'id_vendedor': [],
        'preco': [],
        'quantidade': [],
        'descricao': [] ,
        'homologado': [],
        'plataforma' : [],
        'url' : []
        # 'quantidade_vendida':[]
        # modelo' : modelo
    }
    
    for chave in dicionario.keys():

        yes_words = produtos_para_pesquisa[chave]["yes-words"]
        no_words  = produtos_para_pesquisa[chave]["no-words"]

        for item in dicionario[chave]:
            try:
                # navega até a página do produto
                driver.get(item)
                sleep(tempo_de_espera)

                try:
                    titulo_produto = driver.find_element(
                                                        By.CLASS_NAME,
                                                        'vtex-store-components-3-x-productBrand'
                                                        ).get_attribute('innerHTML')
                    
                except Exception as e:
                    print(e)
                    titulo_produto = ''

                
                # <span class="carrefourbr-carrefour-components-0-x-carrefourSeller b f5">Carrefour</span>
                try:
                    try:
                        id_vendedor    = driver.find_element(
                                                            By.CLASS_NAME,
                                                            'carrefourbr-carrefour-components-0-x-carrefourSeller'
                                                            ).get_attribute('innerHTML')
                        
                    except:
                        id_vendedor    = driver.find_element(
                                                            By.CLASS_NAME,
                                                            'carrefourbr-carrefour-components-0-x-sellerLink'
                                                            ).get_attribute('href')
                        
                        id_vendedor = id_vendedor.split('/')[-1]
                except Exception as e:
                    print(e)
                    id_vendedor    = '##FALHOU##'

                try:        
                    inteiro = driver.find_element(
                                                By.CLASS_NAME,
                                                'carrefourbr-carrefour-components-0-x-currencyInteger'
                                                ).get_attribute('innerHTML')
                    
                    fracao  = driver.find_element(
                                                By.CLASS_NAME,
                                                'carrefourbr-carrefour-components-0-x-currencyFraction'
                                                ).get_attribute('innerHTML')
                    
                    preco   =  float(inteiro + '.' + fracao)
                    preco = '{:0.2f}'.format(preco).replace('.', ',')
                except Exception as e:
                    preco = ''
                    
                try:
                    driver.execute_script("window.scrollTo(0, 500);")
                    sleep(2)
                    descricao = driver.find_element(By.CLASS_NAME, 'vtex-store-components-3-x-productDescriptionText').get_attribute('innerHTML')[0:500]

                    # Criar um objeto BeautifulSoup a partir do HTML
                    soup = BeautifulSoup(descricao, 'html.parser')

                    # Remover todas as tags HTML e converte para latin-1
                    descricao = soup.get_text().strip()

                except Exception as e:
                    print(e)
                    descricao = ''

                quantidade = 1

                if testar_palavras(f'{titulo_produto} {descricao}', yes_words, no_words):
                    homologado = 'CANDIDATO'
                else:
                    homologado = ''
                
                dict_produtos['produto_pesquisado'].append(chave)
                dict_produtos['titulo_produto'].append(titulo_produto)
                # dict_produtos['marca'].append(marca)
                dict_produtos['id_vendedor'].append(id_vendedor)
                dict_produtos['preco'].append(preco)
                dict_produtos['quantidade'].append(quantidade)
                dict_produtos['descricao'].append(descricao)
                dict_produtos['homologado'].append(homologado)
                dict_produtos['plataforma'].append('Carrefour')
                dict_produtos['url'].append(item)
                # dict_produtos['modelo'].append(modelo)

            except:
                pass

    salvar_dict_para_csv(dict_produtos, 'dados/resultado_mercado_livre.csv')