from dll import connectorDB as con

def BDList(values):
    if not values['-BD-']:
        return "Selecione um banco de dados para acessar"
    
def getList():
    data = con.executarQuery("SHOW DATABASES;")
    bancos = []
    for banco in data:
        bancos.append(banco[0])
    return(bancos)