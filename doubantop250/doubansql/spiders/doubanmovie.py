# -*- coding: utf-8 -*-
import scrapy
from doubansql.items import DoubansqlItem
import os
import urllib
class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']
    # for i in range(1, 10):
    #     start_urls.append("https://movie.douban.com/top250?start=%d&filter=" % (25 * i))
    # def start_requests(self):
    #     for i in range(0, 226, 25):
    #         url = self.base_url + "?start=%d&filter=" % i
    #         yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        item = DoubansqlItem()
        # selector =Selector(response)
        Movies = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for eachMovie in Movies:
            moviename = eachMovie.xpath('div/div[2]/div[1]/a/span[1]/text()').extract_first()
            # fullname = "".join(moviename)
            dbimgurl = eachMovie.xpath('div/div[1]/a/img/@src').extract_first()
            classname = eachMovie.xpath('div/div[2]/div[2]/p[2]/span/text()').extract_first()
            grade = eachMovie.xpath('div/div[2]/div[2]/div/span[2]/text()').extract_first()
            count = eachMovie.xpath('div/div[2]/div[2]/div/span[4]/text()').extract_first()
            introduction = eachMovie.xpath('div/div[2]/div[2]/p[1]/text()').extract_first()
            if introduction:
                introduction = introduction[0]
            else:
                introduction = ''
            filename = moviename + '.jpg'
            dirpath = './cover'
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            filepath = os.path.join(dirpath, filename)
            urllib.request.urlretrieve(dbimgurl, filepath)
            cover = 'cover/' + filename
            item['moviename'] = moviename
            item['dbimgurl'] = cover
            item['classname'] = classname
            item['grade'] = grade
            item['count'] = count
            item['introduction'] = introduction
            yield item
            # 解析下一页规则，取后一页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://movie.douban.com/top250' + next_link, callback=self.parse)

