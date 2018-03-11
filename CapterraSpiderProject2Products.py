import scrapy
import os
from scrapy.http.request import Request
import json
import csv

DIRECTORY_NAME = 'project_2_productsV2'
REVIEW_DIR_NAME = 'project_2_product_reviews'

GLOBAL_COUNT = 0

class CapterraSpider(scrapy.Spider):
    name = 'CapterraSpiderProject2Products'
    
    def start_requests(self):
      hrefs = json.load(open('hrefs.json'))
      # hrefs = json.load(open('hrefsSample.json'))
      for hrefObj in hrefs:
        url = 'https://www.capterra.com' + hrefObj['href'][0]
        yield Request(url, self.parse)

    def parse(self, response):

        global GLOBAL_COUNT
        url = response.url
        productId = url[url.index('/p/') + 3 : url.index('/', url.index('/p/') + 3)]
        productName = url[url.index(productId) + len(productId) + 1 : url.index('/', url.index(productId) + len(productId) + 1)]

        ##### sentiment average ####
        sentimentScores = []
        with open(os.path.join(REVIEW_DIR_NAME + '/' + productId + '_reviews.csv'), 'r+', newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            for row in csvreader:
                sentimentScores.append(float(row[1]))


        averageSentiment = 0
        if (len(sentimentScores) != 0):
            averageSentiment = sum(sentimentScores)/float(len(sentimentScores))

        if not os.path.exists(DIRECTORY_NAME):
            os.makedirs(DIRECTORY_NAME)


        
        product = {'productId' : productId, 'productName': productName, 'averageSentiment' : averageSentiment}

        featureCategoryRank = 0
        for i in range(0,20):
            if response.css('#product-features .category-features-list h5.color-blue ::text')[i].extract().startswith("Customer Relationship Management"):
                featureCategoryRank = i
                break

        
        # with open(os.path.join('./' + DIRECTORY_NAME + '/', productId + '_reviews.json'), 'a') as outfile:
        for feature in response.css('#product-features .category-features-list')[featureCategoryRank].css('ul.features-check-list li.ss-check ::text'):
            product[feature.extract()] = 1

        for feature in response.css('#product-features .category-features-list')[featureCategoryRank].css('ul.features-check-list li.ss-check.feature-disabled ::text'):
            product[feature.extract()] = 0
            # reviews.append({'review': review.css('h3 q ::text').extract()[0], 'sentiment_score': getSentiment(review.css('h3 q ::text').extract()[0])})

        outcsvfile = csv.writer(open(os.path.join('./' + DIRECTORY_NAME + '/', 'product_specs.csv'), 'a'))
        if  GLOBAL_COUNT == 0:
            outcsvfile.writerow(product.keys())
            GLOBAL_COUNT =  GLOBAL_COUNT + 1
        outcsvfile.writerow(product.values())




