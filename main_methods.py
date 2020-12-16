import csv
import json
from pprint import pprint
from elasticsearch import helpers, Elasticsearch

# import db_converting as db

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
csv_path = input('Enter csv path:')


with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    db = helpers.bulk(es, reader, index='id')

for row in db:
    print(row)