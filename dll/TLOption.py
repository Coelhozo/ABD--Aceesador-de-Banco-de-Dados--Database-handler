from dll import connectorDB as con
from dll import createWindow as cw

def getTableData(table):
    #lista das colunas - headings -
    cols = con.executarQuery(f"describe {table}")
    colunas = list()
    [colunas.append(col[0]) for col in cols]
    
    result = con.executarQuery(f"select * from {table}")
    return {'cols': colunas, 'data': result}

def CRUD(event, data):
    if 'DL' in event:
        delete(data)
    
    inputData = cw.createWindow('-CRUDCSV+-', theme='Black')
    if 'SV' in event:
        create()
    else:
        update()

def delete(data):
    pass

def update():
    pass

def create():
    pass
