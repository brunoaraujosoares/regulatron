import PySimpleGUI as sg
from funcoes.acessar_dados import *
from funcoes.varrer_mercado_livre import *
from funcoes.varrer_carrefour import *
from funcoes.varrer_amazon import *
from funcoes.varrer_shopee import *

def tela_inicial(): 

    """
    Exibe a tela inicial do programa. 
    
    A tela exibe uma lista de produtos para pesquisa, com 
    caixas de seleção para marcar os produtos desejados.
    Além disso, há botões para adicionar, editar e excluir produtos,
    bem como um botão para avançar para a próxima tela.
    
    A função também permite configurar as opções do sistema,
    como tempo de espera e limite de produtos pesquisados. 

    Argumentos:
    - produtos_para_pesquisa: lista de produtos a serem exibidos na tela inicial.

    Retorno:
    - Não há retorno, mas a função exibe a tela inicial do programa.
    """
    
    # layout
    sg.theme("black")
    
    texto_principal  = 'Escolha produtos para pesquisar:'
    font_principal = ('Arial', 18)
    font_secundario = ('Arial', 12)
    texto_secundario = 'Marque as  caixas de seleção para incluir os produtos na pesquisa.'
    texto_terciario  = 'Clique no produto para editar os critérios de pesquisa ou para excluir.'

    # carregar as variaveis do sistema 
    # (arquivo: dados/config.json):
    #   - tempo_de_espera:
    #    tempo que o navegaodr espera para pesquisar os elementos na página,
    #    ou para carregar a página seguinte
    #   - limite_de_produtos:
    #    quantidade de produtos a serem salvos na base 
    #    (arquivo: dados/resultados.csv) 
    #    obs.: os arquivos carregados podem não corresponder aos arquivos
    #    pesquisados pelo webscrap

    dados = carregar_json('dados/config.json')
    tempo_de_espera    = dados.get('tempo_de_espera')
    limite_de_produtos = dados.get('limite_de_produtos')
    
    dados_produtos = carregar_json('dados/produtos.json')
    conteudo_da_coluna = []

    # Adicionar as caixas de seleções dos produtos
    for chave in dados_produtos.keys():
        conteudo_da_coluna.append([ sg.Checkbox(
                            chave,
                            key=chave,
                            default = False,
                            size=(30,1))
                       ])
    coluna = sg.Column(conteudo_da_coluna, element_justification="l", size = (1000,400), background_color='lightgray')
    
    col1=[[ sg.Image( 'logo_pequeno.png'), sg.Text(' '*120)]]
    col2=[
            [ sg.Button('Treinar Modelo')],
            [ sg.Button('Configurações') ]
         ]
    col3 = [ [sg.Column([
            [ coluna ]
            ], background_color='lightgray', pad=(0,5))] ]

    # Define as configurações da janela
    config = {
        'background_color': 'lightgray',
        'font': ('Helvetica', 12),
        'size': (400, 200),
        'element_padding': (10, 10)
    }

    layout = [
        [ [sg.Column(col1, element_justification='left' ), sg.Column(col2, element_justification='right')] ],
        [ sg.Text( texto_principal, font = font_principal) ],
        [],
                [ [sg.Column(col3, element_justification='left' )] ],
        [  
            # botões 
            sg.Button('Adicionar Produto'),
            sg.Button('Editar'),
            sg.Button('Excluir'),
            sg.Button('Relatório de pesquisas'),
            sg.Text(' '*80),
            sg.Button('Exibir Produtos Capturados'),
            sg.Button('Avançar >>')
        ]
    ]
        
    # Cria a janela do programa
    window = sg.Window('REGULATRON - Versão beta 0.2', 
                       layout, 
                       element_justification='left',
                       size=(1024, 600) #, **config
                      )

    # Loop ===================================================================
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED : 
            break    
        
        
        if event == 'Treinar Modelo':  # Treinar Modelo # ===================
            sg.popup('BREVE DISPONÍVEL')
        
        if event == 'Exibir Produtos Capturados':  # Treinar Modelo # ===================
            window.close()
            listar_produtos_capturados()   


        if event == 'Avançar >>': # Avançar >> ==========================
            produtos_selecionados = [k for k, v in values.items() if v]

            if len(produtos_selecionados) == 0: # testa se há algum produto foi selecionado
                sg.popup('Nenhum produto foi selecionado')
            
            else:
                window.close()
                escolher_plataformas(produtos_selecionados)
        

        if event == 'Editar':  # Editar produto # ===========================
            
            produtos_selecionados = [k for k, v in values.items() if v]


            if len(produtos_selecionados) == 0: # testa se há algum produto foi selecionado
                sg.popup('Nenhum produto foi selecionado')
            
            elif len(produtos_selecionados) > 1:
                sg.popup('Só é possível editar um produto por vez.')

            else: # pegar o produto selecionado
                editar_produto(window, produtos_selecionados[0])
    

        if event == 'Excluir':  # Excluir produtos # ===========================
            
            # testa se há checks selecionados
            produtos_selecionados = set([k for k, v in values.items() if v])
            if len(produtos_selecionados) == 0:
                sg.popup('Nenhum produto foi selecionado')
            
            else:

                confirm = sg.popup_yes_no('Deseja excluir os produtos selecionados?')
                if confirm == 'Yes':

                    for item in produtos_selecionados:
                        del dados_produtos[item]    
                    
                    salvar_json('dados/produtos.json', dados_produtos)
                    
                    window.close()
                    tela_inicial()

        if event == 'Configurações':  # painel de Configurações # ===========================
            try:

                # Criar uma janela de edição        
                edit_config_layout = [
                    [
                        sg.Text('Tempo de Espera:'),
                        sg.InputText(tempo_de_espera, key='tempo_de_espera', size=(5,1)),
                        sg.Text('segundos'),
                    ],
                    [
                        sg.Text('Limite de produtos pesquisados:'),
                        sg.InputText(limite_de_produtos,
                        key='limite_de_produtos' , size=(5,1)), sg.Button('Salvar', key='-SAVE-')]
                ]

                edit_config_window = sg.Window('Configurações do sistema', 
                                                edit_config_layout,
                                                element_justification='left',
                                                size=(400, 100)
                                                )

                # Loop de eventos da janela de edição
                while True:
                    edit_config_event, edit_config_window_values = edit_config_window.read()

                    if edit_config_event == sg.WINDOW_CLOSED:
                        break

                    elif edit_config_event == '-SAVE-':
                        tempo_de_espera = edit_config_window_values['tempo_de_espera']
                        limite_de_produtos = edit_config_window_values['limite_de_produtos']
                        
                        e = 0

                        try:
                            tempo_de_espera = int(tempo_de_espera)
                        except:
                            sg.popup('Digite um valor numérico para o Tempo de Espera.')
                            e+=1

                        try:
                            limite_de_produtos = int(limite_de_produtos)
                        except:
                            sg.popup('Digite um valor numérico para o Limite de Produtos.')
                            e+=1

                        if e == 0:
                            ## salva 
                            dict_config = { "tempo_de_espera" : tempo_de_espera, "limite_de_produtos" : limite_de_produtos }
                            salvar_json('dados/config.json', dict_config)
                            break
                
                edit_config_window.close()

            except Exception as e:
                print(e)

            pass
        
        if event == 'Adicionar Produto':
            adicionar_produto(window)

        if event == 'Relatório de pesquisas':
            relatorio_de_pesquisa()

    window.close()
    
    # fim da tela inicial


