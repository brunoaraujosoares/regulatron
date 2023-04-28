from funcoes.acessar_dados import *
from modelos.testar_palavras import *
from util.util import *
from driver.driver import *
from time import sleep
import urllib


def varrer_carrefour(produtos_selecionados):

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
    
        query = urllib.parse.quote(chave_ext)
        
        navigate_to_page(driver, f'https://www.carrefour.com.br/busca/{query}')
        sleep(tempo_de_espera)
    
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
            
            # navega até a página do produto
            driver.get(item)
            sleep(tempo_de_espera)

            #titulo
            #<span class="vtex-store-components-3-x-productBrand ">Suporte De Parede Para Btv 10/11 </span>
            #vendedor
            # <a href="/parceiro/olist" class="carrefourbr-carrefour-components-0-x-sellerLink">Olist</a>
            # preco
            # <span class="carrefourbr-carrefour-components-0-x-currencyContainer">
            # <span class="carrefourbr-carrefour-components-0-x-currencyCode">R$</span><span class="carrefourbr-carrefour-components-0-x-currencyLiteral">&nbsp;</span><span class="carrefourbr-carrefour-components-0-x-currencyInteger">39</span><span class="carrefourbr-carrefour-components-0-x-currencyDecimal">,</span><span class="carrefourbr-carrefour-components-0-x-currencyFraction">85</span></span>
            # descricao
            # <div class="vtex-store-components-3-x-productDescriptionContainer"><h2 class="vtex-store-components-3-x-productDescriptionTitle t-heading-5 mb5 mt0">Descrição do produto</h2><div class="vtex-store-components-3-x-productDescriptionText c-muted-1"><div style="display: contents;">Leia Toda A Descrição

            try:
                titulo_produto = driver.find_element(By.CLASS_NAME, 'vtex-store-components-3-x-productBrand').text
            except:
                titulo_produto = ''

            try:
                id_vendedor    = driver.find_element(By.XPATH, 'carrefourbr-carrefour-components-0-x-sellerLink').text
            except:
                id_vendedor    = ''

            try:        
                preco = driver.find_element(By.CLASS_NAME, 'carrefourbr-carrefour-components-0-x-currencyContainer').text
            except:
                preco = ''
                
            try:
                        #<div class="vtex-store-components-3-x-productDescriptionText c-muted-1"><div style="display: contents;">Fonte Bivolt 5v 2a Receptor Btv-b8 Btv-b9 Btv-b10 Btv-b11fonte Bivolt 5v 2a Receptor Btv-b8 Btv-b9 Btv-b10 Btv-b11 ==fonte De Energia Para Receptor Btv (substitui A Original) Com As Mesmas Características, Fonte Bivolt De Excelente Custo Beneficio.==funciona Nos Modelos:btv B8btv B9btv Bxbtv 10btv B11btv E9 Expressbtv E10 Express==tv Box 4k==tv Box Inova==tv Box Fullhdbtv B8btv B9btv Bxbtv 10btv E9 Express==características:voltagem:: Bivolt 110-220 Voutput: 5v/ 2a==potencia 10w Real==plug Conector P4==itens Inclusos01 - Fonte De Energia==produto Novo==imagem Ilustrativa==garantia 90 Dias==fabricantejs Technology==</div></div>
                        #<div style="display: contents;">Fonte Bivolt 5v 2a Receptor Btv-b8 Btv-b9 Btv-b10 Btv-b11fonte Bivolt 5v 2a Receptor Btv-b8 Btv-b9 Btv-b10 Btv-b11 ==fonte De Energia Para Receptor Btv (substitui A Original) Com As Mesmas Características, Fonte Bivolt De Excelente Custo Beneficio.==funciona Nos Modelos:btv B8btv B9btv Bxbtv 10btv B11btv E9 Expressbtv E10 Express==tv Box 4k==tv Box Inova==tv Box Fullhdbtv B8btv B9btv Bxbtv 10btv E9 Express==características:voltagem:: Bivolt 110-220 Voutput: 5v/ 2a==potencia 10w Real==plug Conector P4==itens Inclusos01 - Fonte De Energia==produto Novo==imagem Ilustrativa==garantia 90 Dias==fabricantejs Technology==</div>

                descricao      = driver.find_element(By.CLASS_NAME, 'vtex-store-components-3-x-productDescriptionText').text[0:500]
            except:
                descricao      = ''

            quantidade     = 1

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
            dict_produtos['plataforma'].append('Carrefour')
            dict_produtos['url'].append(item)
            # dict_produtos['modelo'].append(modelo)

    salvar_dict_para_csv(dict_produtos, 'dados/resultado_mercado_livre.csv')