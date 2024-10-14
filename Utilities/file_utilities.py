#LoadHashData, AddHashData, FileDetected, LoadWhiteLost, AddToWhiteList  van aqui junto a los relacionados
import os





def FileDetected(archivo, BadArchiveStorage):
    try:
        with open(BadArchiveStorage, 'r') as File:
            Archives = {line.strip() for line in File}
            return archivo in Archives
    except FileNotFoundError:
        return False
    
def LoadWhiteList(WhiteListDr):
    try:
        with open(WhiteListDr) as File:
            WhiteList = {line.strip() for line in File if line.strip()}
            return WhiteList
    except(FileNotFoundError, NameError) as ex:
        print(f"Error:: Unexpected error found on reading:: {ex}")
        return set()

def AddToWhiteList(WhiteListDr, Archive):
    with open(WhiteListDr, 'a') as Add:
        Add.write(Archive + '\n')
    print(f"File {Archive} set to White List.")

def TypeArchivesAllowed(Archive):
    AllowedArchiveType = ['.txt', '.json', '.config']
    return any(Archive.endswith(Type) for Type in AllowedArchiveType)


def DelDeleted(ListaDetectados, Delete):
    try: 
        #abre la lista de detectados
        with open(ListaDetectados, 'r') as File:
            lines = File.readlines()

        DividedLines = [line for line in lines if Delete not in line]

        with open(ListaDetectados, 'w') as File:
            File.writelines(DividedLines)

        print(f"El archivo/documento {ListaDetectados} fue borrado exitosamente")
    
    except FileNotFoundError:
        print(f"El archivo/documento {ListaDetectados} no fue encontrado en la lista")
    
    except Exception as ex:
        print(f"Error, excepcion {ex}")