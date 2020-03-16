import scrapy, re, os
from scrapy import Spider
from scrapy.exceptions import CloseSpider
from MongoDAO import articleDB
from pymongo.errors import DuplicateKeyError

from correctDate import correctDate

##############################################################################################################################################
##########################################################  Functions    #####################################################################
##############################################################################################################################################

def get_links():
    text_path = './tempinfo.csv'

    with open(text_path, 'r') as o:
        links = o.read().split('\n')

    os.remove(text_path)
    lenCsv = len(links)
    return links, lenCsv

def fix_link(mylink):
    if 'bbc' in mylink:
        myNewlink = re.sub(r'(^.*?bbc.*?\/)', '', mylink)

    elif mylink.startswith('1.globo'):
        myNewlink = 'https://g' + mylink

    elif mylink.startswith('g1.globo') or mylink.startswith('.abril'):
        myNewlink = 'https://' + mylink

    else:
        myNewlink = mylink

    return myNewlink

def getXpath(response, mylink):
    if '1.globo.com' in mylink:
        if str(mylink).endswith('.ghtml'):
            title = response.xpath("//div[contains(@class, 'title')]/h1/text()").extract_first()
            subtitle = response.xpath("//div[contains(@class, 'subtitle')]/h2/text()").extract_first()
            date = response.xpath("//time/text()").extract_first()
            article = response.xpath("//article").extract_first()

        elif str(mylink).endswith('.html'):
            title = response.xpath("//h1/text()").extract_first()
            subtitle = response.xpath("//h2/text()").extract_first()
            date = response.xpath("//abbr[contains(@class, 'published')]/text()").extract_first()
            article = response.xpath("//div[contains(@class, 'materia-conteudo')]").extract_first()

        article = re.sub(r'(<script[\w\W]*?script>)', '', article)
        article = re.sub(r'(<[\w\W]*?>)', ' ', article)
        article = re.sub(r' {2,}', '\n', article)

    elif 'bbc.co' in mylink:
        finder = re.compile(r'<p>(?!<.*?>)(.*?)<\/p>')

        title = response.xpath("//h1/text()").extract_first()
        subtitle = response.xpath("//p[contains(@class, 'story-body__introduction')]//text()").extract_first()
        date = response.xpath("//div[contains(@class, 'date date--v')]/text()").extract_first()
        article = response.xpath("//div[contains(@class, 'story-body__inner')]").extract_first()

        article = '\n'.join([match.group(1)
                                for match in re.finditer(finder, article)])

    elif '.abril' in mylink:

        title = response.xpath("//article/header/h1/text()").extract_first()
        subtitle = response.xpath("//article/header/h2/text()").extract_first()
        date = response.xpath("//article/header/*/div[contains(@class, 'article-date')]/span/text()").extract_first()
        article = response.xpath("//article/section[contains(@class, 'article-content')]/p").extract()

        date = date.strip()

        article = '\n'.join([art for art in article])
        article = re.sub(r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)|(\s{2,})|ADVERTISING|AdChoices', '', article)

    elif 'epoca.globo' in mylink:

        title = response.xpath("//section[contains(@class, 'materia-interna')]/header/div/div[1]/a/h1/text()").extract_first()
        subtitle = response.xpath("//section[contains(@class, 'materia-interna')]/header/div/div[1]/h3/text()").extract_first()
        date = response.xpath("//section[contains(@class, 'materia-interna')]/header/div/div[1]/div/div[2]/text()").extract_first()
        article = response.xpath("//article[contains(@class, 'conteudo')]").extract()

        subtitle = subtitle.strip()

        date = date.strip()

        article = '\n'.join(article)
        article = re.sub(r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)|(\s{2,})|ADVERTISING|AdChoices', ' ', article)

    elif 'estadao.com.br'in mylink:
        title = response.xpath("//article[contains(@class, 'n--noticia__header')]/h1/text()").extract_first()
        subtitle = response.xpath("//article[contains(@class, 'n--noticia__header')]/h2/text()").extract_first()
        date = response.xpath("//div[contains(@class, 'box area-select')]/div[1]/div/p/text()").extract_first()
        article = response.xpath("//div[contains(@class, 'box area-select')]/div[3]/p").extract()

        article = '\n'.join(article)
        article = re.sub(r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)|(\s{2,})|ADVERTISING|AdChoices', ' ', article)


    article = re.sub(r'(\s)+', ' ', article)
    article = '\t' + article

    return title, subtitle, date, article

    
##############################################################################################################################################
##########################################################  Spider    ########################################################################
##############################################################################################################################################

class addLink(scrapy.Spider):
    name = 'InfoCrawler'

    start_urls, lenCsv = get_links()

    linksAdd = 0
    linksChecked = 0
    linksFailed = 0

    def parse(self, response):
        mylink = response.url[8:]

        myNewLink = fix_link(mylink)

        title, subTitle, date, article = getXpath(response, mylink)

        try:
            self.linksChecked += 1
            if title != '' and article != '' and date != '' and not myNewLink.startswith('link'):
                with articleDB('News2') as adb:
                    obj = {
                        'Title': title or '',
                        'SubTitle': subTitle or '',
                        'Date': correctDate(str(date)) or '',
                        'Link': myNewLink or '',
                        'Article': article or '',
                        'Source': 'G1',
                        'Type': 'Não avaliado'
                    }
                    adb.insert_one(obj)
                    self.linksAdd += 1

            else: self.linksFailed += 1

        except DuplicateKeyError as e:
            self.linksFailed += 1
            print('\t --> Link já adicionado ao banco!\n\t\t-> {0}'.format(e))



    def closed(self,reason):
        print('\n\n\n\t --> {0} links foram adicionados ao mongoDB.\n\n'.format(self.linksAdd))
        print('\n\t --> {0} links já estavam no banco.\n\n'.format(self.linksFailed))
        print('\n\t --> {0} links foram verificados.\n\n'.format(self.linksChecked))
        print('\n\t --> {0} links foram pegos na busca.\n\n'.format(self.lenCsv))