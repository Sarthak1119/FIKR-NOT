# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 23:49:37 2018

@author: Rishabh
"""

import scrapy
import pymysql
 

class Electrician(scrapy.Spider):
    name = "elec"
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='Project',use_unicode=True, charset="utf8")
    cur=conn.cursor()
    Name = None
    ct_id = None
    city = input("Enter a city: ")
    cur.execute('INSERT INTO city(Name) SELECT * FROM (SELECT %s) AS tmp WHERE NOT EXISTS( SELECT Name from city WHERE Name=%s)',(city,city))
    conn.commit()
    city_url = "https://www.justdial.com/" + city + "/Electricians/nct-10184166"
    cur.execute('select Id from city where Name = %s',(city))
    for r in cur:
        ct_id=r[0]

        
    start_urls = [city_url]
    
    def parse(self, response):
        for href in response.xpath('//li[@class="cntanr"]/@data-href'):
            yield response.follow(href,self.getdetails)
        
        for href in response.xpath('//div[@class="jpag"]/a/@href'):
            yield response.follow(href,self.parse)
            
    def getdetails(self,response):
        def extract_name(query):
            self.Name = response.xpath(query).extract_first()
            self.cur.execute('INSERT INTO Electrician(name,city_id) SELECT * FROM (SELECT %s,%s) AS tmp WHERE NOT EXISTS( SELECT name from Electrician WHERE name=%s and city_id = %s)',(self.Name,self.ct_id,self.Name,self.ct_id))
            self.conn.commit()
            return self.Name
        
        def extract_address(query):
            Address = str(response.xpath(query).extract_first())
            self.cur.execute('update Electrician set Address = %s where name = %s',(Address,self.Name))
            self.conn.commit()
            return Address
        
        def extract_review(query):
            review = response.xpath(query).extract_first()
            return review
        
        yield{
            'Name':extract_name('//span[@class="item"]/span/text()'),
             'address':extract_address('//span[@id="fulladdress"]/span/span[@class="lng_add"]/text()'),
                #'Review':extract_review('//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/div/div/span/span[1]/span[1]/span/text()')
                #'Contact':response.xpath('//*[@id="setbackfix"]/div[1]/div/div[1]/div[2]/div/ul/li[2]/p/span[2]/span/a/span[@class="mobilesv icon"]/text()').extract()
                }
        
        