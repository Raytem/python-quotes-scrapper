from itemadapter import ItemAdapter
from project.items import QuoteItem
from datetime import datetime

class QuoteTransformPipeline:
    def process_item(self, item: QuoteItem, spider):
        adapter = ItemAdapter(item)
        
        author_info = adapter.get('author_info')

        born_date = ItemAdapter(author_info).get('born_date')
        born_date = datetime.strptime(born_date, "%B %d, %Y").date()
        born_date_time = datetime(born_date.year, born_date.month, born_date.day)
        unix_born_date_time = int(born_date_time.timestamp())

        author_info['born_date'] = unix_born_date_time


        return item