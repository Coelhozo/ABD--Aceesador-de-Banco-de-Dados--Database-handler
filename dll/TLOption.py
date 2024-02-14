from dll import connectorDB as con

def getTableData(table):
    #lista das colunas - headings -
    cols = con.executarQuery(f"describe {table}")
    colunas = list()
    [colunas.append(col[0]) for col in cols]
    
    result = con.executarQuery(f"select * from {table}")
    return {'cols': colunas, 'data': result}
