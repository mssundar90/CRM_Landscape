import scrapy

class CapterraSpider(scrapy.Spider):
    name = 'CapterraSpiderProject2'
    start_urls = [
    	'https://www.capterra.com/customer-relationship-management-software/'
    	]

    def parse(self, response):
        for sw in response.css('.spotlight-link'):
            href = sw.css('::attr(href)').extract()[0]

            productId = href[3:href.index('/',3)]

            # yield {
            # 'href': sw.css('::attr(href)').extract(),
            # }

            yield {
            'productId' : productId
            }
