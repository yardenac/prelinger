#!/usr/bin/python3
# http://museumca.org/mashup

import json
import ssl
import string
import urllib.request

cols = ',avg_rating,call_number,collection,contributor,coverage,creator,date,description,downloads,foldoutcount,format,headerImage,identifier,imagecount,language,licenseurl,mediatype,month,num_reviews,oai_updatedate,publicdate,publisher,rights,scanningcentre,source,subject,title,type,volume,week,year'

def getlist(buffer = True, filename = 'all.json', limit = 2147483647):
    """
    buffer - read from file? (always writes)
    """

    # https://archive.org/advancedsearch.php?q=collection:prelinger
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

# getvidmeta
# https://archive.org/details/identifier&output=json

docs = json.loads(getlist(buffer=True))['response']['docs']

# fill in data gaps
for doc in docs:
    if not 'date' in doc and not 'year' in doc:
        doc['date'] = '0000-01-01T00:00:00Z'
        doc['year'] = '0000'
    elif not 'date' in doc: doc['date'] = str(doc['year']) + '-01-01T00:00:00Z'
    elif not 'year' in doc: doc['year'] = int(doc['date'][:4])
    for col in cols.split(','):
        if not col in doc:
            doc[col] = None

# iterate by date
for doc in sorted(docs, key=lambda d: d['date']):
    print(str(doc['date']) + "  " + str(doc['year']) + "     " + doc['identifier'])
