from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

import db_converting as db
import methods

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


def main():
    while True:
        csv_path = input('Enter csv path: ')

        if csv_path[-4:] != '.csv':
            print('\nIncorrect path or type of file. Please try again.\n')
        else:
            try:
                db.converting(csv_path, es, streaming_bulk)
                break
            except FileNotFoundError:
                print('\nIncorrect path. Please try again.\n')
    
    while True:
        print('''
        Three commands are available:
            1. search
            2. delete
            3. quit
        ''')
        comm = input('What do you want? Print the name of the command: ')
        
        if comm == 'search':
            methods.search_keywords(es)
        elif comm == 'delete':
            methods.delete_by_index(es)
        elif comm == 'quit':
            es.delete(index='db')
            quit()
        else:
            print('\nIncorrect command. Please try again.\n')
            

if __name__ == '__main__':
    main()