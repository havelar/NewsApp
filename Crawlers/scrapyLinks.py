# -*- coding: utf-8 -*-

import scrapy
import re, requests, os

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector



##############################################################################################################################################
##########################################################  Functions    #####################################################################
##############################################################################################################################################
def globoLinks(assunto, pgs):

    link = 'https://g1.globo.com/busca/?q={0}'.format('-'.join(assunto.split()))

    resp_link = requests.get(link)
    li_div = Selector(text=resp_link.text).xpath("//li[contains(@class, 'widget widget--card widget--navigational')]").extract_first()
    Regxr = re.compile('tudo-sobre%2F(.*)%2F')
    match = Regxr.search(li_div or '')

    text = '+'.join(assunto.split(' '))

    if match and False:
        match = match.group(1)
        tudoSobre = 'https://g1.globo.com/tudo-sobre/{0}/index/feed/pagina-1.ghtml'.format(match)
        print('\t' + tudoSobre)

        resp_tudo = requests.get(tudoSobre)
        checker = Selector(text=resp_tudo.text).xpath("//div[contains(@class, 'theme')]/div[contains(@id, 'bstn-launcher')]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[contains(@class, 'bastian-page')]").extract_first() 

        check_rgx = re.compile('<div class="_xn"></div>')

        check = check_rgx.search(checker)
        if not check:
            print("\n\n\tUtilizando a aba de 'tudo-sobre'")
            return ['https://g1.globo.com/tudo-sobre/{0}/index/feed/pagina-{1}.ghtml'.format(match, pg) for pg in range(1, pgs+1)]
        else:
            return ['https://g1.globo.com/busca/?q={0}&order={2}&species=notícias&page={1}'.format(text, pg, order) for pg in range(1, pgs+1) for order in ['relevant', 'recent']]
    else:
        return ['https://g1.globo.com/busca/?q={0}&order={2}&species=notícias&page={1}'.format(text, pg, order) for pg in range(1, pgs+1) for order in ['relevant', 'recent']]

def link_gen():
    links = []
    assuntos = []

    print('\n-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/')
    assunto = input("\n -> Digite o assunto da primeira busca: ")

    while assunto.lower() != 'parar' and assunto.lower() != '':
        pgs = input("\n -> Digite o número de páginas: ")
        while not pgs.isnumeric():
            pgs = input("\n -> ERROR: Digite um numero válido de páginas: ")

        assuntos.extend([ass.lower() for ass in assunto.split(' ')])
        pgs = int(pgs)

        text = '+'.join(assunto.split(' '))

        # Globo, bbc, veja, exame, epoca, estadao
        links.extend(globoLinks(assunto, pgs))
        #links.extend(['https://www.bbc.com/portuguese/search/?q={0}&start={1}'.format(text, ((pg-1)*10)+1) for pg in range(1, pgs+1)])
        #links.extend(['https://{3}.abril.com.br/pagina/{0}/?s={1}&orderby={2}'.format(pg, text, order, site) for pg in range(1, pgs+1) for order in ['post_date', 'relevance'] for site in ['veja', 'exame']])
        #links.extend(['https://epoca.globo.com/busca/?q={0}&species=notícias&page={1}'.format(text, pg) for pg in range(1, pgs + 1)])
        #links.extend(['https://busca.estadao.com.br/modulos/busca-resultado?modulo=busca-resultado&config%5Bbusca%5D%5Bpage%5D={0}&config%5Bbusca%5D%5Bparams%5D=tipo_conteudo%3DTodos%26quando%3D%26q%3D{1}&ajax=1'.format(pg, text) for pg in range(1, pgs+1)])
        
        # https://search.folha.uol.com.br/search?q=samarco&site=todos&periodo=todos&results_count=1131&search_time=0%2C247&url=http%3A%2F%2Fsearch.folha.uol.com.br%2Fsearch%3Fq%3Dsamarco%26site%3Dtodos%26periodo%3Dtodos&sr=76
        # Trocar onde for samarco e o ultimo argumento, cada pg tem 25, então é 1-26, 26-51, 51-76 ...

        print('\n\tSalvo!')
        print('\n-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/')
        print('\n -> Obs.:Para parar e continuar digite "Parar".\n')
        assunto = input(" -> Digite o assunto da proxima busca: ")

    return (links, assuntos)


