def search_keywords(index, client):
    '''Searches documents in database through the input keywords. 
    Returns maximum 20 results sorted by date or "No results" message.
    Instructions for user are provided.
    '''
    print('''
    "search" command allows you to find documents in database using keywords.
    To perform this command, type your keywords using space.
    Pay attention to the language of your database.
    Example: job john binary advertisement
    ''')
    keywords = input('Write keywords for searching: ')
    query_body = {
        "query": {
            "match": {
                "text": {
                    "query": keywords
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
        print(f'\nFound {total_found} documents.')
        if total_found > 20: print('Last 20 documents are shown.')
        for hit in result_list:
            print(f"\nid: {hit['_id']},")
            source = hit['_source']
            print(f"date: {source['created_date']},\nrubrics: {source['rubrics']},\ntext: {source['text']}\n")
    else:
        print('\nNo results. Check your keywords and try again.\n')


def delete_by_index(index, client):
    '''At first searches the documents in database through the document id. 
    If document is found, deletes it and sends confirmation to user.
    Else returns "No results" message.
    Instructions for user are provided.
    '''
    print('''
    "delete" command allows you to delete documents from database using document id.
    To perform this command, type document id. You can get it through the "search" command.
    Pay attention to your request. No other symbols except id itself are allowed. 
    Example: fhgh234fhdhf
    ''')
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

    
