import PySimpleGUI as sg
import re
from telas import telaInicial as telaIni
from telas import createWindow as cw

def openWindow(nome, layout):

    janela = sg.Window(nome, layout, element_justification='c')
    erro = None

    #expressões regulares para os tipos gerais de eventos
    isTelaInicial = re.compile(r'-TIF[0-9]{2}\w{2}-')
    isOK = re.compile(r'-TIF[0-9]{2}OK-')
    returnsData = re.compile(r'-.*C(UP)?(SV)?\w-')

    while True:
        event, values = janela.read()

        if event == sg.WIN_CLOSED:
            break
        
        #verificação de telas
        telaInicial = isTelaInicial.match(event)

        if telaInicial:
            erro = telaIni.telaInicial(values, event)
            if erro:
                janela.Element('-TITLE-').update(erro, text_color='Red')
        if isOK.match(event) and not erro:
            break
        if returnsData.match(event):
            janela.close()
            return values
        
        #updates de tela
        #->Update da tela inicial
        if event != '-TIF01CSVN-' and telaInicial:
            indexes = telaIni.getIndex()
            janela['-REGISTRO-'].update(indexes)

    janela.close()

if __name__ == '__main__':

    cw.createWindow('-TI-')