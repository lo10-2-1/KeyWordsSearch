import csv
from elasticsearch import helpers, Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def count_docs(dataset_path):
    '''Reads .csv file and returns number of rows as an integer.
    '''
    if dataset_path[-4:] != '.csv':
        return print('Incorrect path or type of file. Try again.')

    try:
        with open(dataset_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum([1 for row in reader])
    except FileNotFoundError:
        print('Incorrect path. Try again.')
    

# with open(CSV_PATH, encoding='utf-8') as f:
#     reader = csv.DictReader(f)
#     db = helpers.bulk(es, reader, index='id')