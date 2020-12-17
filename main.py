import json
from pprint import pprint
from elasticsearch import helpers, Elasticsearch

import db_converting as db

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
CSV_PATH = input('Enter csv path: ')

def main():
    db = db.converting(CSV_PATH, es)

if __name__ == '__main__':
    main()