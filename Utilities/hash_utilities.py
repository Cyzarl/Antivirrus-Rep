#calcular Hash va aqui junto a todo lo relacionado
import hashlib

def CalcularHash(archivo, algoritmo = 'sha256'):
    HashAlgoritmo = hashlib.new(algoritmo)
    with open(archivo, 'rb') as file:
        chunk = file.read(8192)
        while chunk:
            HashAlgoritmo.update(chunk)
            chunk = file.read(8192)
    return HashAlgoritmo.hexdigest()

def LoadHashData(FileRoute):
    try:
        with open(FileRoute, 'r') as file:
            hashes = {line.strip() for line in file if line.strip()}
            return hashes
    except(FileNotFoundError, IOError) as error:
        print(f"Error al leer el archivo de base de datos {error}")
        print(" ")
        return set()

def AddHashToData(FileRoute, HashCode):
    with open(FileRoute, 'a') as file:
        file.write(HashCode + '\n')