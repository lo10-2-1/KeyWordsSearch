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


def count_docs(csv_file):
    '''Reads the file through csv.DictReader()
    and returns number of rows as an integer.
    '''
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return sum([1 for row in reader])


def generate_actions(csv_file):
    '''Reads the file through csv.DictReader()
    and yields a single document in index for each row.
    '''
    with open(csv_file, encoding='utf-8') as f:
            reader = csv.DictReader(f)
        
            for row in reader:
                document = {
                    "text": row["text"],
                    "created_date": row["created_date"],
                    "rubrics": row["rubrics"],
                }
                yield document


def converting(csv_file, index, client, helper):
    '''Reads the .csv file and converts it to the ElasticSearch database.
    '''
    # try:
    create_index(index, client)
    number_of_docs = count_docs(csv_file)
    successes = 0
    for ok, action in helper(
        client=client, index=index, actions=generate_actions(csv_file),
    ):
        successes += ok
    return ("Database created! Indexed %d/%d documents." % (successes, number_of_docs))
    # except:
    #     return "Something's happened. Check your file and try again."