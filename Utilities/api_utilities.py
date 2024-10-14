#CheckVirusAPI va aqui

import requests

def CheckVirusAPI(HashCodeT, API_Key):
    
    url = f"https://www.virustotal.com/api/v3/files/{HashCodeT}"
    Headers = {"x-apikey": API_Key}

    try:
        Respond = requests.get(url, headers=Headers)
        if Respond.status_code == 200:
            JsonResponse = Respond.json()
            #si algunos de los atributos inferiores es mayor a 0 entonces si es malicioso
            #esto ya que el api indica que otros antivirus lo han detectado asi.
            if JsonResponse['data']['attribute']['last_analysys_stats']['malicious'] > 0:
                return True

    except Exception as ex:
        print(f"Excepcion/Exclusion al realizar la solicitud a VirusTotal: {ex}")
        print(f"{ex} Es un archivo que puede no ser malicioso o que hubo algun error en la consulta...")
        print(" ")
        return False
    

def SafeBrowsingAPIG(url, APIKey):
    APIURL = "safebrowsing.googleapis.com/v4/threatMatches:find"

    #Datos para la Solicitud

    DatatoSend = {
        "Client": {
            "clientId": "Cyz arl",
            "clientVersion": "1.0"
        },
        "threatInfo":{
            "threatTypes":["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes:": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    #hacer solicitud
    answer = requests.post(f"{APIURL}?key={APIKey}", json=DatatoSend)

    if answer.status_code == 200:
        Results = answer.json()

        #vasicamente si en lo que nos llegue a answer tiene "matchea" entonces es verdadero
        if "matches" in answer:
            return True
        #basicamente si matecha con los datos de malware de google regresara un valor verdadero
        # si no matchea regresara un valor de malware negativo indicando que no es peligroso
        else:
            return False
    else:
        print(f"Error en la informacion: {answer.status_code}, {answer.text}")
        return False