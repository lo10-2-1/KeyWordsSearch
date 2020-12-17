import csv
import tqdm


def create_index(client):
    '''Creates an index in Elasticsearch.
    '''
    client.indices.create(
        index="DB",
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


def count_docs(dataset):
    '''Reads .csv file and returns number of rows as an integer.
    '''
    return sum([1 for row in dataset])


def generate_actions(dataset):
    '''Yields a single document in index for each row.
    '''
    for row in dataset:
        document = {
            "text": row["text"],
            "created_date": row["created_date"],
            "rubrics": row["rubrics"],
        }
        yield document


def converting(path, client):
    '''Reads the file through csv.DictReader() and for each row
    yields a single document.
    '''
    if dataset_path[-4:] != '.csv':
        return print('Incorrect path or type of file. Try again.')

    try:
        with open(dataset_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            number_of_docs = count_docs(reader)
        except FileNotFoundError:
        print('Incorrect path. Try again.')

    number_of_docs = db.count_docs(path)
    create_index(client)
    
    progress = tqdm.tqdm(unit='docs', total=number_of_docs)

    successes = 0
    for ok, action in streaming_bulk(
        client=es, index='DB', actions=generate_actions(),
    ):
        progress.update(1)
        successes += ok
    print("Indexed %d/%d documents" % (successes, number_of_docs))
    print(number_of_docs)


if __name__ == '__main__':
    converting()