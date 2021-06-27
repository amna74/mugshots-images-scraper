# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from random import randrange
import logging
import requests
import os

class StrainsSpider(scrapy.Spider):
    name = 'strains'

    custom_settings = {
        'CONCURRENT_REQUESTS': '1'
        # 'FEED_EXPORT_ENCODING': 'utf-8'
    }
    def start_requests(self):
        yield scrapy.Request(url="http://mugshots.com/US-States/", callback=self.parse)

    def parse(self, response):
        for country in response.xpath("//div[@style='overflow: hidden']/div/ul/li"):
            link= response.urljoin(country.xpath(".//a/@href").get())

            yield scrapy.Request(url=link, callback=self.parse_new)

    # def parse3(self,response):
    #     for newcountry in response.xpath("//div[@class='image']"):
    #         imagurl= newcountry.xpath(".//img/@src").get().strip()
    #         yield scrapy.Request(url=imagurl, callback= self.parse)

    def parse_new(self, response):

        for country in response.xpath("//div[@style='overflow: hidden']/div/ul/li"):
            link= response.urljoin(country.xpath(".//a/@href").get())

            yield scrapy.Request(url=link, callback=self.parse_download)

    def parse_download(self, response):
        state_name=response.xpath("//div[@class='category-breadcrumbs']/h1/a[2]/text()").get()
        country_name = response.xpath("//div[@class='category-breadcrumbs']/h1/a[3]/text()").get()
        city_name = response.xpath("//div[@class='category-breadcrumbs']/h1/span/text()").get()

        if os.path.exists(state_name +str('/')+ country_name +str('/')+ city_name):
            print("File Exist")
        else:
            print("File Created")
            os.makedirs(state_name +str('/')+ country_name +str('/')+ city_name)

        path=(state_name +str('/')+ country_name +str('/')+ city_name)

        img_url=response.xpath("//div[@class='image']/img/@src").getall()

        #img_url=img_url.replace(".110x110", "")

        img_url = [item.replace("110x110", "400x800") for item in img_url]

        names=response.xpath("//div[@class='label']/text()").getall()

        for img_url, name in zip(img_url, names):
            print(img_url)
            imageUrls=requests.get(url=img_url)

            with open(path+"/"+name+".jpg", 'wb') as c:
                c.write(imageUrls.content)
                print("image saved at : " + path)

process = CrawlerProcess()
process.crawl(StrainsSpider)
process.start()