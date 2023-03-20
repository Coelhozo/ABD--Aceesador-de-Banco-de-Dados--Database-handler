import PySimpleGUI as sg
from telas import telaInicial as telaIni

def openWindow(nome, layout):

    janela = sg.Window(nome, layout, element_justification='c')

    while True:
        evento, valores = janela.read()
        if evento == "telaInc" or evento == "regBD" or evento == "telaIncReg":
            erro = telaIni.telaInicial(valores, evento)
            if erro:
                janela.Element("-TITLE-").update(erro, text_color="Red")
            else:
                break
        elif evento == "regNome":
            janela.close()
            return valores
        else:
            break

    janela.close()


def createWindow(window, origem="", theme="DarkAmber"):
    sg.theme(theme)
    # layout da tela inicial
    if (window == 1):
        layout_coluna_input = [
            [sg.InputText(key="Host")],
            [sg.InputText(key="Usuário")],
            [sg.InputText(key="Senha")],
            [sg.InputText(key="Banco")]
        ]

        layout_coluna_text = [
            [sg.Text("Host: ")],
            [sg.Text("Usuário: ")],
            [sg.Text("Senha: ")],
            [sg.Text("Banco de Dados: ")]
        ]

        layout_frame_registros = [
            [sg.Listbox(values=["pedro1", "pedro2", "pedro3", "pedro4", "pedro5"], size=(30,6), key="RegEnter")],
            [sg.Button("Pronto", key="telaIncReg")]
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

    values = openWindow(nome, layout)
    if values:
        return values

if __name__ == "__main__":
    createWindow(1)