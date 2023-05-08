from funcoes.acessar_dados import *
from modelos.testar_palavras import *
from util.util import *
from driver.driver import *
from time import sleep
import re

def varrer_mercado_livre(produtos_selecionados):

    # carregar os produtos a serem pesquisados
    produtos_para_pesquisa = carregar_json('dados/produtos.json')
    qtde_produtos = carregar_json('dados/relatorio_produtos.json')
    # print(qtde_produtos)

    # carregar configurações de tempo de espera e limite de produtos
    dados_configuracoes = carregar_json('dados/config.json')
    tempo_de_espera     = dados_configuracoes.get('tempo_de_espera')
    limite_de_produtos  = dados_configuracoes.get('limite_de_produtos')
    
    produtos_para_pesquisa = filter_dict_by_set_keys(produtos_para_pesquisa, produtos_selecionados)

    url = 'https://www.mercadolivre.com.br'
    query = ''
    element_id = 'cb1-edit'

    driver = get_driver() # abre o navegador

    dict_produtos   = {}    # vai guardar todas as informações dos produtos

    # varredura inicial: loop pelas chaves e valores do dicionário externo
    for chave_ext, valor_ext in produtos_para_pesquisa.items():
        # print(f"Produto pesquisado: {chave_ext}")


        yes_words = produtos_para_pesquisa[chave_ext]["yes-words"]
        no_words  = produtos_para_pesquisa[chave_ext]["no-words"]
        set_produtos = set() # vai guardar os links dos produtos

        navigate_to_page(driver, url)
        sleep(tempo_de_espera)


        if element_exists(driver, element_id):
            query = chave_ext
            search(driver, query, element_id)
            sleep(tempo_de_espera) # espera a lista de produtos carregar

            qtde_produto_pesquisado =  driver.find_element(
                    By.XPATH,'//*[@id="root-app"]/div/div[2]/aside/div[2]/span'
                ).get_attribute('innerHTML').split(' ')[0]

            if chave_ext in qtde_produtos: # se o produto já existe no dict
                    qtde_produtos[chave_ext]['Mercado Livre'] =  qtde_produto_pesquisado
            else:
                qtde_produtos[chave_ext] = {'Mercado Livre' : qtde_produto_pesquisado }
            
            try: 
                ultima_pagina = driver.find_element(By.CLASS_NAME,'andes-pagination__page-count').get_attribute('innerHTML')
                padrao = r"<!-- -->(\d+)"
                resultado = re.search(padrao, ultima_pagina)

                if resultado:
                    ultima_pagina = int(resultado.group(1))

            except:
                ultima_pagina = 1

            for i in range(ultima_pagina):
                if ( len(set_produtos) == limite_de_produtos ) and ( limite_de_produtos > 0 ) :
                    break

                # print('pesquisando página ', i+1, 'de', ultima_pagina, 'para', chave_ext)

                # salva todos os links em uma lista
                urls_produtos = driver.find_elements(By.TAG_NAME, "a")

                for item in urls_produtos:
                    if ( len(set_produtos) == limite_de_produtos ) and ( limite_de_produtos > 0 ) :
                        break
                    
                    if 'produto' in item.get_attribute("href"):

                        set_produtos.add( item.get_attribute("href") )

                # clicar na próxima página 
                try: 
                    link_proxima_pagina = driver.find_element(By.LINK_TEXT, 'Seguinte')
                    driver.execute_script("arguments[0].click();", link_proxima_pagina)            
                    sleep(tempo_de_espera)           

                except Exception as e:
                    pass

            dict_produtos[chave_ext] = list(set_produtos)

    # salvar o resultado dos produtos
    salvar_json('dados/relatorio_produtos.json', qtde_produtos)

    capturar_detalhes_produtos(dict_produtos, driver)
    driver.quit()
    


