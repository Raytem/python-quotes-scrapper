import scrapy
from lab_scrapy.custom_stats_collectors import CustomStatsCollector
from scrapy import signals


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["https://quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/page/1/"]
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'CLOSESPIDER_PAGECOUNT': 1,
    }

    cur_page_items_cnt_value_name = 'cur_page_items_count'
    cur_page_value_name = 'cur_page'
    total_items_value_name = 'total_items'

    def parse(self, response):
        crawler_stats = self.crawler.stats;

        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            crawler_stats.inc_value(self.cur_page_items_cnt_value_name)
            crawler_stats.inc_value(self.total_items_value_name)


        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            crawler_stats.inc_value(self.cur_page_value_name)

            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

            self.logger.info(f"----Current page: {crawler_stats.get_value(self.cur_page_value_name)}")
            self.logger.info(f"----Current page items count: {crawler_stats.get_value(self.cur_page_items_cnt_value_name)}")
            crawler_stats.set_value(self.cur_page_items_cnt_value_name, 0)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.stats = CustomStatsCollector(crawler)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
        
    def spider_closed(self, spider):
        stats = self.crawler.stats.get_stats()
        self.logger.info(f"Final stats: {stats}")
        # self.logger.info(f"Total successful requests: {stats['success_count']}")
        # self.logger.info(f"Total errors encountered: {stats['error_count']}")