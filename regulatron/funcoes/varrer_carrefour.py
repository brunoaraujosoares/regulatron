from funcoes.acessar_dados import *
from modelos.testar_palavras import *
from util.util import *
from driver.driver import *
from time import sleep

def varrer_carrefour(produtos_selecionados):
    print('varrer_carrefour', produtos_selecionados)
    return
    links = set()
    query = 'tv box'
    query = urllib.parse.quote(query)
    driver = get_driver()
    navigate_to_page(driver, f'https://www.carrefour.com.br/busca/{query}')
    sleep(3)

    ### descobrir a última página

    try:
        ultima_pagina = driver.find_elements(By.CLASS_NAME, 'carrefourbr-carrefour-components-0-x-Pagination_ItemsList')
        ultima_pagina = ultima_pagina[0].find_elements(By.TAG_NAME, 'a')
        ultima_pagina = ultima_pagina[-1].get_attribute('href') 
        ultima_pagina = int(ultima_pagina[ultima_pagina.find('=')+1:])

    except:
        ultima_pagina = 1

    for pagina in range(ultima_pagina):
        try:
            print('pesquisando página ', pagina+1, 'de', ultima_pagina)
            wait_for_element(driver, 'styles_iconpack', 5 )
            sleep(3)

            #descobrir os links dos produtos
            # grid_produtos = driver.find_elements(By.CLASS_NAME, 'carrefourbr-carrefour-components-0-x-gallery')
            # a_elements = grid_produtos[0].find_elements(By.TAG_NAME, 'a')
            a_elements = driver.find_elements(By.TAG_NAME, 'a')
            for element in a_elements:

                if element.get_attribute('href')[-2:] == '/p':
                    # print(element.get_attribute('href'))
                    links.add(element.get_attribute('href'))

            if pagina < ultima_pagina-1:
                navigate_to_page(driver, f'https://www.carrefour.com.br/busca/{query}?page={pagina+2}')
                
        except:
            pass
