import csv

def create_index(index, client):
    '''Creates an index in Elasticsearch.
    '''
    client.indices.create(
        index=index,
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


def converting(path, index, client, helper):
    '''Reads the .csv file and converts it to the ElasticSearch database.
    '''
    # try:
    create_index(index, client)
    number_of_docs = count_docs(path)

    successes = 0
    for ok, action in helper(
        client=client, index=index, actions=generate_actions(path),
    ):
        successes += ok
    return ("Database created! Indexed %d/%d documents." % (successes, number_of_docs))
    # except:
    #     return "Something's happend. Check your file and try again."