def  relatorio_de_pesquisa():
    import os
    import datetime

    # Obtém o tempo de criação do arquivo em formato de timestamp
    timestamp = os.path.getmtime('dados/relatorio_produtos.json')

    # Converte o timestamp para o formato de data e hora
    data_hora_criacao = datetime.datetime.fromtimestamp(timestamp)
    data_hora_criacao = data_hora_criacao.strftime("%d/%m/%Y %H:%M")
    
    dados_produtos = carregar_json('dados/relatorio_produtos.json')

    cabecalho = ['Produto', 'Mercado Livre', 'Carrefour', 'Amazon', 'Shopee']
    tabela = [cabecalho]  # Inicia a tabela com o cabeçalho

    # preenche a tabela
    for produto, dict_qtde in dados_produtos.items():
        linha = [produto]  # Adiciona o nome do produto na primeira coluna
        for plataforma in cabecalho[1:]:
            try:
                linha.append(dict_qtde[plataforma])  # Adiciona as quantidades para cada plataforma
            except:
                linha.append('-')
        tabela.append(linha)  # Adiciona a linha à tabela


    # Definição do layout
    layout = [
        [sg.Table(values=tabela[1:],
                headings=['Produto', 'Qtde ML', 'Qtde Carrefour', 'Qtde Amazon', 'Qtde Shopee'],
                justification='center',
                auto_size_columns=True,
                num_rows=10,
                key='-TABLE-')],
        [ sg.Text( f'Resultados atualizados em: {data_hora_criacao}') ]
    ]

    # Criação da janela
    janela = sg.Window('Relatório de produtos pesquisados', layout)

    # Loop de eventos
    while True:
        evento, valores = janela.read()
        if evento == sg.WINDOW_CLOSED:
            break

    # Fechamento da janela
    janela.close()
    
    return 


   

