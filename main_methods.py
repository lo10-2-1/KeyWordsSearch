import json
from pprint import pprint
from elasticsearch import helpers, Elasticsearch

import db_converting as db

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
CSV_PATH = input('Enter csv path: ')

number_of_docs = db.count_docs(CSV_PATH)

print(number_of_docs)