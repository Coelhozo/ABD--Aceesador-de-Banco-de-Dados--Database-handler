from dll import telaInicial as ti
from dll import createWindow as cw
from dll import connectorDB as con

if __name__ == '__main__':

    #inicia o programa pela tela inicial
    cw.createWindow('-TI-', itensExibicao=ti.getIndex())

    #inicia/continua o programa pela tela de visualização de tabelas
    result = con.executarQuery("SHOW TABLES")
    tables = []
    [tables.append(item[0]) for item in result]
    describe = {}
    for table in tables:
        cols = con.executarQuery(f"Describe {table}")
        describe[table] = list()
        [describe[table].append(cols[c][0]) for c in range(len(cols))]

    cw.createWindow('-TL-', theme='DarkBrown6', text=con.getDBVariables()['Banco'], itensExibicao=describe)