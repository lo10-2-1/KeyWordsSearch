import json
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

import db_converting as db

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
CSV_PATH = input('Enter csv path: ')

def main():
    db.converting(CSV_PATH, es, streaming_bulk)

if __name__ == '__main__':
    main()