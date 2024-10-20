import scrapy
from .author_item import AuthorItem

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    tags = scrapy.Field()
    author_info = scrapy.Field()