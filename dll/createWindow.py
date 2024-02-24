import PySimpleGUI as sg
from dll import openWindow as op

def createWindow(window, theme='DarkAmber', itensExibicao = None, text = None):
    sg.theme(theme)

    if window == '-ERR-':
        layout = [
            [sg.T(f'{itensExibicao}')]
        ]
        nome = "Ocorreu um erro."

    # layout da tela inicial
    if window == '-TI-':

       #Frame 01 
        layout_coluna_input = [
            [sg.InputText(key='Host')],
            [sg.InputText(key='Usuario')],
            [sg.InputText(key='Senha', password_char='#')],
            [sg.InputText(key='Banco')]
        ]

        layout_coluna_text = [
            [sg.Text("Host: ")],
            [sg.Text("Usuário: ")],
            [sg.Text("Senha: ")],
            [sg.Text("Banco de Dados: ")]
        ]

        #Frame 02
        layout_frame_registros = [
            [sg.Listbox(values=itensExibicao, size=(34,6), key='-REGISTRO-')],
            [sg.Button('Remover', key='-TIF02DL-'), sg.Button('Editar', key='-TIF02UP-'), sg.Button('Visualizar', key='-TIF02SW-'), sg.Button('Pronto', key='-TIF02OK-')]
        ]

        layout_frame_inserir= [
            [sg.Column(layout_coluna_text, vertical_alignment='left', justification='left'), sg.Column(layout_coluna_input, vertical_alignment='right', justification='right')],
            [sg.Button('Salvar', key='-TIF01SV-'), sg.Button('Pronto', key='-TIF01OK-')]
        ]

        layout = [
            [sg.Text('Bem-Vindo!', key='-TITLE-')],
            [sg.Frame(' Inserir ', layout_frame_inserir, element_justification='center', title_color='white', border_width='1px'), sg.Frame(' Registros ', layout_frame_registros, element_justification='center', title_color='white', border_width='1px')]
        ]

        nome = "Acessador de Banco de Dados"
    
    #Layout da tela complementar ao frame 01 da tela inicial do tipo salvar (SV)
    if window == '-TIF01CSV-':
        layout = [
            [sg.T("Defina um nome para salvar este endereço de acesso.")],
            [sg.InputText(key='nome')],
            [sg.Button('Pronto', key='-TIF01CSVN-')]
        ]

        nome = "Nome do Registro"
    
    #Layout da tela complementar ao frame 02 da tela inicial do tipo atualizar (UP)
    if window == '-TIF02CUP-':

        layout_coluna_input = [
            [sg.InputText(key='Nome')],
            [sg.InputText(key='Host')],
            [sg.InputText(key='Usuario')],
            [sg.InputText(key='Senha', password_char='#')],
            [sg.InputText(key='Banco')]
        ]

        layout_coluna_text = [
            [sg.Text("Nome do Registro: ")],
            [sg.Text("Host: ")],
            [sg.Text("Usuário: ")],
            [sg.Text("Senha: ")],
            [sg.Text("Banco de Dados: ")]
        ]

        layout = [
            [sg.T("Defina os valores do campo que queira atualizar.")],
            [sg.Column(layout_coluna_text, vertical_alignment='left', justification='left'), sg.Column(layout_coluna_input, vertical_alignment='right', justification='right')],
            [sg.Button('Pronto', key='-TIF02CUPR-')]
        ]

        nome = "Atualizar registro"

    #Layout da tela complementar ao frame 02 da tela inicial do tipo visualizar (SW)
    if window == '-TIF02CSW-':
            
        layout_coluna_text = [
            [sg.Text(f"Host: {itensExibicao['Host']}")],
            [sg.Text(f"Usuário: {itensExibicao['Usuario']}")],
            [sg.Text(f"Senha: {itensExibicao['Senha']}")],
            [sg.Text(f"Banco de Dados: {itensExibicao['Banco']}")]
        ]

        layout = [
            [sg.T("Detalhes do registro")],
            [sg.Column(layout_coluna_text, vertical_alignment='left', justification='left', size=(280, 120))],
        ]

        nome = "Visualizar Registro"

    #Layout da tela de visualização de bancos de dados do servidor
    if window == '-BL-':
        layout = [
            [sg.T("Lista de Banco de dados no servidor", key='-TITLE-')],
            [sg.Listbox(values=itensExibicao, size=(100,6), key='-BD-')],
            [sg.Button('Pronto', key='-BLF01UP-')]
        ]

        nome = f"Host: {text}"

    if window == '-TL-':
        layout = [
            [sg.T('Lista de Tabelas')]
        ]
        frame = list()
        for item in itensExibicao:
            value = itensExibicao[item]
            description = [
                [sg.T("Colunas")],
                [sg.Combo(value, size=(600,6), default_value=value[0])],
                [sg.Button('Acessar', key=f'-TLOP{item}-')]
            ]

            frame.append([sg.Frame(item, description, element_justification='left', title_color='white', border_width='1px', size=(600, 100))])
        layout.append([sg.Column(frame, size=(600,400), scrollable=True, vertical_scroll_only=True)])
        nome = f"Banco: {text}"

    if window == '-CRUD-':
        crud = [
            [sg.Button('Criar', key='-CRUDCSV-')],
            [sg.Button('Atualizar', key='-CRUDCUP-')],
            [sg.Button('Deletar', key='-CRUDCDL-')]
        ]
        layout = [
            [sg.Column(crud), 
             sg.Table(
                itensExibicao['data'], 
                headings=itensExibicao['cols']
            )]
        ]
        nome = f'Tabela: {text}'
    
    values = op.openWindow(nome, layout)
    if values:
        return values