def capturar_detalhes_produtos(dicionario, driver):
    """
    1. Navega pelos links dos produtos coletados na varredura inicial,
    captura os atributos dos produtos grava em um csv com as seguintes colunas:

        produto_pesquisado: a palavra-chave do produto pesquisado
        titulo_produto : título do produto, conforme aparece no mercado livre

        # marca: ainda não disponível nesta versão
        id_vendedor : id do vendedor no mercado livre
        preco : preço do produto
        quantidade : quantidade disponível no momento da varredura
        homologado: informa se o produto é candidato a ser um produto de interesse        
        descricao : 500 primeiros caracteres da descrição do produto no mercado livre
        # modelo : ainda não disponível nesta versão
        url : endereço url do produto
        plataforma : 'Mercado Livre' servirá para identificar a origem do produto

    Args:
        dicionario (dict): O dicionário dos produtos coletados na varredura inicial 
        driver (webdriver): a instância o navegador autônomo
        
    """

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
            
            # navega até a página do produto
            driver.get(item)
            sleep(tempo_de_espera)
            
            try:
                titulo_produto = driver.find_element(By.CLASS_NAME, 'ui-pdp-title').text
            except:
                titulo_produto = ''

            try:
                id_vendedor    = driver.find_element(By.XPATH, '//*[@id="seller_info"]/div/a').get_attribute('href')
                id_vendedor    = id_vendedor.split('/')[-1]
                
            except:
                id_vendedor    = ''

            try:        
                preco = driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
                try:
                    preco = float(preco + '.' + driver.find_element(By.CLASS_NAME, 'andes-money-amount__cents').text)
                    preco = '{:0.2f}'.format(preco).replace('.', ',')                    
                except:
                    pass

            except:
                preco = ''
                
            try:
                descricao      = driver.find_element(By.CLASS_NAME, 'ui-pdp-description__content').text[0:500]
            except:
                descricao      = ''

            # <span class="ui-pdp-buybox__quantity__available">(8 disponíveis)</span>
            try:
                quantidade     = driver.find_element(By.CLASS_NAME, 'ui-pdp-buybox__quantity__available').text
                padrao = r'\((\d+)\s+\w+\)'
                match = re.search(padrao, quantidade)

                if match:
                    quantidade = int(match.group(1))

                else:
                    quantidade = 1 
            except Exception as e:
                # print(e)
                quantidade     = 1

            # # <strong class="ui-pdp-seller__sales-description">+100</strong>
            # try:
            #     quantidade_vendida     = driver.find_element(By.CLASS_NAME, 'ui-pdp-seller__sales-description').text
            #     padrao = r'\((\d+)\s+\w+\)'
            #     match = re.search(padrao, quantidade_vendida)

            #     if match:
            #         quantidade_vendida = int(match.group(1))

            #     else:
            #         quantidade_vendida = 1 
            # except Exception as e:
            #     print(e)
            #     quantidade_vendida     = -1 

            if testar_palavras(titulo_produto + ' ' + descricao, yes_words, no_words):
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
            dict_produtos['plataforma'].append('Mercado Livre')
            dict_produtos['url'].append(item)
            # dict_produtos['modelo'].append(modelo)

    
    salvar_dict_para_csv(dict_produtos, 'dados/resultado_mercado_livre.csv')


def relatorio_meracdo_livre(produtos):
    # carregar configurações de tempo de espera e limite de produtos
    dados_configuracoes = carregar_json('dados/config.json')
    tempo_de_espera     = dados_configuracoes.get('tempo_de_espera')

    # #driver = get_driver() # abre o navegador

    # for chave in produtos.keys():
    #     # pega ML
    #     navigate_to_page(driver, 'https://www.mercadolivre.com.br')
    #     sleep(tempo_de_espera)
    #     search(driver, query, element_id)
    #     sleep(tempo_de_espera)
    #     # pega a quantidade de produtos


    #     # pega carrfour


    #     # pega amazon


    #     # pega shopee


    # driver.close()
    return

