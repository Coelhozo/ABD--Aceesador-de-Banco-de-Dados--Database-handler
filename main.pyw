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
        
        isTI = isTelaInicial.match(event)
        isBL = isTelaBL.match(event)

        #verificação de telas
        if isTI:
            try:
                argsMissing = telaIni.telaInicial(values, event)
                if argsMissing:
                    janela.Element('-TITLE-').update(argsMissing, text_color='Red')
            except FileNotFoundError:
                requestTela.request('-ERR-', itens=f"Verifique se entries/index.txt e entries/data/{values['-REGISTRO-'][0]}.txt não foram apagados")
            except FileExistsError:
                requestTela.request('-ERR-', itens=f"O arquivo com o nome {values['-REGISTRO-'][0]} já existe, não crie arquivos manualmente, insira o nome do registro no index")
        
        if isOK.match(event) and not argsMissing:
            if isTI:
                bdValues = telaIni.trimValues(values, event)
                con.writeDBVariables(bdValues)
            break

        
        if isBL:
            argsMissing = bl.BDList(values);
            if argsMissing:
                janela.Element('-TITLE-').update(argsMissing, text_color='Red')

        if returnsData.match(event) or isBL:
            janela.close()
            return values
        
        #updates de tela
        #->Update da tela inicial
        if event != '-TIF01CSVN-' and isTI:
            indexes = telaIni.getIndex()
            janela['-REGISTRO-'].update(indexes)

    janela.close()

    #caso o banco não for selecionado no momento de registro de credenciais, é inserido neste ponto
    if bdValues and not bdValues['Banco']:
        list = bl.getList();
        bd = cw.createWindow('-BL-', theme="Black", text=bdValues['Host'], itensExibicao=list)
        bdValues['Banco'] = bd['-BD-'][0]
        con.writeDBVariables(bdValues)

if __name__ == '__main__':

    #inicia o programa pela tela inicial
    cw.createWindow('-TI-', itensExibicao=telaIni.getIndex())

    #inicia/continua o programa pela tela de visualização de tabelas
    cw.createWindow('-TL-', theme='DarkBrown6', text=con.getDBVariables()['Host'], itensExibicao=[1,2,3,4,5,6,7,8])
        