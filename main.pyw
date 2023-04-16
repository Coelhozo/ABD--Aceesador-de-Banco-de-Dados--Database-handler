import PySimpleGUI as sg
import re
from telas import telaInicial as telaIni
from telas import createWindow as cw
from telas import requestTela

def openWindow(nome, layout):

    janela = sg.Window(nome, layout, element_justification='c')
    argsMissing = None

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
            try:
                argsMissing = telaIni.telaInicial(values, event)
                if argsMissing:
                    janela.Element('-TITLE-').update(argsMissing, text_color='Red')
            except FileNotFoundError:
                requestTela.request('-ERR-', itens=f"Verifique se entries/index.txt e entries/data/{values['-REGISTRO-'][0]}.txt não foram apagados")
            except FileExistsError:
                requestTela.request('-ERR-', itens=f"O arquivo com o nome {values['-REGISTRO-'][0]} já existe, não crie arquivos manualmente, insira o nome do registro no index")
        if isOK.match(event) and not argsMissing:
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