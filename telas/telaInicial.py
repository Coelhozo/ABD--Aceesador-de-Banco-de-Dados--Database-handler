import telas.requestTela as requestTela
from shutil import rmtree
import re
import os

#variáveis de escopo global para o módulo
entriesPATH = "entries/data/"
indexPATH = "entries/index.txt"

def telaInicial(values, event):
    if runCheck(values, event):
        #events do frame 01 -INSERIR-
        eventPattern = re.compile(r'-\w{3}([0-9]{2})(\w{2})-')
        operation = eventPattern.match(event)

        if operation.group(1)=='01':
            if operation.group(2)=='SV':
                while True:
                    nome = requestTela.request('-TIF01CSV-')
                    if not nome or not nome['nome'] in getIndex():
                        break
                    else:
                        requestTela.request('-ERR-', itens="Esse nome já consta nos registros.")
                if nome:
                    saveEntry(values, nome['nome'])
            else:
                print(values)
        else:
            #events do frame 02 -registros-
            nome = values['-REGISTRO-'][0]

            if operation.group(2) == 'DL':
                i = getIndex()
                #remove todo o diretório
                rmtree(path=entriesPATH+i.pop(i.index(nome)))
                index = "\n".join(i)
                writeIndex(index, action='w')

            elif operation.group(2) == 'UP':
                data = requestTela.request('-TIF02CUP-')
                if data and any(dado != "" for dado in list(data.values())):

                    if data['Nome']:
                        i = getIndex()
                        removedItem = i.index(nome)
                        i.pop(removedItem)
                        i.insert(removedItem, data['Nome'])
                        index = "\n".join(i)
                        writeIndex(index, action='w')
                        #edita o nome da pasta antes de editar o nome do arquivo
                        os.rename(entriesPATH+f"{nome}",  entriesPATH+f"{data['Nome']}")
                        os.rename(entriesPATH+f"{data['Nome']}/{nome}.txt", entriesPATH+f"{data['Nome']}/{data['Nome']}.txt")
                        nome = data['Nome']
                        
                    data.pop('Nome')
                    oldRecord = getEntry(nome)
                    newRecord = {}
                    for col in data:
                        if data[col]:
                            newRecord[col] = data[col]
                        else:
                            newRecord[col] = oldRecord[col]
                    saveEntry(newRecord, nome, update = True)

            elif operation.group(2) == 'SW':
                entryInfo = getEntry(nome)
                requestTela.request('-TIF02CSW-', entryInfo)
    else:
        return errorMessage(values, event)


def runCheck(values, event):
    if re.match(r'-TIF01.*-', event):
        # confere se os campos foram preenchidos
        for key in values:
            if not values[key] and key != '-REGISTRO-':
                # se o valor vazio não for do campo -BD-, retorne falso
                if not key == 'Banco':
                    return False
        return True
    
    if re.match(r'-TIF02.*-', event):
        if not values['-REGISTRO-']:
            return False
        else:
            return True


def saveEntry(values, nome, update = False):
    if not update:
        writeIndex(nome)
        path = os.path.join(entriesPATH+f"{nome}/")
        os.mkdir(path)
    
    filename = entriesPATH+f"{nome}/{nome}.txt"
    with open(filename, 'w') as file:
        file.write(
            f"""Usuario: {values['Usuario']}
Senha: {values['Senha']}
Host: {values['Host']}
Banco: {values['Banco']}"""
        )

def getEntry(nome):
    filename = entriesPATH+f"{nome}/{nome}.txt"
    with open(filename, 'r') as entry:
        i = entry.read()
    data = i.split('\n')
    valores = [item.split(': ') for item in data]
    
    oldRecords = {}
    for item in valores:
        oldRecords[item[0]] = item[1]
    return oldRecords

def writeIndex(nome='', action = 'a'):
    filename = indexPATH
    #insere o seprador caso haja algum indice no index.txt
    if nome: nome+='\n'
        
    with open(filename, action) as file:            
        file.write(nome)

def getIndex():
    with open(indexPATH, 'r') as index:
        i = index.read()
        indexes = i.split('\n')
        indexes.pop(-1)#Retira o ultimo item (vázio)
    return indexes

def errorMessage(values = '', event = ''):
    if not values['-REGISTRO-'] and re.match(r'-TIF02\w{2}-', event):
        return "Selecione um registro"
    values.pop('-REGISTRO-')
    # constrói a menssagem de erro
    plural = True
    done = False
    c = 1
    # define o offset para localizar a vírgula
    empty = 0
    for key in values:
        if values[key] == "":
            empty += 1

    if not values['Banco'] and empty == 2:
        plural = False
    if values['Banco']:
        if empty == 1:
            plural = False
        empty += 1

    offset = len(values)-empty

    if offset == 3:
        return

    while (True and not done):
        if (plural):
            erro = 'Os campos: '

            for key in values:
                if not values[key] and key != 'Banco':
                    c += 1
                    erro += key.lower()

                    if len(values) - c > 1+offset:
                        erro += ","
                    elif len(values) - c > offset:
                        erro += " e"

                    erro += " "

                if (key == 'Banco'):
                    erro += "têm que ser preenchidos"
                    done = True
                    break
        else:
            erro = "O campo "
            for key in values:
                if not values[key] and key != 'Banco':
                    erro += key.lower()
            erro += " tem que ser preenchido"
            break
    return erro