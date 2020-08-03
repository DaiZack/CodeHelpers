import scrapy, json
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from unidecode import unidecode

result = []
domain = 'rel8ed.to'

def visiableText(page):
    from bs4 import BeautifulSoup, Comment
    import re
    soup = BeautifulSoup(page, 'lxml')
    comm = soup.findAll(text=lambda text:isinstance(text, Comment))
    [c.extract() for c in comm]
    alltags = soup.findAll(text=True)
    visable_tags = [t for t in alltags if t.parent.name not in ['style', 'script','script','img', 'head', 'title', 'meta','link','footer','base','applet','iframe','embed','nodembed','object','param','source','[document]']] 
    visable = ' '.join(visable_tags)
    # visable = re.sub(r'\s+',r' ', visable)
    visable = re.sub(r'\W*\n\W*',r'\n', visable)
    return visable

class MySpider(CrawlSpider):
    name = domain
    allowed_domains = [domain]
    start_urls = [f'http://{domain}']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        line = {
            "domain":self.name,
            "url":response.url,
            "content":unidecode(visiableText(response.body))
        }
        result.append(line)

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(MySpider)
process.start()

with open(f'webdata/{domain}.json', 'w') as f:
    json.dump(result,f)
