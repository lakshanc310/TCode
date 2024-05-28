import scrapy

class CralwerListing(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']
    def parse(self,response):
        title= response.css('title::text').extract()
        yield {'titletext':title}
#'http://quotes.toscrape.com/',