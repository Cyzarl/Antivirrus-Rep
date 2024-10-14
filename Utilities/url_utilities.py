import re
def ScanUrl(url):
    UrlVerif = re.compile(
        r'^(http?://)?' #revisa el https
        r'([a-zA-Z0-9.-]+)' #evalua el dominio
        r'(\.[a-zA-Z]{2.6})' #valua la extension del dominio
        r'(/[a-zA-Z0-9._-]+)*$' #evalua lo que resta de la url
    )

    return re.match(UrlVerif, url) is not None