from transformers import pipeline
import requests
from pprint import pprint

nlp = pipeline('ner', grouped_entities=True)

def visiableText(page):
    from bs4 import BeautifulSoup, Comment
    import re
    soup = BeautifulSoup(page, 'lxml')
    comm = soup.findAll(text=lambda text:isinstance(text, Comment))
    [c.extract() for c in comm]
    alltags = soup.findAll(text=True)
    visable_tags = [t for t in alltags if t.parent.name not in ['style', 'script','script','img', 'head', 'title', 'meta','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]
    visible =  ' '.join(visable_tags)
    return visible

def nerpage(url):
    try:
        res = requests.get(url, timeout = 10)
    except:
        return {'error':f'failed to connect the url {url}'}
    vis = visiableText(res.content)
    corpus = vis.split('\n')
    print(f'corpus has {len(corpus)} sentences')

    result = nlp(vis)

    result = filter(lambda x: x['score']>0.45 and '#' not in x['word'] 
                    and len(r['word'])>1, result)
    result = sorted(result, key = lambda x: x['score'] , reverse=True)
    
    resultdedup = []
    word = []
    for rs in result:
        if rs['word'] in word:
            continue
        word.append(rs['word'])
        resultdedup.append(rs)
    return resultdedup

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/Apache'
    print('starting ner')
    resultdedup = nerpage(url)
    pprint(resultdedup)
