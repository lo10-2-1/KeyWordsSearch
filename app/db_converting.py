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
    '''Gets .csv and returns number of rows as an integer.
    '''
    return sum([1 for row in csv_file])


def generate_actions(csv_file):
    '''Gets .csv and yields a single document in index for each row.
    '''
    for row in csv_file:
        document = {
            "text": row["text"],
            "created_date": row["created_date"],
            "rubrics": row["rubrics"],
        }
        yield document


def converting(csv_file, index, client, helper):
    '''Reads the .csv file and converts it to the ElasticSearch database.
    '''
    try:
        create_index(index, client)
        number_of_docs = count_docs(csv_file)
        successes = 0
        for ok, action in helper(
            client=client, index=index, actions=generate_actions(csv_file),
        ):
            successes += ok
        return ("Database created! Indexed %d/%d documents." % (successes, number_of_docs))
    except:
        return "Something's happened. Check your file and try again."