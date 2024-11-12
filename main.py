import os
import shutil
from scanner import EscaneoCarpetas
from Utilities.hash_utilities import CalcularHash, LoadHashData, AddHashToData
from Utilities.file_utilities import TypeArchivesAllowed, FileDetected, DelDeleted, LoadWhiteList, AddToWhiteList 
from Utilities.api_utilities import CheckVirusAPI
import time

if __name__ == '__main__':

    API_Key = 'YourAPIKeyHere'
    SafeBrowsingAPIG = 'AIzaSyCnkuMdt-S6SPlvbDBQ8-EQtFupz0sdmD8'

    HashDataRoute = 'Data/BaseDatosHash.txt'

    BaseDatosHash = LoadHashData(HashDataRoute)

    WhiteListArchive = 'Data/WhiteList.txt'

    
    Entrada = input('Ingrese el directorio or URL que desea escanear: ')
    
    ArchivoEscanear = fr'{Entrada}'
   


    TreatsFound = EscaneoCarpetas(ArchivoEscanear, BaseDatosHash, API_Key, WhiteListArchive, SafeBrowsingAPIG)

    if TreatsFound:
        print("Archivos Maliciosos encontrados: ")

        for threat in TreatsFound:
            ThreatsDeleted = 0
            print(threat)
            
            try:
                Delete = input("Le gustaria Borrar los archivos maliciosos encontrados? s/n: ")
                print(" ")
                if Delete.lower() == 's':
                    print("Borrando archivos maliciosos.")
                    print(" ")
                    BadArchiveStorage = 'Data/ListaDetectados.txt'

                    with open(BadArchiveStorage, 'r') as file:
                        NamesRead = {line.strip() for line in file if line.strip()}

                        for EachArchive in NamesRead:

                            if os.path.exists(EachArchive):
                                os.remove(EachArchive)
                                print(f"La carpeta {EachArchive} ha sido eliminada")
                                DelDeleted(BadArchiveStorage , EachArchive)
                                ThreatsDeleted = ThreatsDeleted + 1
                                print(" ")

                            elif os.path.isdir(EachArchive):
                                shutil.rmtree(EachArchive)
                                print(f"La carpeta {EachArchive} se borro")
                                DelDeleted(BadArchiveStorage, EachArchive)


                            else:
                                print(f"La carpeta {EachArchive} no existe o ya ha sido eliminado")
                                print(" ")
   

                elif Delete.lower() == 'n':
                    print("Comprendido! Los archivos no se borraran.")
                    break
            
            except Exception as Ex:
                print(f"Error {Ex}")
        
        print(f"Amenazas totales Borradas: {ThreatsDeleted}")
    else:
        print("No se encontraron amenazas.")
