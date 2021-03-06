from bs4 import BeautifulSoup as bs
from lxml import etree
import requests
import scrapy
from crawler.items import CrawlerItem
import time
import random
import datetime

class SaksOff5th(scrapy.Spider):
    name = "saks-off-5th"
    allowed_domains = ["saksoff5th.com"]
    start_urls = []
    sitemaps = []

    sitemap_main = ["http://www.saksoff5th.com/sitemap_index.xml"]
    main_tags = bs(requests.get(sitemap_main[0]).text, "lxml").find_all("sitemap")
    for main_tag in main_tags:
        sitemaps.append(main_tag.findNext("loc").text)

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
            item['brand'] = "Saks Off 5th"
            item['long_desc'] = " | ".join(response.selector.xpath('//div[@itemprop="description"]/ul/li/text()').extract())
            item['short_desc'] = response.selector.xpath('//div[@class="pdt-short-desc o5-product-short-decription"]/span/text()').extract()[0]
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
                item['imglink_1'] = "http://image.s5a.com/is/image/saksoff5th/" + response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0] + "_247x329.jpg"
            except IndexError:
                item['imglink_1'] = ""

            try:
                item['imglink_2'] = "http://image.s5a.com/is/image/saksoff5th/" + response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0] + "A1_247x329.jpg"
            except IndexError:
                item['imglink_2'] = ""

            try:
                item['imglink_3'] = "http://image.s5a.com/is/image/saksoff5th/" + response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0] + "A2_247x329.jpg"
            except IndexError:
                item['imglink_3'] = ""

            try:
                item['imglink_4'] = "http://image.s5a.com/is/image/saksoff5th/" + response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0] + "A3_247x329.jpg"
            except IndexError:
                item['imglink_4'] = ""

            try:
                item['imglink_5'] = "http://image.s5a.com/is/image/saksoff5th/" + response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0] + "A4_247x329.jpg"
            except IndexError:
                item['imglink_5'] = ""

            try:
                item['imglink_6'] = "http://image.s5a.com/is/image/saksoff5th/" + response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0] + "A5_247x329.jpg"
            except IndexError:
                item['imglink_6'] = ""

            item['mcat_1'] = ""
            item['mcat_2'] = ""
            item['mcat_3'] = ""
            item['mcat_4'] = ""
            item['mcat_5'] = ""
            item['mcat_code'] = ""

            item['merchant'] = "Saks Off 5th"
            item['merchant_id']  = "E78883"
            item['merchant_prod_id'] = response.selector.xpath('//div[@id="js-product-number"]/@data-master-sku').extract()[0]

            item['is_available'] = 1
            item['currency'] = "USD"
            item['currency_symbol'] = "$"

            try:
                if (int(float(response.selector.xpath('//span[@class="o5-price-standard"]/text()').extract()[0][1:])) != int(float(response.selector.xpath('//span[@class="price-sales o5-price-sales"]/text()').extract()[0][1:]))):
                    orig = int(float(response.selector.xpath('//span[@class="o5-price-standard"]/text()').extract()[0][1:]))
                    sale = int(float(response.selector.xpath('//span[@class="price-sales o5-price-sales"]/text()').extract()[0][1:]))
                    item['price_orig'] = orig
                    item['price_sale'] = sale
                    item['price_perc_discount'] = int(100-100*(sale/orig))
                    item['price'] = item['price_sale']
                    item['on_sale'] = 1
                else:
                    item['price_orig'] = int(float(response.selector.xpath('//span[@class="o5-price-standard"]/text()').extract()[0][1:]))
                    item['price'] = item['price_orig']
                    item['price_sale'] = ""
                    item['on_sale'] = 0
            except IndexError:
                item['price_orig'] = int(float(response.selector.xpath('//span[@class="o5-price-standard"]/text()').extract()[0][1:]))
                item['price'] = item['price_orig']
                item['price_sale'] = ""
                item['on_sale'] = 0 #BOOLEAN

            item['primary_color'] = ""
            tags = [unicode(item['brand']), unicode(item['short_desc']), unicode(item['long_desc'])] #str(" ".join(item['mcats'])),
            item['tags'] = " ".join(tags)
            yield item
        except IndexError as e:
            return