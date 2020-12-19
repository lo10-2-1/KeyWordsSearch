from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from flask import Flask, url_for, render_template, request, make_response
from flask_elasticsearch import FlaskElasticsearch

import db_converting as db
import methods

app = Flask(__name__)
es = FlaskElasticsearch(app)
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        es.indices.delete(index=request.form['db_name'], ignore=[400, 404])
        return 'Your session is over. Thank you and come again!'
    return render_template('main.html'), 'ok'


@app.route('/download_file', methods=['POST', 'GET'])
def download_file():
    if request.method == 'POST':
        csv_path = request.form['download']
        db_name = request.form['db_name']
        if csv_path[-4:] != '.csv':
            return 'Incorrect path or type of file. Please try again.'
        elif csv_path == False or db_name == False:
            return 'You forgot to paste data in the forms. Please try again.'
        result = db.converting(csv_path, db_name, es, streaming_bulk)
        return result
    return render_template('download.html'), 'ok'


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        keywords = request.form['search']
        try:
            methods.search_keywords(db_name, es)
            return redirect
        except:
            return "Something's gone wrong. Check if your database is downloaded and try again."
    else:
        return render_template('search.html'), 'ok'


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        keywords = request.form['search']
        try:
            methods.delete_by_index(db_name, es)
            return redirect
        except:
            return "Something's gone wrong. Check if your database is downloaded and try again."
    return render_template('delete.html'), 'ok'


if __name__ == '__main__':
    app.run(debug=True)