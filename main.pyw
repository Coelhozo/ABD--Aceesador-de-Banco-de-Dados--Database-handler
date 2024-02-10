from dll import telaInicial as ti
from dll import createWindow as cw
from dll import connectorDB as con

if __name__ == '__main__':

    #inicia o programa pela tela inicial
    cw.createWindow('-TI-', itensExibicao=ti.getIndex())

    #inicia/continua o programa pela tela de visualização de tabelas
    cw.createWindow('-TL-', theme='DarkBrown6', text=con.getDBVariables()['Host'], itensExibicao=[1,2,3,4,5,6,7,8])
        