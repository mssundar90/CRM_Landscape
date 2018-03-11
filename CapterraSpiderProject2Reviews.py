import scrapy
import os
from scrapy.http.request import Request
import json
import csv
import re
from textblob import TextBlob

DIRECTORY_NAME = 'project_2_product_reviews'


def cleanStr(str):
    '''
    Utility function to clean string by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str).split())

def getSentiment(str):
    '''
    Utility function to classify sentiment
    using textblob's sentiment method
    '''
    # create TextBlob object of passed string
    analysis = TextBlob(cleanStr(str))
    
    return analysis.sentiment.polarity

class CapterraSpider(scrapy.Spider):
    name = 'CapterraSpiderProject2'
    
    def start_requests(self):
      productIds = json.load(open('productIds.json'))
      # productIds = json.load(open('productIdsSample.json'))
      for productIdObj in productIds:
        for page in range(0,13):
            url = 'https://www.capterra.com/gdm_reviews?product_id=' + productIdObj['productId'] + '&page=' + str(page)
            yield Request(url, self.parse)

    def parse(self, response):
        url = response.url
        productId = url[url.index('product_id=') + len('product_id=') : url.index('&', url.index('product_id=') + len('product_id='))]
        reviews = []

        if not os.path.exists(DIRECTORY_NAME):
            os.makedirs(DIRECTORY_NAME)

        
        # with open(os.path.join('./' + DIRECTORY_NAME + '/', productId + '_reviews.json'), 'a') as outfile:
        for review in response.css('.cell-review'):
            if(len(review.css('h3 q ::text').extract()) > 0):
                reviews.append({'review': review.css('h3 q ::text').extract()[0], 'sentiment_score': getSentiment(review.css('h3 q ::text').extract()[0])})

        outcsvfile = csv.writer(open(os.path.join('./' + DIRECTORY_NAME + '/', productId + '_reviews.csv'), 'a'))

        for reviewObject in reviews:
            outcsvfile.writerow(reviewObject.values())


