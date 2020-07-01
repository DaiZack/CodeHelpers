import requests
import pandas as pd

totalcorps = 109629

def getCorp(limit=2000, offset=0, searchTerm=''):
    filters = ''
    if searchTerm:
        filters = 'FILTER ( REGEX(str(?company), "%s", "i") ) ' % searchTerm
    query ='''
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?company ?headquarter ?netIncome ?numberOfEmployees ?revenue \
                    ?foundingYear ?country ?locationCity ?keyPerson
    WHERE { ?company a dbo:Company .
            optional {?company dbo:country ?country} .
            optional {?company dbo:keyPerson ?keyPerson} .
            optional {?company dbo:locationCity ?locationCity} .
            optional {?company dbo:headquarter ?headquarter} .
            optional {?company dbo:netIncome ?netIncome} .
            optional {?company dbo:numberOfEmployees ?numberOfEmployees} .
            optional {?company dbo:revenue ?revenue} .
            optional {?company dbo:revenue ?foundingYear} .
            %s
    }
    LIMIT 2000
    offset 2000
    ''' % filters

    params = (
        ('default-graph-uri', 'http://dbpedia.org'),
        ('query', query),
        ('output', 'json'),
    )
    response = requests.get('http://dbpedia.org/sparql', params=params)
    data = response.json()['results']['bindings']
    dataJ = [{k:d[k]['value'].replace('http://dbpedia.org/resource/','').replace('_',' ') for k in d} for d in data]
    return pd.DataFrame(dataJ)

df = getCorp()
df.to_csv('DBcorps.csv', index=0, header=1, mode='a')