def editar_produto(janela, produto):

    dados_produtos = carregar_json('dados/produtos.json')
    produto_dict = dados_produtos[produto]

    # pegar o produto a partir do dict
    yes_words = ",".join(produto_dict["yes-words"])
    no_words = ",".join(produto_dict["no-words"])

    # Criar uma janela de edição        
    # layout_edit = [
    #     [sg.Text('Nome do produto:'), sg.InputText(produto, key='nome')],
    #     [sg.Text('Black List (separadas por vírgula):'), sg.InputText(yes_words, key='yes-words')],
    #     [sg.Text('White List (separadas por vírgula):'), sg.InputText(no_words, key='no-words')],
    #     [sg.Button('Salvar', key='-SAVE-'), sg.Button('Cancelar')]
    # ]

    layout_edit = [
        [sg.Text('Nome do produto:        '), sg.InputText(produto, key='nome')],
        [sg.Text('Black List \n(separadas por vírgula):\n \n \n \n'), sg.Multiline(default_text=yes_words, key='yes-words', size=(60,7))],
        [sg.Text('White List \n(separadas por vírgula): \n \n \n \n'), sg.Multiline(default_text=no_words, key='no-words', size=(60,7))],
        [sg.Text(' '*110), sg.Button('Salvar', key='-SAVE-'), sg.Button('Cancelar')]
]

    window_edit = sg.Window('Editar produto', layout_edit,  size=(600, 330))

    # Loop de eventos da janela de edição
    while True:
        event_edit, values_edit = window_edit.read()

        if event_edit == sg.WINDOW_CLOSED or event_edit == 'Cancelar':                
            break

        elif event_edit == '-SAVE-':

            del dados_produtos[produto]
            nome = values_edit['nome']
            dados_produtos[nome] = {
                'yes-words': values_edit['yes-words'].split(','),
                'no-words' : values_edit['no-words'].split(',')
            }

            # print(dados_produtos)
            salvar_json('dados/produtos.json', dados_produtos)
            window_edit.close()
            janela.close()
            tela_inicial()
            

    window_edit.close()

