def visiablePage(url):
    import requests, re
    from bs4 import BeautifulSoup, Comment
    url = 'http://'+re.sub(r'^.*https?:?/+','', url)
    try:
      page = requests.get(url).content
    except:
      print('page not found')
      return ''
    soup = BeautifulSoup(page, 'lxml')
    comm = soup.findAll(text=lambda text:isinstance(text, Comment))
    [c.extract() for c in comm]
    alltags = soup.findAll(text=True)
    visable_tags = [t for t in alltags if t.parent.name not in ['style', 'script','script','img', 'head', 'title', 'meta','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']]
    visible =  ' '.join([re.sub(r'[\n\s\r\t/]+',' ', t) for t in visable_tags])
    return re.sub(r'\s+', ' ', visible)

def SVO(text, sentiment=False):
  if not text:
    print('no text found')
    return
  import pandas as pd
  import spacy, textacy
  from textblob import TextBlob
  doc = nlp(text)
  out = []
  for sent in doc.sents:
    elements = list(textacy.extract.subject_verb_object_triples(sent))
    if sentiment:
      score = TextBlob(' '.join([d.text for d in sent])).sentiment.polarity
      elements = [(e[0],e[1],e[2], score) for e in elements]
    out += elements
  columns=['Subject','Verb','Object']
  if sentiment:
    columns.append('Sentiment')
  df = pd.DataFrame(out, columns=columns)
  return df

def SVOpage(url, sentiment=False):
  return SVO(visiablePage(url), sentiment)

def SVOfile(path, sentiment=False):
  try:
    with open(path) as f:
      text = f.read()
  except:
    print('bad file path!')
    return
  if not text:
    print('empty file!')
    return
  return SVO(text, sentiment)
