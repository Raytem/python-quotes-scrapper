import sqlite3
from collections import Counter
from prettytable import PrettyTable
from project.constants import *

def analyze_data(db_sql_lite_path):
    print('\n========Statistics========')
    connection = sqlite3.connect(db_sql_lite_path)
    cur = connection.cursor()

    # authors analytics
    cur.execute(f"""
            SELECT a.name, a.surname, COUNT(q.id) as quotes_cnt
            FROM {SQL_AUTHOR_TABLE_NAME} a
            LEFT JOIN {SQL_QUOTE_TABLE_NAME} q ON q.author_id = a.id
            GROUP BY a.id
            ORDER BY quotes_cnt DESC
    """)
    authors = cur.fetchall()

    authors_table = PrettyTable()
    authors_table.field_names = ['Full name', 'Quotes count']
    authors_table.align['Full name'] = 'l'
    for author in authors:
        authors_table.add_row((f"{author[0]} {author[1]}", author[2]))

    # tags analytics
    cur.execute(f"SELECT tags FROM {SQL_QUOTE_TABLE_NAME}")
    tags_list = cur.fetchall()

    tags_flat = [tag for sublist in tags_list for tag in sublist[0].split(',')]
    tag_counts = Counter(tags_flat)

    tags_table = PrettyTable()
    tags_table.field_names = ['Name', 'Count']
    tags_table.align['Name'] = 'l'
    for tag, count in tag_counts.most_common(10):
        tags_table.add_row((tag, count))

    print('\nAuthors and quotes count:')
    print(authors_table)
    print("\nFrequently occurring tags:")
    print(tags_table)

    connection.close()