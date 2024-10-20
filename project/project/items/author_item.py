import scrapy

class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    surname = scrapy.Field()
    born_date = scrapy.Field()
    born_location = scrapy.Field()
    description = scrapy.Field()