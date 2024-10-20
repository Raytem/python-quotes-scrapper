import sqlite3
from project.constants import *
from project.items import QuoteItem, AuthorItem
from scrapy import Spider
import json
from project.analyze_data import analyze_data

class SqlLitePipeline:
    def __init__(self):
        print('------------', SQL_LITE_DB_PATH)
        self.con = sqlite3.connect(SQL_LITE_DB_PATH)
        self.cur = self.con.cursor()

        #creating databases
        self.cur.execute(SQL_CREATE_AUTHOR_TABLE_QUERY)
        self.cur.execute(SQL_CREATE_QUOTE_TABLE_QUERY)


    def process_item(self, item: QuoteItem, spider: Spider):
        author: AuthorItem = item['author_info']

        # search for existing author
        self.cur.execute(f"SELECT a.id FROM {SQL_AUTHOR_TABLE_NAME} a WHERE a.name = ? AND a.surname = ? AND a.born_date = ?", (
                author['name'],
                author['surname'],
                author['born_date'],
            )
        )
        existing_author = self.cur.fetchone()

        quote_author_id = None

        if (existing_author):
            quote_author_id = existing_author[0]
            spider.logger.warning("Author already exists in the database. Name, surname : {}, {}".format(author['name'], author['surname']))
        else:
            self.cur.execute(f"""
                    INSERT INTO {SQL_AUTHOR_TABLE_NAME} (name, surname, born_date, born_location, description) 
                    VALUES (?, ?, ?, ?, ?)
                """, 
                (
                    author['name'],
                    author['surname'],
                    author['born_date'],
                    author['born_location'],
                    author['description'],
                )
            )
            quote_author_id = self.cur.lastrowid


        # search for existing quote
        self.cur.execute(f"SELECT q.id FROM {SQL_QUOTE_TABLE_NAME} q WHERE q.text = ?", (
            item['text'],
        ))
        existing_quote = self.cur.fetchone()

        if (not existing_quote):
            self.cur.execute(f"""
                INSERT INTO {SQL_QUOTE_TABLE_NAME} (text, tags, author_id) VALUES (?, ?, ?)
            """,
                (
                    item['text'],
                    ','.join(item['tags']),
                    quote_author_id,
                )
            )
        else:
            spider.logger.warning("Quote already exists in the database, text: {}".format(item['text']))

        self.con.commit()
    
        return item
    
    def close_spider(self, spider):
        self.con.close()
        analyze_data(SQL_LITE_DB_PATH)