def getXpath(response, mylink):
        if '1.globo.com' in mylink:
            if '1.globo.com/tudo-sobre/' in mylink:
                commonXpath = "//*[@id='feed-placeholder']/div/div/div[2]/div/div[contains(@class, 'bastian-page')]/div[contains(@class, '_xn')]/div[contains(@class, 'bastian-feed-item')]/div[contains(@class, 'feed-post bstn-item-shape type-materia')]/div[contains(@class, 'feed-post-body')]"
                titles = response.xpath(commonXpath + "/div[contains(@class, 'feed-post-body-title gui-color-primary gui-color-hover ')]/div[contains(@class, '_label_event')]/div[contains(@class, '_et')]/a/text()").extract()
                links = response.xpath(commonXpath + "/div[contains(@class, 'feed-post-body-title gui-color-primary gui-color-hover ')]/div[contains(@class, '_label_event')]/div[contains(@class, '_et')]/a/@href").extract()
                descriptions = response.xpath(commonXpath + "/div[contains(@class, 'feed-post-body-resumo')]/div[contains(@class, '_label_event')]/text()").extract()
            else:
                globoMainPath = "//ul[contains(@class, 'results__list')]//li/div[contains(@class, 'widget--info__text-container')]"
                links = response.xpath( globoMainPath + "/a/@href" ).extract()
                titles = response.xpath( globoMainPath + "/a/div[1]/text()" ).extract()
                descriptions = response.xpath( globoMainPath ).extract()

        elif 'bbc.com' in mylink:
            links = response.xpath('//div[contains(@class, "hard-news-unit hard-news-unit--regular faux-block-link")]/div[1]/h3/a/@href').extract()
            titles = response.xpath('//div[contains(@class, "hard-news-unit hard-news-unit--regular faux-block-link")]/div[1]/h3/a/text()').extract()
            descriptions = response.xpath('//div[contains(@class, "hard-news-unit hard-news-unit--regular faux-block-link")]/div[1]/p/text()').extract()

        elif '.abril.com' in mylink:
            links = response.xpath('//ul[contains(@class, "articles-list")]/li/div/span/a/@href').extract()
            titles = response.xpath('//ul[contains(@class, "articles-list")]/li/div/span/a/text()').extract()
            descriptions = ['No description.' for _ in range(1, len(links))]

        elif 'epoca.globo' in mylink:
            links = response.xpath("//ul[contains(@class, 'resultado_da_busca')]/li/div[1]/a/@href").extract()
            titles = response.xpath("//ul[contains(@class, 'resultado_da_busca')]/li/div[1]/a/text()").extract()
            descriptions = response.xpath("//ul[contains(@class, 'resultado_da_busca')]/li/div[1]/div/p").extract()

        elif 'estadao.com.br' in mylink:
            links = response.xpath("//div[contains(@class, 'lista')]/section/div[1]/div[contains(@class, 'row')]/section[1]/a/@href").extract()
            titles = response.xpath("//div[contains(@class, 'lista')]/section/div[1]/div[contains(@class, 'row')]/section[1]/a/h3/text()").extract()
            descriptions = response.xpath("//div[contains(@class, 'lista')]/section/div[1]/div[contains(@class, 'row')]/section[1]/a/p/text()").extract()

        
        return links, titles, descriptions


##############################################################################################################################################
##########################################################  Spider    ########################################################################
##############################################################################################################################################

class getLinks(scrapy.Spider):
    name = 'InfoCrawler'
    start_urls, assuntos = link_gen()
    links = []
    fake_links = []
    filtering_off = (False if input('\n\t --> Deseja ligar o filtro(S/N): ').lower() == 's' else True) if assuntos else True

    def parse(self, response):
        mylink = response.url[8:]

        dSpace = re.compile('[\s]+')
        
        links, titles, descriptions = getXpath(response, mylink)

        for link, title , description in zip(links, titles, descriptions):
            title = title.strip()

            description = re.sub(dSpace, ' ', description)

            if re.search(r'((g1|epoca)\.globo\.com(?!.*\2\.globo\.com).*\.g?html)', link):
                link = re.search(r'((g1|epoca)\.globo\.com(?!.*\2\.globo\.com).*\.g?html)', link).group(1)
                link = re.sub(r'%2F', '/', link)
                link = 'http://' + link
                description = re.sub(r'<[\w\W]*?>', ' ', description)


            print('\n\t-> LINK: \n')
            print('\t\t{}'.format(link))
            print('\n\t-> Title: \n')
            print('\t\t{}'.format(title))
            print('\n\t-> Description: \n')
            print('\t\t{}'.format(description))
            print('\n\t-> Status: \n')

            # Verifica relevancia do assunto
            if ((any(assunto in title.lower() for assunto in self.assuntos) or any(assunto in description.lower() for assunto in self.assuntos)) if description != 'No description.' else any(assunto in title.lower() for assunto in self.assuntos)) or self.filtering_off:
                if link.startswith('http'):
                    self.links.append(link)
                    print('\t\tLink sent to server')
                else:
                    self.fake_links.append(link)
                    print('\t\tBroken link')
            else:
                self.fake_links.append(link)
                print('\t\tNo value link')

            print(148*'#' + '\n' + 148*'#')

    def closed(self, reason):
        if self.links:
            text_path = './tempinfo.csv'
            with open(text_path, 'w') as o:
                o.write('\n'.join(self.links))

        if self.fake_links and False:
            print('\n ---> Esses links são de notícias não relevantes:')
            for link in self.fake_links:
                print('\n\t -> {0}'.format(link))
