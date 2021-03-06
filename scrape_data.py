import json, os
import scrapy
import html2text

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

class FAQSpider(scrapy.Spider):
    name = "faqs"
    start_urls = [
        'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/fragor-och-svar/'
    ]

    def parse(self, response):
        
        print('Running parser...')
        
        questions = response.css('div.content-3').css('span.accordion__item__title__text').getall()

        answers = response.css('div.content-3').css('div.textbody').getall()

        faq_list = [{'question': html2text.html2text(q).replace('\n', ' '),
                     'answer': html2text.html2text(a).replace('\n', ' '),
                     'source': response.url}
                    for q, a in zip(questions, answers)]

        filename = 'faq-info-coronavirus.json'
       
        if not os.path.isdir('output'): os.mkdir('output')

        with open(os.path.join('output', filename), 'w') as f:
            json.dump(faq_list, f)


if __name__ == "__main__":
    runner = CrawlerRunner()
    deferred = runner.crawl(FAQSpider)
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()