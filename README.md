# KeyWordsSearch

Test assignment. Search in .csv documents with Elasticsearch 7.10.1. Written on Python.

## Instruction

First you should install [ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/7.10/getting-started-install.html) client and [Python](https://realpython.com/installing-python/) if you don't have it. Then run the ElasticSearch server.

Install the ``elasticsearch`` package with [pip](https://pypi.org/project/elasticsearch) to work with this rep:

```python -m pip install elasticsearch```

Then download or clone this rep, start ``cmd`` and go to the KeyWordsSearch directorium by using commant ``cd``:

```cd  C:\Users\Loopa\Downloads\KeyWordsSearch```

And run the main file:

```python main.py```

In the program you should start with writing a path to your .csv file. You can copy it from file properties. Required columns: text, created_date, rubrics. Example: ``C:\Users\Loopa\Downloads\db.csv``

Give your database special name and start.

## Options

Three commands are available:

1. **search** - searches documents in database through the input keywords. Returns maximum 20 results sorted by date or "No results" message. Instructions for user are provided. 

2. **delete** - at first searches the documents in database through the document id. If document is found, deletes it and sends confirmation to user. Else returns "No results" message. Instructions for user are provided.

3. **quit** - quits the programm deleting the created database from ElasticSearch server.

## Notes

In the future this rep will be modified into web-application.
At the moment its current version is available on the branch Flask.