def adicionar_produto(janela):

    # código para adicionar um novo produto

    layout_add = [ # Define o layout da janela para adicionar um novo registro
        [sg.Text('Nome do produto:'), sg.Input(key='nome')],
        [sg.Text('yes-words (separadas por vírgula):'), sg.Input(key='yes-words')],
        [sg.Text('no-words (separadas por vírgula):'), sg.Input(key='no-words')],
        [sg.Button('Adicionar'), sg.Button('Cancelar')]
    ]

    # Cria a janela
    window_add = sg.Window('Novo produto', layout_add)

    # Loop de eventos
    while True:
        event_add, values_add = window_add.read()

        if event_add == sg.WINDOW_CLOSED or event_add == 'Cancelar':
            break

        elif event_add == 'Adicionar':
            dados_produtos = carregar_json('dados/produtos.json')

            nome = values_add['nome']
            dados_produtos[nome] = {
                'yes-words': values_add['yes-words'].split(','),
                'no-words': values_add['no-words'].split(',')
            }

            salvar_json('dados/produtos.json', dados_produtos)

            window_add.close()
            janela.close()
            tela_inicial()
            
    window_add.close()

# fim da tela inicial ================================================================

def escolher_plataformas(produtos_selecionados):

    # layout
    sg.theme("black")

    texto_principal  = 'Escolha as plataforma para pesquisar:'
    font_principal   = ('Arial', 18)
    font_secundario  = ('Arial', 12)
    font_terciario   = ('Arial', 10)
    texto_secundario = 'Atenção! Varrer múltiplas plataformas pode levar muito tempo.'
    texto_terciario  = 'Marque as caixas de seleção para pesquisar nas plataformas.'

    dados = carregar_json('dados/config.json')
    tempo_de_espera    = dados.get('tempo_de_espera')
    limite_de_produtos = dados.get('limite_de_produtos')
    
    dados_produtos = carregar_json('dados/produtos.json')


    conteudo_da_coluna = []

    # Adicionar as caixas de seleções das plataformas
    conteudo_da_coluna.append([ sg.Checkbox(
                            'Mercado Livre',
                            key='MERCADOLIVRE',
                            default = False,
                            size=(119,1))
                       ])

    conteudo_da_coluna.append([ sg.Checkbox(
                            'Carrefour',
                            key='CARREFOUR',
                            default = False,
                            size=(119,1))
                       ])


    conteudo_da_coluna.append([ sg.Checkbox(
                            'Amazon',
                            key='AMAZON',
                            default = False,
                            size=(119,1))
                       ])
    
    conteudo_da_coluna.append([ sg.Checkbox(
                            'Shopee',
                            key='SHOPEE',
                            default = False,
                            size=(119,1))
                       ])

    coluna = sg.Column(conteudo_da_coluna, element_justification="l", size = (1000,376), background_color='lightgray')

    layout = [
            [ [ sg.Image( 'logo_pequeno.png'), sg.Text(' '*120)],
            [ sg.Text( texto_principal, font = font_principal) ],
            [ sg.Text( texto_terciario, font = font_terciario) ],
            [ sg.Text( texto_secundario, font = font_secundario) ],
            [],
            [ coluna ],
            [
                # botões 
                sg.Button('<< Voltar à tela inicial'),
                sg.Text(' '*175),
                sg.Button('Iniciar Varredura >>')
            ]
        ]
    ]
        
    # Cria a janela do programa
    window = sg.Window('REGULATRON - Versão beta 0.2', 
                       layout, 
                       element_justification='left',
                       size=(1024, 600) #, **config
                      )

    # Loop ===================================================================
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED : 
            break    

        if event == '<< Voltar à tela inicial':
            window.close()
            tela_inicial()

        if event == 'Iniciar Varredura >>':
            ## pegar as plataformas selecionadas
            plataformas_selecionadas = set( [ k for k, v in values.items() if v ] )
            if len(plataformas_selecionadas) == 0:
                sg.popup('Nenhuma plataforma foi selecionada')
            
            else:
            
                if 'MERCADOLIVRE' in plataformas_selecionadas:
                    varrer_mercado_livre(produtos_selecionados)

                if 'CARREFOUR' in plataformas_selecionadas:
                    varrer_carrefour(produtos_selecionados)

                if 'AMAZON' in plataformas_selecionadas:
                    varrer_amazon(produtos_selecionados)

                if 'SHOPEE' in plataformas_selecionadas:
                    varrer_shopee(produtos_selecionados)

                window.close()
                listar_produtos_capturados()

    window.close()
    
