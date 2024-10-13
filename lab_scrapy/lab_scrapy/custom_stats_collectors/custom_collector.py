from scrapy.statscollectors import StatsCollector

class CustomStatsCollector(StatsCollector):
    def __init__(self, crawler):
        super().__init__(crawler)
        self.success_count = 0
        self.error_count = 0

    def increment_success(self):
        self.success_count += 1

    def increment_error(self):
        self.error_count += 1

    def get_stats(self, *args, **kwargs):
        # Возвращаем собранные данные
        return {
            "success_count": self.success_count,
            "error_count": self.error_count,
            **super().get_stats(*args, **kwargs),
        }