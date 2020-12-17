

def search_keywords(client):
    print('''"Search" command allows you to find documents in database using keywords.
    To perform this command, type your keywords using space.
    Pay attention to the language of your database.
    Example: job john binary advertisement
    ''')
    keywords = input('Write keywords for searching: ')
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
    
    result = client.search(index="db", body=query_body, size=20)
    result_list = list(result['hits']['hits'])
    if len(result_list) > 0:
        for hit in result_list:
            print(f'id: {hit['_id']},\ndate: {hit['created_date']},\nrubrics: {hit['rubrics']},\ntext: {hit['text']}')
    else:
        print('No results. Check your keywords and try again.')

def delete_by_index(client):
    pass