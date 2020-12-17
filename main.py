import json
from pprint import pprint
from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

import db_converting as db

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def main():
    while True:
        csv_path = input('Enter csv path: ')

        if csv_path[-4:] != '.csv':
            print('Incorrect path or type of file. Try again.')
        else:
            try:
                db.converting(csv_path, es, streaming_bulk)
                break
            except FileNotFoundError:
                print('Incorrect path. Try again.')
    

if __name__ == '__main__':
    main()