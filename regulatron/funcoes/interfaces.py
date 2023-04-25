import PySimpleGUI as sg
from funcoes.acessar_dados import *

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
                            size=(15,1))
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
            sg.Text(' '*120),
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
        
        if event == 'Editar':  # Editar produto # ===========================
            
            produtos_selecionados = [k for k, v in values.items() if v]


            if len(produtos_selecionados) == 0: # testa se há algum produto foi selecionado
                sg.popup('Nenhum produto foi selecionado')
            
            elif len(produtos_selecionados) > 1:
                sg.popup_yes_no('Só é possível editar um produto por vez.')

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

    window.close()
    
    # fim da tela inicial
   

def editar_produto(janela, produto):

    dados_produtos = carregar_json('dados/produtos.json')
    produto_dict = dados_produtos[produto]

    # pegar o produto a partir do dict
    yes_words = produto_dict['yes-words']
    no_words = produto_dict['no-words']

    # Criar uma janela de edição        
    layout_edit = [
        [sg.Text('Nome do produto:'), sg.InputText(produto, key='nome')],
        [sg.Text('yes-words (separadas por vírgula):'), sg.InputText(yes_words, key='yes-words')],
        [sg.Text('no-words (separadas por vírgula):'), sg.InputText(no_words, key='no-words')],
        [sg.Button('Salvar', key='-SAVE-'), sg.Button('Cancelar')]
    ]

    window_edit = sg.Window('Editar produto', layout_edit)

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
  



def editar_produtos_para_pesquisar():   #adicionar produtos e editar  palavras "yes-words" e "no-words" dos produtos        

    # carrega os produtos
    dados = carregar_json('dados/produtos.json')

    conteudo_tabela = [ [key, ','.join(dados[key]['yes-words']), ','.join(dados[key]['no-words'])] for key in dados ]

    layout = [
        # primeira linha - imagem do logotipo
        [sg.Image('img/logo.png', size=(781,240))],

        # segunda linha
        [sg.Table(
            values=conteudo_tabela, 
            headings=['Produto', 'Yes-words', 'No-words'],
            key='-TABLE-',
            justification='center',
            num_rows=10, 
            auto_size_columns=False,
            def_col_width=26,
            enable_events=True)

        ],

        # terceira linha
        [sg.Button('Adicionar produto', key='-ADD-'),
         sg.Button('Editar produto', key='-EDIT-', disabled=True),
         sg.Button('Remover produto', key='-REMOVE-', disabled=True),
         sg.Button('Voltar para a tela inicial', key='-VOLTAR-')]
    ]

    # Configurações da janela
    sg.theme('Black')   # tema escuro
    window = sg.Window('Regulatron - Editar produtos da pesquisa', layout, size=(1024, 600), element_justification="c")
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event== '-VOLTAR-':            
            window.close()
            escolher_produtos_para_pesquisar()

            
        if event == '-TABLE-':
            try:
                row_index = window['-TABLE-'].get()[0]
                window['-EDIT-'].update(disabled=False)
                window['-REMOVE-'].update(disabled=False)
            except:
                window['-ERROR-'].update('Selecione um produto para editar ou remover')



        if event == '-EDIT-': 
    #        try:

            # Obter a linha selecionada na tabela
            selected_row = values['-TABLE-']

            if selected_row != []:

                selected_row = values['-TABLE-'][0]

                # código para editar o produto selecionado

                # Criar uma janela de edição        
                edit_layout = [
                    [sg.Text('Nome do dispositivo:'), sg.InputText(table_data[selected_row][0], key='nome')],
                    [sg.Text('yes-words (separadas por vírgula):'), sg.InputText(table_data[selected_row][1], key='yes-words')],
                    [sg.Text('no-words (separadas por vírgula):'), sg.InputText(table_data[selected_row][2], key='no-words')],
                    [sg.Button('Salvar', key='-SAVE-'), sg.Button('Cancelar')]
                ]

                edit_window = sg.Window('Editar linha', edit_layout)

                # Loop de eventos da janela de edição
                while True:
                    edit_event, edit_values = edit_window.read()

                    if event == sg.WINDOW_CLOSED or edit_event == 'Cancelar':                
                        break

                    elif edit_event == '-SAVE-':

                        data[ edit_values['nome'] ] = {
                            'yes-words': edit_values['yes-words'].split(','),
                            'no-words': edit_values['no-words'].split(',')
                        }

                        save_data('produtos_para_pesquisa.json', data)

                        #atualiza a tabela ##### TODO -- fazer uma função para atualizar a tabela
                        table_data = [[key, ','.join(data[key]['yes-words']), ','.join(data[key]['no-words'])] for key in data]
                        window['-TABLE-'].update(values=table_data)
                        break

                edit_window.close()

    #        except Exception as e:
    #            print(e)

    #                 

            pass 

            
            

    window.close()
    