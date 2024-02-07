entriesPATH = "entries/data/"
def getEntry(nome=None):
    filename = entriesPATH+f"{nome}/{nome}.txt" if nome else "dbVariables.txt"
    with open(filename, 'r') as entry:
        i = entry.read()
    data = i.split('\n')
    valores = [item.split(': ') for item in data]
    
    oldRecords = {}
    for item in valores:
        oldRecords[item[0]] = item[1]
    return oldRecords