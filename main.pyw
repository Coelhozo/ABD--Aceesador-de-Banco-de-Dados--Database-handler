import PySimpleGUI as sg
import re

from dll import telaInicial as telaIni
from dll import createWindow as cw
from dll import requestTela
from dll import BDList as bl

from dll import connectorDB as con

def openWindow(nome, layout):

    janela = sg.Window(nome, layout, element_justification='c')

    #argumentos obrigatórios que não foram preenchidos
    argsMissing = None

    #informações de acesso no banco de dados
    bdValues = None

    #expressões regulares para os tipos gerais de eventos
    isTelaInicial = re.compile(r'-TIF[0-9]{2}\w{2}-')
    isTelaBL = re.compile(r'-BL\w*')
    isOK = re.compile(r'-\w*OK-') # de -TIF[0-9]{2}OK- para -\w*OK-
    returnsData = re.compile(r'-.*C(UP)?(SV)?\w-')

    while True:
        event, values = janela.read()

        if event == sg.WIN_CLOSED:
            break
        
        #verificação de telas
        if isTelaInicial.match(event):
            try:

                argsMissing = telaIni.telaInicial(values, event)
                if argsMissing:
                    janela.Element('-TITLE-').update(argsMissing, text_color='Red')
            except FileNotFoundError:

                requestTela.request('-ERR-', itens=f"Verifique se entries/index.txt e entries/data/{values['-REGISTRO-'][0]}.txt não foram apagados")
            except FileExistsError:

                requestTela.request('-ERR-', itens=f"O arquivo com o nome {values['-REGISTRO-'][0]} já existe, não crie arquivos manualmente, insira o nome do registro no index")
            if isOK.match(event) and not argsMissing:

                bdValues = telaIni.trimValues(values, event)
                con.writeDBVariables(bdValues)
                break

        if isTelaBL.match(event):
            argsMissing = bl.BDList(values);
            if argsMissing:
                janela.Element('-TITLE-').update(argsMissing, text_color='Red')

        if returnsData.match(event):
            janela.close()
            return values
        
        #updates de tela
        #->Update da tela inicial
        if event != '-TIF01CSVN-' and isTelaInicial.match(event):
            indexes = telaIni.getIndex()
            janela['-REGISTRO-'].update(indexes)

    janela.close()

    #continua a execução do código
    if bdValues:
        tela = '-BL-' if not bdValues['Banco'] else '-TL-'
        cw.createWindow(tela, theme="Black", text=bdValues['Host'])

if __name__ == '__main__':

    cw.createWindow('-TI-')
        