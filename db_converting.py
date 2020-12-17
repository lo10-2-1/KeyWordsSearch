import csv
import tqdm


def create_index(client):
    '''Creates an index in Elasticsearch.
    '''
    client.indices.create(
        index="db",
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "created_date": {"type": "date",
                                     "format": "yyyy-MM-dd HH:mm:ss"},
                    "rubrics": {"type": "text"},
                }
            },
        },
        ignore=400,
    )


def count_docs(path):
    '''Reads the file through csv.DictReader()
    and returns number of rows as an integer.
    '''
    with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return sum([1 for row in reader])


def generate_actions(path):
    '''Reads the file through csv.DictReader()
    and yields a single document in index for each row.
    '''
    with open(path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
        
            for row in reader:
                document = {
                    "text": row["text"],
                    "created_date": row["created_date"],
                    "rubrics": row["rubrics"],
                }
                yield document


def converting(path, client, helper):
    '''Reads the file through csv.DictReader() and converts it to
    the ElasticSearch database.
    '''
    if path[-4:] != '.csv':
        return print('Incorrect path or type of file. Try again.')

    try:
        create_index(client)
        number_of_docs = count_docs(path)

        successes = 0
        for ok, action in helper(
            client=client, index='db', actions=generate_actions(path),
        ):
            successes += ok
        print("Database created! Indexed %d/%d documents" % (successes, number_of_docs))

    except FileNotFoundError:
        print('Incorrect path. Try again.')


if __name__ == '__main__':
    converting()