import telas.requestTela as requestTela
import os

def telaInicial(values, evento):
    if runCheck(values, evento):
        #eventos de botões da tela inicial são default e os de telas derivadas são os casos
        if evento == "regBD":
            while True:
                nome = requestTela.request(2, "save")
                if not nome or not nome["nome"] in getIndex():
                    break
                else:
                    requestTela.request(0, itens="Esse nome já consta nos registros.")
            if nome:
                saveEntry(values, nome["nome"])
        else:
            #eventos dos botões da tela inicial
            if evento == "telaIncRemover":
                i = getIndex()
                os.remove("Entries/"+i.pop(i.index(values["RegEnter"][0]))+".txt")
                index = "\n".join(i)
                writeIndex(index, action="w")

            elif evento == "telaIncEditar":
                dados = requestTela.request(2, "atualizar")
                if dados and any(dado != "" for dado in list(dados.values())):
                    nome = values["RegEnter"][0]

                    if dados["Nome"]:
                        i = getIndex()
                        removedItem = i.index(nome)
                        i.pop(removedItem)
                        i.insert(removedItem, dados["Nome"])
                        index = "\n".join(i)
                        writeIndex(index, action="w")
                        os.rename(f"Entries/{nome}.txt", f"Entries/{dados['Nome']}.txt")
                        nome = dados['Nome']
                        
                    dados.pop("Nome")
                    vRegistro = getEntry(nome)
                    nRegistro = {}
                    for tipo in dados:
                        if dados[tipo]:
                            nRegistro[tipo] = dados[tipo]
                        else:
                            nRegistro[tipo] = vRegistro[tipo]
                    saveEntry(nRegistro, nome, atualizar = True)

            elif evento == "telaIncVisualizar":
                nome = values["RegEnter"][0]
                valores = getEntry(nome)
                requestTela.request(2, "visualizar", valores)
                    
            else:
                print(values)
    else:
        return errorMessage(values, evento)


def runCheck(values, evento):
    if evento == "telaInc" or evento == "regBD":
        # confere se os campos foram preenchidos
        for key in values:
            if not values[key] and key != "RegEnter":
                # se o valor vazio não for do campo -BD-, retorne falso
                if not key == "Banco":
                    return False
        return True
    
    if evento == "telaIncReg" or evento == "telaIncRemover" or evento == "telaIncEditar" or evento == "telaIncVisualizar":
        if not values["RegEnter"]:
            return False
        else:
            return True


def saveEntry(values, nome, atualizar = False):
    filename = "Entries/"+nome+".txt"
    with open(filename, "w") as file:
        file.write(
            f"""Usuario: {values["Usuario"]}
Senha: {values["Senha"]}
Host: {values["Host"]}
Banco: {values["Banco"]}"""
        )
    
    if not atualizar:
        writeIndex(nome)

def getEntry(nome):
    filename = "Entries/"+nome+".txt"
    with open(filename, "r") as entry:
        i = entry.read()
    data = i.split("\n")
    valores = [item.split(": ") for item in data]
    
    vRegistros = {}
    for item in valores:
        vRegistros[item[0]] = item[1]
    return vRegistros

def writeIndex(nome="", action = "a"):
    filename = f"Entries/index.txt"
    nome+="\n"
    
    with open(filename, action) as file:            
        file.write(nome)

def getIndex():
    try:
        with open("Entries/index.txt", "r") as index:
            i = index.read()
            indexes = i.split("\n")
            indexes.pop(-1)
        return indexes
    except:
        writeIndex()
        print("O arquivo Entries/index.txt não existe... Tente novamente")

def errorMessage(values = "", evento = ""):
    if not values["RegEnter"] and evento == "telaIncReg" or evento == "telaIncRemover" or evento == "telaIncEditar" or evento == "telaIncVisualizar":
        return "Selecione um registro"
    values.pop("RegEnter")
    # constrói a menssagem de erro
    plural = True
    done = False
    c = 1
    # define o offset para localizar a vírgula
    empty = 0
    for key in values:
        if values[key] == "":
            empty += 1

    if not values["Banco"] and empty == 2:
        plural = False
    if values["Banco"]:
        if empty == 1:
            plural = False
        empty += 1

    offset = len(values)-empty

    if offset == 3:
        return

    while (True and not done):
        if (plural):
            erro = "Os campos: "

            for key in values:
                if not values[key] and key != "Banco":
                    c += 1
                    erro += key.lower()

                    if len(values) - c > 1+offset:
                        erro += ","
                    elif len(values) - c > offset:
                        erro += " e"

                    erro += " "

                if (key == "Banco"):
                    erro += "têm que ser preenchidos"
                    done = True
                    break
        else:
            erro = "O campo "
            for key in values:
                if not values[key] and key != "Banco":
                    erro += key.lower()
            erro += " tem que ser preenchido"
            break
    return erro
