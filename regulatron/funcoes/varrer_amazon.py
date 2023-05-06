from funcoes.acessar_dados import *
from modelos.testar_palavras import *
from util.util import *
from driver.driver import *
from time import sleep

def varrer_amazon(produtos_selecionados):
    # carregar os produtos a serem pesquisados
    produtos_para_pesquisa = carregar_json('dados/produtos.json')

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


        links = set()
        driver.get('https://www.amazon.com.br')
        sleep(3)

        search(driver = driver, query = query, element_id = element_id)
        sleep(3)

        ## descobre a úlitim página 
        # <span class="s-pagination-item s-pagination-disabled" aria-disabled="true">7</span>
        try:
            ultima_pagina = driver.find_elements(By.CLASS_NAME, 's-pagination-disabled')[1].get_attribute('innerHTML')
            ultima_pagina = int(ultima_pagina)
        except: 
            ultima_pagina = 1
            

        for pagina in range(ultima_pagina):
            try:
                # print('pesquisando página ', pagina + 1, 'de', ultima_pagina)
                #descobrir os links dos produtos
                
                a_elements = driver.find_elements(By.CLASS_NAME, 'a-link-normal')
                # a_elements = a_elements.find_elements(By.TAG_NAME, 'a')
                for element in a_elements:
                    link_produto = element.get_attribute('href') 
        #             16,https://www.amazon.com.br/gp/goldbox/
        #             ,https://www.amazon.com.br/s?k=
                    if '/gp/' in link_produto:
                        pass
                    elif '/s?' in link_produto:
                        pass 
                    elif '/s/' in link_produto:
                        pass
                    elif '/b?' in link_produto:
                        pass
                    else:
                        links.add(link_produto)

                if pagina < ultima_pagina:
                    driver.find_elements(By.CLASS_NAME, 's-pagination-next')[0].click()
                    sleep(3)
                    
            except Exception as e:
                print(e)

        dict_produtos[chave_ext] = list(set_produtos)

    capturar_detalhes_produtos_amazon(dict_produtos, driver)
    driver.quit()



def capturar_detalhes_produtos_amazon(dict_produtos, driver): 
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
                    id_vendedor    = ''

                try:      

                    string = driver.find_element(By.CLASS_NAME, 'a-price-whole').get_attribute('innerText')
                    parte_numerica = re.findall(r'\d+', string)
                    parte_inteira = int(parte_numerica[0])
                    
                    string = driver.find_element(By.CLASS_NAME, 'a-price-fraction').get_attribute('innerText')
                    parte_numerica = re.findall(r'\d+', string)
                    parte_decimal = int(parte_numerica[0])

                    preco = float(f'{parte_inteira}.{parte_decimal}')
                    preco = '{:0.2f}'.format(preco).replace('.', ',') 

                except:
                    preco = ''

                try:
                    descricao = driver.find_element(By.ID, 'productDescription').text
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