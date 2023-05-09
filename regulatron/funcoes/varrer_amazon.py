from funcoes.acessar_dados import *
from modelos.testar_palavras import *
from util.util import *
from driver.driver import *
from time import sleep

def varrer_amazon(produtos_selecionados):
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

        driver.get('https://www.amazon.com.br')
        sleep(3)

        search(driver = driver, query = chave_ext, element_id = 'twotabsearchtextbox')
        sleep(3)
        try:
            qtde_produto_pesquisado =  driver.find_element(
            By.CLASS_NAME,'a-spacing-top-small'
                ).get_attribute('innerText')

            posicao_aspa = qtde_produto_pesquisado.find('"')
            qtde_produto_pesquisado = qtde_produto_pesquisado[0:posicao_aspa-17].split(' ')[-1]
        except: 
            qtde_produto_pesquisado = 0

        if chave_ext in qtde_produtos: # se o produto já existe no dict
                qtde_produtos[chave_ext]['Amazon'] =  qtde_produto_pesquisado
        else:
            qtde_produtos[chave_ext] = {'Amazon' : qtde_produto_pesquisado }


        ## descobre a úlitim página 
        try:
            ultima_pagina = driver.find_elements(By.CLASS_NAME, 's-pagination-disabled')[1].get_attribute('innerHTML')
            ultima_pagina = int(ultima_pagina)
        except: 
            ultima_pagina = 1
            

        for pagina in range(ultima_pagina):
            if ( len(set_produtos) == limite_de_produtos ) and ( limite_de_produtos > 0 ) :
                break

            try:
                # print('pesquisando página ', pagina + 1, 'de', ultima_pagina)
                #descobrir os links dos produtos
                
                a_elements = driver.find_elements(By.CLASS_NAME, 'a-link-normal')
                # a_elements = a_elements.find_elements(By.TAG_NAME, 'a')
                for element in a_elements:
                    if ( len(set_produtos) == limite_de_produtos ) and ( limite_de_produtos > 0 ) :
                        break

                    link_produto = element.get_attribute('href').split('&qid=')[0]

                    if ('/gp/' in link_produto or '/dp/' in link_produto ) and ('bestsellers' not in link_produto or 'goldbox' not in link_produto):
                        set_produtos.add(link_produto)

                if pagina < ultima_pagina:
                    driver.find_elements(By.CLASS_NAME, 's-pagination-next')[0].click()
                    sleep(3)
                    
            except Exception as e:
                print(e)

        dict_produtos[chave_ext] = list(set_produtos)

    # salvar o resultado dos produtos
    salvar_json('dados/relatorio_produtos.json', qtde_produtos)

    capturar_detalhes_produtos_amazon(dict_produtos, driver)
    driver.quit()


def capturar_detalhes_produtos_amazon(dicionario, driver): 
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
                    titulo_produto = driver.find_element(By.ID, 'productTitle').text
                except:
                    titulo_produto = ''

                try:
                    id_vendedor    = driver.find_element(By.XPATH, '//*[@id="tabular-buybox"]/div[1]/div[6]/div').get_attribute('innerText')

                except:
                    try:
                         id_vendedor = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[3]/div[1]/div[8]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[3]/div/div[1]/form[1]/div/table/tbody/tr[2]/td[2]/span').get_attribute('innerText')

                    except:
                        id_vendedor    = ''

                try:      

                    inteiro = driver.find_element(By.CSS_SELECTOR,
                                                '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole'
                                                ).get_attribute('innerText').replace('\n', '')
                    fracao = driver.find_element(By.CSS_SELECTOR,
                                                '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-fraction'
                                                ).get_attribute('innerText')
                    print('corePriceDisplay_desktop_feature_div')

                    preco = f'{inteiro}{fracao}'

                except Exception as e:
                    
                    try: 
                      
                        inteiro = driver.find_element(By.CSS_SELECTOR,
                                                '#corePrice_feature_div > div > span.a-price.aok-align-center > span:nth-child(2) > span.a-price-whole'
                                                 ).get_attribute('innerText')
                        fracao =  driver.find_element(By.CSS_SELECTOR, 
                                                      '#corePrice_feature_div > div > span.a-price.aok-align-center > span:nth-child(2) > span.a-price-fraction'
                                                   ).get_attribute('innerText')
                      
                        print('corePrice_feature_div')
                        preco = f'{inteiro},{fracao}'
                      
                    except Exception as e:
                        print(e)

                        try:
                            preco = driver.find_element(By.ID, 'kindle-price-column').get_attribute('innerText')[2:]
                        except:
                            preco = ''


                try:
                    descricao = driver.find_element(By.ID, 'productDescription').text
                except:
                    try:
                        descricao = driver.find_element(By.ID, 'bookDescription_feature_div').text
                    except:
                        try:
                            descricao = driver.find_element(By.ID, 'prodDetails').text
                        except:
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
                dict_produtos['plataforma'].append('Amazon')
                dict_produtos['url'].append(item)
                # dict_produtos['modelo'].append(modelo)
            except:
                pass
         
    salvar_dict_para_csv(dict_produtos, 'dados/resultado_mercado_livre.csv')