# fim da tela de escolher plataformas ===================================


def listar_produtos_capturados():
    import pandas as pd

    data = carrega_produtos_capturados('dados/resultado_mercado_livre.csv')
   
    sg.theme('Black')

    texto_principal = 'Produtos Capturados'
    font_principal = ("Arial", 24)
    font_selecao   = ("Arial", 16)

    subtotal_produtos   = resultados_exibidos   = len(data)
    subtotal_candidados = resultados_candidados = sum(1 for elemento in data if 'CANDIDATO' in elemento)
    
    df = pd.read_csv('dados/resultado_mercado_livre.csv', sep=';', encoding = 'utf-8')
    quantidade_mercado_livre = df.loc[df['plataforma'] == 'Mercado Livre']['quantidade'].sum()


    plataformas = ['Todas', 'Mercado Livre', 'Carrefour']
    # produtos = ['Todos','btv','celular','flipper zero', 'tv_box']
    produtos = carregar_json('dados/produtos.json')
    lista = ['Todos']
    lista.extend(list(produtos.keys()))
    produtos = lista

    # Definindo o layout da janela
    layout = [
                # primeira linha
                [sg.Column(
                    [[ sg.Text(texto_principal, font = font_principal, justification="l") ]],
                    size=(600, 50)
                ), 
                sg.Column(
                    [
    #                      [ sg.Text(f'Total de produtos em todas as plataformas: {total_produtos}') ],
    #                      [ sg.Text(f'Produtos Candidatos: {total_candidados}') ]
                    ])
                ],
    #             [
    #                 sg.Text('-'* 250)
    #             ],
                # segunda linha
                [sg.Column([
                    [   
                        sg.Text('Palataforma: '),
                        sg.Combo(plataformas, default_value='Todas', size = (26, None) )
                    ],
                    [
                        sg.Text(f'Subotal de produtos: ', size = (28, None) ),
                        sg.Input(subtotal_produtos, key = 'subtotal_produtos', size = (7,None), justification='r')
                    ],
                    [
                        sg.Text(f'Subtotal de Produtos Candidatos: ', size = (28, None) ) ,
                        sg.Input(subtotal_candidados, key = 'subtotal_candidados', size = (7,None), justification='r'),
                    ]
                    
                ],
                    size=(305, 85), background_color = 'white'
                ), 
                sg.Column(
                    
                    [
                        [ sg.Text(f'Termo pesquisado: '),
                        sg.Combo(produtos, default_value='Todos', size = (21, None)  )
                        ],
                        [ sg.Text(f'Resultados exibidos na plataforma:', size = (28, None) ),
                        sg.Input(resultados_exibidos, key = 'resultados_exibidos', size = (7,None), justification='r')
                        ],
                        [ sg.Text(f'Produtos candidatos:' , size = (28, None) ),
                        sg.Input(resultados_candidados, key='resultados_candidados', size = (7,None), justification='r')
                        ]
                        
                    ],size=(305, 85), background_color = 'white'),
                sg.Column(
                    
                    [
                        [ sg.Text(f'Mercado Livre: ')
                        
                        ],
                        [ sg.Text(f'Quantidade de produtos disponíveis:', size = (28, None) ),
                        sg.Input(quantidade_mercado_livre, key = 'quantidade_mercado_livre', size = (7,None), justification='r')
                        ] #,
                        # [ sg.Text(f'Quantidade de produtos vendidos:' , size = (28, None) ),
                        # sg.Input('10000000', key='quantidade_vendidos', size = (7,None), justification='r')
                        # ]
                        
                    ],size=(305, 85), background_color = 'white'),
                ],

        
                [
                    sg.Table(
                        values=data,
                        
                        headings=[
                                'produto',
                                'titulo',
                                'vendedor',
                                'preço',
                                'qtd',
                                'descricao',
                                'homologado',
                                'plataforma',
                                'url'
                                ],
                        key='-TABLE-',
                        enable_events=True,
                        auto_size_columns=False,
                        num_rows=24,
                        justification='left',
                        col_widths=[10, 30, 12, 7, 5, 15, 10,9,10]
                        # display_row_numbers = True,
                    )
                ],

        
                [
                    sg.Button('<< voltar à tela inicial'),
                    sg.Button('Editar produto', key='-EDITAR-', disabled=True),
                    sg.Button('ver página do produto', key='-ACESSAR-', disabled=True)
                ]
            ]

    # Criando a janela
    window = sg.Window("Regulatron Beta", layout, size=(1024, 600))

    # Loop para processar eventos
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == '<< voltar à tela inicial':
           window.close()
           tela_inicial()

        if event == '-TABLE-':
            try:
                row_index = window['-TABLE-'].get()[0]
                window['-EDITAR-'].update(disabled=False)
                window['-ACESSAR-'].update(disabled=False)
            except:
                pass
                #window['-ERROR-'].update('Selecione um produto para editar ou remover')

        if event == '-EDITAR-': 
    #        try:

            # Obter a linha selecionada na tabela
            selected_row = values['-TABLE-']

            if selected_row != []:

                selected_row = values['-TABLE-'][0]

                # código para editar o produto selecionado

                # Criar uma janela de edição        
                edit_layout = [
                    [ sg.Text('Editando produto:', font=font_principal) ],
                    [ sg.Text(data[selected_row][1][:30], font=font_selecao) ],
                    [ sg.Text('Termo pesquisado:', font=font_selecao), sg.Text(data[selected_row][0] , font=font_selecao) ],
                    [ sg.Text("-"*20) ],
                    [ sg.Button('HOMOLOGADO'), sg.Button('NÃO HOMOLOGADO'), sg.Button('NÃO APLICÁVEL') , sg.Button('Cancelar') ],
                    [ sg.Text('* Marcar "NÃO APLICÁVEL" se o produto não corresponde ao termo pesquisado') ]
                ]

                edit_window = sg.Window('Editar linha', edit_layout, element_justification="c")

                # Loop de eventos da janela de edição
                while True:
                    edit_event, edit_values = edit_window.read()

                    if edit_event == sg.WINDOW_CLOSED or edit_event == 'Cancelar':   
                        edit_window.close()
                        break 

                    elif edit_event == 'HOMOLOGADO' or edit_event == 'NÃO HOMOLOGADO' or edit_event == 'NÃO APLICÁVEL':
                        import pandas as pd # todo --- fazer salvar em csv  #########################################

                        selected_row = values['-TABLE-']
                        if selected_row != []:
                            selected_row = values['-TABLE-'][0]
                            url = data[selected_row][8]
                        
                            df_temp = pd.read_csv('dados/resultado_mercado_livre.csv', encoding = 'utf-8', sep = ';')
                            df_temp.loc[df_temp['url'] == url, 'homologado'] = edit_event
                            
                            df_temp.to_csv('dados/resultado_mercado_livre.csv', encoding = 'utf-8', sep = ';', index = False)
                            # data = carrega_produtos_capturados('dados/resultado_mercado_livre.csv')
                            data[selected_row][6] = edit_event
                            window['-TABLE-'].update(values=data)
                        
                        edit_window.close()
                        break 

        if event == '-ACESSAR-':
            import webbrowser
            selected_row = values['-TABLE-']
            if selected_row != []:
                selected_row = values['-TABLE-'][0]
                url = data[selected_row][8]
                webbrowser.open(url)

    # Fechando a janela
    window.close()