def tela_inicial(produtos_para_pesquisa):   
    import PySimpleGUI as sg
    
    sg.theme("black")
    
    texto_principal  = 'Escolha produtos para pesquisar:'
    font_principal = ('Arial', 18)
    font_secundario = ('Arial', 12)
    texto_secundario = 'Marque as  caixas de seleção para incluir os produtos na pesquisa.'
    texto_terciario  = 'Clique no produto para editar os critérios de pesquisa ou para excluir.'
    
    col1=[[ sg.Image( 'logo_pequeno.png')]]
    col2=[[ sg.Button('Treinar Modelo'), sg.Button('Configurações')]]


    layout = [
        [ [sg.Column(col1, element_justification='left' ), sg.Column(col2, element_justification='right')]],
        [ sg.Text( texto_principal, font = font_principal) ],
        [],
        
        [ 
            sg.Button('Adicionar Produto'),
            sg.Button('Editar'),
            sg.Button('Excluir'),
            sg.Text(' '*30),
            sg.Button('Avançar >>')
        ]
    ]
        
    # Cria a janela do programa
    window = sg.Window('REGULATRON - Versão beta 0.2', 
                       layout, 
                       element_justification='left',
                       size=(1024, 600)
                      )

    # Loop para processar os "events" e atualizar os valores dos inputs
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED : 
            break    
        
    # fim da tela inicial
    #editar palavras "yes-words" e "no-words" dos produtos        

def editar_produtos_para_pesquisar(): 

    # carrega os produtos
    data = carregar_produtos()

    table_data = [[key, ','.join(data[key]['yes-words']), ','.join(data[key]['no-words'])] for key in data]

    layout = [
        # primeira linha - imagem do logotipo
        [sg.Image('img/logo.png', size=(781,240))],

        # segunda linha
        [sg.Table(
            values=table_data, 
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

        if event == '-ADD-':
            try:
                # código para adicionar um novo produto

                layout_add = [ # Define o layout da janela para adicionar um novo registro
                    [sg.Text('Nome do dispositivo:'), sg.Input(key='nome')],
                    [sg.Text('yes-words (separadas por vírgula):'), sg.Input(key='yes-words')],
                    [sg.Text('no-words (separadas por vírgula):'), sg.Input(key='no-words')],
                    [sg.Button('Adicionar'), sg.Button('Cancelar')]
                ]

                # Cria a janela
                window_add = sg.Window('Novo registro', layout_add)

                # Loop de eventos
                while True:
                    event, values = window_add.read()

                    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                        break

                    elif event == 'Adicionar':
                        nome = values['nome']
                        data[nome] = {
                            'yes-words': values['yes-words'].split(','),
                            'no-words': values['no-words'].split(',')
                        }

                        save_data('produtos_para_pesquisa.json', data)

                        #atualiza a tabela ##### TODO -- fazer uma função para atualizar a tabela
                        table_data = [[key, ','.join(data[key]['yes-words']), ','.join(data[key]['no-words'])] for key in data]
                        window['-TABLE-'].update(values=table_data)

                        # Exibir mensagem de confirmação
                        sg.popup(f'Registro "{nome}" adicionado com sucesso!', title='Sucesso')

                        # Fechar a janela
                        break

                window_add.close()

            except Exception as e:
                print(e)      


            pass

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

            pass # ========================================================================================= BUGADO

        if event == '-REMOVE-':
            try:
                confirm = sg.popup_yes_no('Deseja excluir o produto da lista de pesquisa?')
                if confirm == 'Yes':

                    # Obter a linha selecionada na tabela
                    selected_row = values['-TABLE-']

                    if selected_row != []:

                        # Obter a linha selecionada
                        selected_row = values['-TABLE-'][0]

                        # remover os dados do dict
                        data.pop(  table_data[selected_row][0]  )
                        save_data('produtos_para_pesquisa.json', data)

                        # Remover a linha dos dados da tabela
                        table_data.pop(selected_row)

                        # Atualizar a tabela
                        window['-TABLE-'].update(values=table_data)

            except Exception as e:
                print(e)

            pass

    window.close()
    