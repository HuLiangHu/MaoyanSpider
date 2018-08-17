from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('doubanmovies')
process.crawl('maoyanmovies')
process.crawl('shiguangmovies')
process.crawl('taopiaopiaomovies')
process.start()