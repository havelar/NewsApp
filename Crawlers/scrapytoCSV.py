import scrapy, re, pymongo
import pandas as pd
from DAO import autoConnect
from MongoDAO import articleDB
from pymongo.errors import WriteError


def get_links():
    with autoConnect() as cursor:
        cursor.execute(
            'SELECT link from links where tipo in (1,2,3)')
        links = [link[0] for link in cursor.fetchall()]
        return links


class addLink(scrapy.Spider):
    name = 'InfoCrawler'

    start_urls = get_links()

    df = pd.DataFrame(columns=['Title', 'SubTitle',
                               'Date', 'Article', 'Type', 'link'])

    def parse(self, response):
        mylink = response.url[8:]

        if 'bbc' in mylink:
            myNewlink = re.sub(r'(^.*?bbc.*?\/)', '', mylink)

        elif mylink.startswith('1.globo'):
            myNewlink = 'https://g' + mylink

        elif mylink.startswith('g1.globo') or mylink.startswith('veja.abril'):
            myNewlink = 'https://' + mylink

        else:
            myNewlink = mylink

        with autoConnect() as cursor:
            cursor.execute(
                'select tipo from links where link LIKE "%{0}%"'.format(myNewlink))
            status = cursor.fetchone()[0]
            tipo = 'Bom' if status == 1 else 'Ruim' if status == 2 else 'Sem valor'

        if '1.globo.com' in mylink:
            if str(mylink).endswith('.ghtml'):
                title = response.xpath(
                    "//div[contains(@class, 'title')]/h1/text()").extract_first()
                subtitle = response.xpath(
                    "//div[contains(@class, 'subtitle')]/h2/text()").extract_first()
                date = response.xpath("//time/text()").extract_first()
                article = response.xpath("//article").extract_first()

            elif str(mylink).endswith('.html'):
                title = response.xpath("//h1/text()").extract_first()
                subtitle = response.xpath("//h2/text()").extract_first()
                date = response.xpath(
                    "//abbr[contains(@class, 'published')]/text()").extract_first()
                article = response.xpath(
                    "//div[contains(@class, 'materia-conteudo')]").extract_first()

            article = re.sub(r'(<script[\w\W]*?script>)', '', article)
            article = re.sub(r'(<[\w\W]*?>)', ' ', article)
            article = re.sub(r' {2,}', '\n', article)

        elif 'bbc.co' in mylink:
            finder = re.compile(r'<p>(?!<.*?>)(.*?)<\/p>')

            title = response.xpath("//h1/text()").extract_first()
            subtitle = response.xpath(
                "//p[contains(@class, 'story-body__introduction')]//text()").extract_first()
            date = response.xpath(
                "//div[contains(@class, 'date date--v')]/text()").extract_first()
            article = response.xpath(
                "//div[contains(@class, 'story-body__inner')]").extract_first()

            article = '\n'.join([match.group(1)
                                 for match in re.finditer(finder, article)])

        elif 'veja.abril' in mylink:

            title = response.xpath(
                "//article/header/h1/text()").extract_first()
            subtitle = response.xpath(
                "//article/header/h2/text()").extract_first()
            date = response.xpath(
                "//article/header/*/div[contains(@class, 'article-date')]/span/text()").extract_first()
            article = response.xpath(
                "//article/section[contains(@class, 'article-content')]/p").extract()

            date = date.strip()

            article = '\n'.join([art for art in article])
            article = re.sub(
                r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)|(\s{2,})|ADVERTISING|AdChoices', '', article)

        elif 'epoca.globo' in mylink:

            title = response.xpath(
                "//section[contains(@class, 'materia-interna')]/header/div/div[1]/a/h1/text()").extract_first()
            subtitle = response.xpath(
                "//section[contains(@class, 'materia-interna')]/header/div/div[1]/h3/text()").extract_first()
            date = response.xpath(
                "//section[contains(@class, 'materia-interna')]/header/div/div[1]/div/div[2]/text()").extract_first()
            article = response.xpath(
                "//article[contains(@class, 'conteudo')]").extract()

            subtitle = subtitle.strip()

            date = date.strip()

            article = '\n'.join(article)
            article = re.sub(
                r'(<script(\s|\S)*?<\/script>)|(<style(\s|\S)*?<\/style>)|(<!--(\s|\S)*?-->)|(<\/?(\s|\S)*?>)|(\s{2,})|ADVERTISING|AdChoices', ' ', article)

        # print(article)
        # print(title)
        # print(subtitle)
        # print(date)

        article = re.sub(r'(\s)+', ' ', article)
        article = '\t' + article

        self.df = self.df.append({
            'Title': title,
            'SubTitle': subtitle,
            'Date': date,
            'Article': article,
            'Type': tipo,
            'Link': mylink
        }, ignore_index=True)

    def closed(self, reason):
        df = self.df
        print(df)
        with articleDB('News') as adb:
            for i in range(len(df)):
                try:
                    adb.insert_one({
                        'Title': df['Title'][i] or '',
                        'SubTitle': df['SubTitle'][i] or '',
                        'Date': df['Date'][i] or '',
                        'Link': df['Link'][i] or '',
                        'Article': df['Article'][i] or '',
                        'Type': df['Type'][i]
                    })
                except WriteError as e:
                    print('Erro de validação: {0}'.format(e))

        # self.df.to_csv('links4training.csv', i ndex=False)
