def search_keywords(keywords, index, client):
    '''Searches documents in database through the input keywords. 
    Returns maximum 20 results sorted by date or "No results" message.
    Instructions for user are provided.
    '''
    query_body = {
        "query": {
            "match": {
                "text": {
                    "query": keywords,
                    "fuzziness": "AUTO",
                }
            }
        },
        "sort": {   
            "created_date": {
                "order": "desc",
            }
        }
    }
    
    result = client.search(index=index, body=query_body, size=20)
    result_list = list(result['hits']['hits'])
    total_found = result['hits']['total']['value']
    if len(result_list) > 0:
        return output
    else:
        return 'No results. Check your keywords and try again.'


def delete_by_index(index, client):
    '''At first searches the documents in database through the document id. 
    If document is found, deletes it and sends confirmation to user.
    Else returns "No results" message.
    Instructions for user are provided.
    '''
    doc_id = input('Write id for deleting: ')
    query_body = {
        "query": {
            "match": {
                "_id": {
                    "query": doc_id,
                }
            }
        }
    }

    result = client.search(index=index, body=query_body)
    result = result['hits']['hits']
    if len(result) > 0:
        res = result[0]['_source']
        print(f"\nDeleting this document...\ndate: {res['created_date']},\nrubrics: {res['rubrics']},\ntext: {res['text']}\n")
        client.delete(index=index, id=doc_id, refresh=True)
    else:
        print("\nThis document doesn't exist. Check your id and try again.\n")

    
