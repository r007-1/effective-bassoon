from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from crawler.items import CrawlerItem
import time
import random
import datetime

class Harrods(scrapy.Spider):
    name = "harrods"
    allowed_domains = ["harrods.com"]
    start_urls = []
    sitemaps = []
    sitemaps = ["http://www.harrods.com/SiteMaps/harrods-sitemap-products.xml"]
    for sitemap in sitemaps:
        tags = bs(requests.get(sitemap).text, "lxml").find_all("url")
        for tag in tags:
            prod_link = tag.findNext("loc").text
            start_urls.append(prod_link)

    def parse(self, response):
        try:
            datetime = int(str(int(time.time()*100))) #Don't change!
            random.seed(1412112 + datetime) #Don't change!

            item = CrawlerItem() #Don't change!
            item['prod_id'] = unicode(datetime) + unicode(int(random.uniform(100000, 999999))) #Don't change!
            item['prod_id'] = int(item['prod_id'])
            item['affiliate_partner'] = "viglink"
            item['brand'] = "Harrods"
            item['long_desc'] = unicode(response.selector.xpath('//p[@class="description"]/text()').extract()[0])
            item['short_desc'] = unicode(response.selector.xpath('//span[@class="productname"]/text()').extract()[0].strip())
            item['product_link'] = response.selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0]

            item['cat_1'] = ""
            item['cat_2'] = ""
            item['cat_3'] = ""
            item['cat_code'] = ""

            item['date_added'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]
            item['date_last_updated'] = [unicode(str(time.strftime("%d/%m/%Y %H:%M:%S")), "utf-8")]

            item['image_urls'] = ""
            item['img_1'] = ""
            item['img_2'] = ""
            item['img_3'] = ""
            item['img_4'] = ""
            item['img_5'] = ""

            try:
                item['imglink_1'] = response.selector.xpath('//ul[@class="alt_view"]/li[1]/a/@href').extract()[0]
            except IndexError:
                item['imglink_1'] = ""

            try:
                item['imglink_2'] = response.selector.xpath('//ul[@class="alt_view"]/li[2]/a/@href').extract()[0]
            except IndexError:
                item['imglink_2'] = ""

            try:
                item['imglink_3'] = response.selector.xpath('//ul[@class="alt_view"]/li[3]/a/@href').extract()[0]
            except IndexError:
                item['imglink_3'] = ""

            try:
                item['imglink_4'] = response.selector.xpath('//ul[@class="alt_view"]/li[4]/a/@href').extract()[0]
            except IndexError:
                item['imglink_4'] = ""

            try:
                item['imglink_5'] = response.selector.xpath('//ul[@class="alt_view"]/li[5]/a/@href').extract()[0]
            except IndexError:
                item['imglink_5'] = ""

            try:
                item['imglink_6'] = response.selector.xpath('//ul[@class="alt_view"]/li[6]/a/@href').extract()[0]
            except IndexError:
                item['imglink_6'] = ""

            item['mcat_1'] = ""
            item['mcat_2'] = ""
            item['mcat_3'] = ""
            item['mcat_4'] = ""
            item['mcat_5'] = ""
            item['mcat_code'] = ""

            item['merchant'] = "Harrods"
            item['merchant_id']  = "2GSE52"
            item['merchant_prod_id'] = response.selector.xpath('//span[@class="product_code"]/text()').extract()[0][13:]

            item['is_available'] = 1 #BOOLEAN
            item['currency'] = response.selector.xpath('//span[@class="country-selector_currency"]/text()').extract()[0].strip()
            item['currency_symbol'] = response.selector.xpath('//span[@class="country-selector_currency"]/span[@class="code"]/text()').extract()[0].encode('utf-8').strip()

            try:
                if (int(float(response.selector.xpath('//span[@class="prices price"]/span[@class="was"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//span[@class="prices price"]/span[@class="now"]/text()').extract()[0][5:]))):
                    orig = int(float(response.selector.xpath('//span[@class="prices price"]/span[@class="was"]/text()').extract()[0][1:]))
                    sale = int(float(response.selector.xpath('//span[@class="prices price"]/span[@class="now"]/text()').extract()[0][5:]))
                    item['price_orig'] = orig
                    item['price_sale'] = sale
                    item['price_perc_discount'] = int(100-100*(sale/orig))
                    item['price'] = item['price_sale']
                    item['on_sale'] = 1 #BOOLEAN
                else:
                    item['price_orig'] = int(float(response.selector.xpath('//span[@class="prices price"]/span[@class="was"]/text()').extract()[0][1:]))
                    item['price'] = item['price_orig']
                    item['price_sale'] = ""
                    item['on_sale'] = 0

            except IndexError:
                item['price_orig'] = int(float(response.selector.xpath('//*[@class="product_right_box f_right"]//span[@class="price_all"]/span[1]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
                item['price_sale'] = ""
                item['on_sale'] = 0 #BOOLEAN

            item['primary_color'] = ""

            tags = [item['brand'], item['short_desc'], item['long_desc']] #str(" ".join(item['mcats'])),
            item['tags'] = " ".join(tags).encode('utf-8').strip()
            yield item
        except IndexError as e:
            return