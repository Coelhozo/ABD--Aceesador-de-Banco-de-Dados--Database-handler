import main

def request(tela, origem="", itens = None):
    if tela == 2:
        tema = "DarkBlue"
    
    if tela == 0:
        tema = "DarkRed2"
    return main.createWindow(tela, origem, theme = tema, itensExibicao = itens)