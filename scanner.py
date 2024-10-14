import os
import time
from Utilities.hash_utilities import CalcularHash, AddHashToData
from Utilities.file_utilities import TypeArchivesAllowed, FileDetected, DelDeleted ,LoadWhiteList, AddToWhiteList
from Utilities.api_utilities import CheckVirusAPI, SafeBrowsingAPIG
from Utilities.url_utilities import ScanUrl
def EscaneoCarpetas(FileOrURL, BaseDatosHash, API_Key, WhiteListArchive, SBrowsergAPIG):
    threats = []
    WhiteList = LoadWhiteList(WhiteListArchive)
    BadArchiveStorage = 'Data/ListaDetectados.txt'
    AmountOfDetected = 0

    if ScanUrl(FileOrURL):
        print(f"Verificando la URL {FileOrURL}")
        if SafeBrowsingAPIG(FileOrURL, SBrowsergAPIG):
            print(f"La URL {FileOrURL} es malicioso!")
            AmountOfDetected = AmountOfDetected + 1
            threats.append(FileOrURL)

            if FileDetected(FileOrURL, BadArchiveStorage):
                print(f"La URL maliciosa ya e habia registrado")
            
            else:
                with open(BadArchiveStorage, 'a') as DataNameFile:
                    DataNameFile.write(FileOrURL + '\n')
                print(f"La URL malicosa {FileOrURL} se agrego en la lista.")
        else:
            print(f"La URL {FileOrURL} es segura")
        
        return threats
            
   
   
    for root, dirs, files in os.walk(FileOrURL):
        time.sleep(2)
        for archivo in files:
            RutaCompleta = os.path.join(root, archivo)
            BadArchiveStorage = 'Data/ListaDetectados.txt'
            #convierte en harsh los archivos del directorio
            ArchivoHash = CalcularHash(RutaCompleta)

            if TypeArchivesAllowed(archivo):
                print(f"El documento {archivo} es de un tipo permitido.")

            

                #verifica si anda en la lista blanca o no
                if RutaCompleta in WhiteList:
                    print(f"{archivo} encontrado en la lista blanca, no se escaneara")
                    continue#salta el archivo

                
                
            #en esta transicion desde aqui y el else, si al final detecta el virus
            #al no cumplir con la condicion pasara al bloque del 'else'

                if not CheckVirusAPI(ArchivoHash, API_Key):
                    print(f"El Documento {archivo} es seguro, se transferira a la lista blanca")
                    AddToWhiteList(WhiteListArchive, RutaCompleta)

            
            else:
                #en caso que no sea un tipo permitido(otra cosa que no sea .txt.json.config):
                if RutaCompleta in WhiteList:
                    print(f"{archivo} encontrado en la lista blanca, se ignorara")
                    continue




                if ArchivoHash in BaseDatosHash:
                    print(f"El archivo {archivo} es malicioso!")
                    threats.append(RutaCompleta)
                    AmountOfDetected = AmountOfDetected + 1
                    print(" ")
                    #'a' agrega texto sin borrarlo en el .txt
                    if FileDetected(RutaCompleta, BadArchiveStorage):
                        print("No se guardo el Archivo malicioso en la lista, pues ya esta en el.")
                
                    else: 
                        with open(BadArchiveStorage, 'a') as DataNameFile:
                            #'\n' Escribe el texto en una nueva linea en la base de datos txt
                            DataNameFile.write(RutaCompleta + '\n')
                
                
            
            #en caso que no este en la base de datos
                else: 
                    print(f"Verificando el archivo {archivo} en VirusTotal...")
                    if CheckVirusAPI(ArchivoHash, API_Key):
                        print(f"El archivo {archivo} es malicioso.")
                        AmountOfDetected = AmountOfDetected + 1
                        print(" ")
                        #guarda el hash a la base de datos local
                        threats.append(RutaCompleta)
                        AddHashToData('BaseDatosHash.txt', ArchivoHash)

                    
                        if FileDetected(RutaCompleta, BadArchiveStorage):
                            print(f"No se guardo el Archivo malicioso en la lista, pues {archivo} ya esta en el.")                   
                    
                        else:
                            #'a' agrega texto sin borrarlo en el .txt
                            with open(BadArchiveStorage, 'a') as DataNameFile:
                            #'\n' Escribe el texto en una nueva linea en la base de datos txt
                                DataNameFile.write(archivo + '\n')
                            print(f"El archivo malicioso {archivo} se agrego a la lista de archivos malicioso.")
                     
                    else:
                        print(f"El archivo {archivo} no fue detectado como amenaza.")
                        print(" ")
    
    print(f"{AmountOfDetected} amenazas maliciosas fuerin detectadas")

    return threats