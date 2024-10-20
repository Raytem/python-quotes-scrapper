from scrapy.statscollectors import StatsCollector

class CustomStatsCollector(StatsCollector):
    def __init__(self, crawler):
        super().__init__(crawler)
        self.crawler = crawler

    def _persist_stats(self, stats, spider):
        print('------custom-stats-------')
        print('pages_count: {}'.format(self.get_value('pages_count')))
        print('items_count: {}'.format(self.get_value('items_count')))

        requests_cnt = self.get_value('downloader/request_method_count/GET')
        responses_cnt = self.get_value('downloader/response_count')
        successful_responses_cnt = requests_cnt = responses_cnt

        print('total_requests_count: {}'.format(requests_cnt))
        print('successful_responses_count: {}'.format(successful_responses_cnt))

    def increment_pages_counter(self):
        self.inc_value('pages_count')

    def increment_items_counter(self):
        self.inc_value('items_count')