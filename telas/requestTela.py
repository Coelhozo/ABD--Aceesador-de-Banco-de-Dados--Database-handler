from telas import createWindow as cw

def request(tela, itens = None, tema = "DarkAmber"):
    if 'C' in tela:
        tema = 'DarkBlue'
    
    if tela == '-ERR-':
        tema = 'DarkRed2'
    return cw.createWindow(tela, theme = tema, itensExibicao = itens)