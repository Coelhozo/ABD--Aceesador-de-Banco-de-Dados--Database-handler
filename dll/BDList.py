import connectorDB as con

def BDList(values):
    if not values['-BD-']:
        return "Selecione um banco de dados para acessar"
    
def getList():
    data = con.executarQuery("SHOW DATABASES;")
    print(data)

getList()