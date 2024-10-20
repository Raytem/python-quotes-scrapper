import scrapy
from scrapy.http import Response
from project.stats_classes.custom_stats_collector import CustomStatsCollector
from typing import cast
from project.items import AuthorItem, QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    #json
    custom_feed = {
        "../output/quotes.json": {
            "format": "json",
            "indent": 2,
            "overwrite": True,
        }
    }

    ##csv
    # custom_feed = {
    # '../output/quotes.csv': {
    #     'format': 'csv',
    #     'overwrite': True,
    # },

    custom_settings = {
        'STATS_CLASS': 'project.stats_classes.custom_stats_collector.CustomStatsCollector',
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        settings.setdefault("FEEDS", {}).update(cls.custom_feed)



    def __init__(self, *args, **kwargs):
        spider = super().__init__(*args, **kwargs)
        

    def parse(self, response: Response):
        self.crawler.stats = cast(CustomStatsCollector, self.crawler.stats)
        

        self.logger.info("Parsing main page: {}".format(response.url))

        for quote in response.css('div.quote'):
            quoteData = QuoteItem()
            quoteData['text'] = quote.css('span.text::text').get()
            quoteData['tags'] = quote.css('div.tags a.tag::text').getall()

            author_url = quote.css('span a::attr(href)').get()
            if author_url:
                author_url = response.urljoin(author_url)
                self.logger.info(f"Found author URL: {author_url}")
                
                request = scrapy.Request(
                    author_url, 
                    callback=self.parse_author, 
                    meta={'quote': quoteData}
                )
                self.logger.info(f"Request created: {request}")
                yield request
            else:
                self.logger.warning("Author URL not found for a quote.")
            
            self.crawler.stats.increment_items_counter()


        self.crawler.stats.increment_pages_counter()
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Following to the next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("No next page found. Crawling completed.")


    def parse_author(self, response: Response):
        if response.status != 200:
            self.logger.warning(f"Failed to retrieve author page: {response.url} with status {response.status}")
            return
         
        self.logger.info(f"Parsing author page: {response.url}")

        quote: QuoteItem = response.meta['quote']
        author_full_name = response.css('h3.author-title::text').get()

        if author_full_name:
            author_name_parts = author_full_name.strip().split(' ', 1)
            name = author_name_parts[0] if len(author_name_parts) > 0 else ''
            surname = author_name_parts[1] if len(author_name_parts) > 1 else ''
        else:
            self.logger.warning("Author name not found on page.")
            name, surname = '', ''

        author_info = AuthorItem()
        author_info['name'] = name
        author_info['surname'] = surname
        author_info['born_date'] = response.css('span.author-born-date::text').get()
        author_info['born_location'] = response.css('span.author-born-location::text').get()
        author_info['description'] = response.css('div.author-description::text').get()

        yield {
            **quote,
            'author_info': author_info,
        }