# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ProjectParserHhItem(scrapy.Item):
    name = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()

class ProjectParserSuperJobItem(scrapy.Item):
    name = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
