# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
from datetime import datetime
from moviesgrade.items import MovieGrade


class TaoMoviesSpider(scrapy.Spider):
    name = 'taopiaopiaomovies'
    allowed_domains = ['taopiaopiao.com']
    start_urls = ['http://taopiaopiao.com/']

    def start_requests(self):
        chrome_options = webdriver.ChromeOptions()
        # 使用headless无界面浏览器模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        broswer =webdriver.Chrome(chrome_options=chrome_options)
        wait = WebDriverWait(broswer, 10)
        url='https://h5.m.taopiaopiao.com/app/moviemain/pages/index/index.html?from=outer&spm=a1z21.6646385.header.3.614e2c47Ql6p6T&n_s=new'
        broswer.get(url)
        location =broswer.find_element_by_xpath('//ul/li[text()="上海"]')
        location.click()

        for i in range(10):
            broswer.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            ActionChains(broswer).key_down(Keys.DOWN).perform()
            time.sleep(1)

        movieurls=broswer.find_elements_by_xpath('//div[@class="m-info"]/a')
        for movieurl in movieurls:
            url =movieurl.get_attribute('href')
            yield scrapy.Request(url,meta={'url':url})

    def parse(self, response):

        chrome_options = webdriver.ChromeOptions()
        # 使用headless无界面浏览器模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # wait = WebDriverWait(driver, 10)

        driver.get(response.meta['url'])
        item=MovieGrade()
        item['name'] =driver.find_element_by_xpath('//*[@id="J_show-name"]').text
        item['movieDate']=driver.find_element_by_xpath('//span[@class="show-open-info"]').text
        item["comefrom"] = "淘票票"
        item["filmid"] = re.search('showid=(\d+)', response.meta['url']).group(1)
        item['want'] = driver.find_element_by_xpath('//*[@id="J_rootContent"]/section[2]/section/div[2]/div[1]').text
        try:
            item['Grade'] = driver.find_element_by_xpath('//*[@id="J_rootContent"]/section[2]/section/div[1]/div[1]').text
            gradePeople=driver.find_element_by_xpath('//*[@id="J_rootContent"]/section[2]/section/div[1]/div[2]').text
            item['gradePeople'] =re.search('(\d+)',gradePeople,re.S).group(1)
        except:
            item['Grade'] = None
            item['gradePeople'] = None
        item['crawldate'] = str(datetime.today())
        item["createdtime"] = str(datetime.now())
        yield item

