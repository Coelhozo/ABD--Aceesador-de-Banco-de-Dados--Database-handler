import mysql.connector as ms
from dll import utilidades as utils

def executarQuery(query):
    dbValues = getDBVariables()
    print(dbValues)
    data = []
    with ms.connect(
        host=dbValues['Host'],
        user=dbValues['Usuario'],
        password=dbValues['Senha'] if dbValues['Senha'] != "''" else '',
        database = dbValues['Banco'] if dbValues['Banco'] else None
    ) as con:
        cursor = con.cursor()
        cursor.execute(query)
        for item in cursor:
            data.append(item)
        return data
        

def writeDBVariables(values):
    filename = f"dbVariables.txt"
    with open(filename, 'w') as file:
        file.write(
            f"""Usuario: {values['Usuario']}
Senha: {values['Senha']}
Host: {values['Host']}
Banco: {values['Banco'] if values['Banco'] else ''}"""
        )

def getDBVariables():
    return utils.getEntry()