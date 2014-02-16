#!/usr/bin/python3
# http://museumca.org/mashup

import json
import ssl
import string
import urllib.request

def getlist(buffer = True, filename = 'all.json', limit = 2147483647):
    """
    buffer - read from file? (always writes)
    """

    # https://archive.org/advancedsearch.php?q=collection:prelinger
    cols = ',avg_rating,call_number,collection,contributor,coverage,creator,date,description,downloads,foldoutcount,format,headerImage,identifier,imagecount,language,licenseurl,mediatype,month,num_reviews,oai_updatedate,publicdate,publisher,rights,scanningcentre,source,subject,title,type,volume,week,year'
    url = 'https://archive.org/advancedsearch.php?q=collection:prelinger&output=json' \
          + '&rows=' + str(limit) + cols.replace(',','&fl%5B%5D=')

    try:
        if buffer:
            with open(filename,"r") as file:
                full = file.read()
                file.close()
        else:
            raise IOError()
    except IOError:
        with open(filename,"w") as file:
            full = urllib.request.urlopen(url,capath="/etc/ssl/certs").read().decode()
            file.write(full)
            file.close()

    return full

#for doc in json.loads(getlist(buffer=False,limit=5))['response']['docs']:
for doc in json.loads(getlist(buffer=True))['response']['docs']:
    id = doc['identifier']
    try:
        format = doc['format']
    except KeyError:
        format = "[NOFORMAT]"
    print( id + "\n   " + str(format))
