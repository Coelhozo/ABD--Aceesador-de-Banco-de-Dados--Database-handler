import telas.requestTela as requestTela

def telaInicial(values, evento):
    if runCheck(values):
        if evento == "regBD":
            nome = requestTela.request(2, "save")
            saveEntry(values, nome)
    else:
        # constroi a menssagem de erro
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


def runCheck(values):
    # confere se os campos foram preenchidos
    for key in values:
        if not values[key]:
            # se o valor vazio não for do campo -BD-, retorne falso
            if not key == "Banco":
                return False
    return True


def saveEntry(values, nome):
    filename = "Entries/"+nome["nome"]+".txt"
    with open(filename, "a") as file:
        file.write(
            f"""Usuario: {values["Usuário"]}
Senha: {values["Senha"]}
Host: {values["Host"]}
Banco: {values["Banco"]}"""
        )
