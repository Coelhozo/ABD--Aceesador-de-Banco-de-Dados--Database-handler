import PySimpleGUI as sg
from telas import telaInicial as telaIni

def openWindow(nome, layout):

    janela = sg.Window(nome, layout, element_justification='c')

    while True:
        evento, valores = janela.read()

        if evento == "telaInc" or evento == "regBD" or evento == "telaIncReg" or evento == "telaIncRemover" or evento == "telaIncEditar" or evento == "telaIncVisualizar":
            erro = telaIni.telaInicial(valores, evento)
            if erro:
                janela.Element("-TITLE-").update(erro, text_color="Red")
            elif evento != "regBD" and evento != "telaIncRemover" and evento != "telaIncEditar" and evento != "telaIncVisualizar":
                break
        elif evento == "regNome" or evento == "regAtualizar":
            janela.close()
            return valores
        else:
            break
        
        #updates de tela
        #->Update da tela inicial
        if evento != "regNome" and nome == "Acessador de Banco de Dados":
            indexes = telaIni.getIndex()
            janela["RegEnter"].update(indexes)

    janela.close()


def createWindow(window, origem = None, theme="DarkAmber", itensExibicao = None):
    sg.theme(theme)

    if window == 0:
        layout = [
            [sg.T(f"{itensExibicao}")]
        ]

        nome = "Ocorreu um erro."
    # layout da tela inicial
    if (window == 1):
        layout_coluna_input = [
            [sg.InputText(key="Host")],
            [sg.InputText(key="Usuario")],
            [sg.InputText(key="Senha", password_char="#")],
            [sg.InputText(key="Banco")]
        ]

        layout_coluna_text = [
            [sg.Text("Host: ")],
            [sg.Text("Usuário: ")],
            [sg.Text("Senha: ")],
            [sg.Text("Banco de Dados: ")]
        ]

        indexes = telaIni.getIndex()
        layout_frame_registros = [
            [sg.Listbox(values=indexes, size=(34,6), key="RegEnter")],
            [sg.Button("Remover", key="telaIncRemover"), sg.Button("Editar", key="telaIncEditar"), sg.Button("Visualizar", key="telaIncVisualizar"), sg.Button("Pronto", key="telaIncReg")]
        ]

        layout_frame_inserir= [
            [sg.Column(layout_coluna_text, vertical_alignment="left", justification="left"), sg.Column(layout_coluna_input, vertical_alignment="right", justification="right")],
            [sg.Button("Salvar", key="regBD"), sg.Button("Pronto", key="telaInc")]
        ]

        layout = [
            [sg.Text("Bem-Vindo!", key="-TITLE-")],
            [sg.Frame(" Inserir ", layout_frame_inserir, element_justification="center", title_color="white", border_width="1px"), sg.Frame(" Registros ", layout_frame_registros, element_justification="center", title_color="white", border_width="1px")]
        ]

        nome = "Acessador de Banco de Dados"
    if (window == 2):
        if origem == "save":
            layout = [
                [sg.T("Defina um nome para salvar este endereço de acesso.")],
                [sg.InputText(key="nome")],
                [sg.Button("Pronto", key="regNome")]
            ]

            nome = "Nome do Registro"
        if origem == "atualizar":

            layout_coluna_input = [
                [sg.InputText(key="Nome")],
                [sg.InputText(key="Host")],
                [sg.InputText(key="Usuario")],
                [sg.InputText(key="Senha", password_char="#")],
                [sg.InputText(key="Banco")]
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
                [sg.Column(layout_coluna_text, vertical_alignment="left", justification="left"), sg.Column(layout_coluna_input, vertical_alignment="right", justification="right")],
                [sg.Button("Pronto", key="regAtualizar")]
            ]

            nome = "Atualizar registro"

        if origem == "visualizar":
            
            layout_coluna_text = [
                [sg.Text(f"Host: {itensExibicao['Host']}")],
                [sg.Text(f"Usuário: {itensExibicao['Usuario']}")],
                [sg.Text(f"Senha: {itensExibicao['Senha']}")],
                [sg.Text(f"Banco de Dados: {itensExibicao['Banco']}")]
            ]

            layout = [
                [sg.T("Detalhes do registro")],
                [sg.Column(layout_coluna_text, vertical_alignment="left", justification="left", size=(280, 120))],
            ]

            nome = "Visualizar Registro"

    values = openWindow(nome, layout)
    if values:
        return values

if __name__ == "__main__":
    createWindow(1)