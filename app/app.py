from elasticsearch import Elasticsearch
from elasticsearch.helpers import streaming_bulk

from flask import Flask, url_for, render_template, request, make_response
from flask_elasticsearch import FlaskElasticsearch

import db_converting as db
import methods
import os
import csv

app = Flask(__name__)
es = FlaskElasticsearch(app)
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'csv'}
USER_DB = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
@app.route('/main', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        es.indices.delete(index=USER_DB, ignore=[400, 404])
        return 'Your session is over. Thank you and come again!'
    return render_template('main.html'), 'ok'


@app.route('/download_file', methods=['POST', 'GET'])
def download_file():
    if request.method == 'POST':
        csv_file = request.files['download']
        db_name = request.form['db_name']
        USER_DB = db_name
        if db_name == False or csv_file.filename == '':
            return 'You forgot to paste data in the forms. Please try again.'
        if csv_file and allowed_file(csv_file.filename):
            filename = csv_file.filename
            csv_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            csv_path = os.path.join(app.config['UPLOAD_FOLDER']) + filename
            with open(csv_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                read_list = [row for row in reader]
                result = db.converting(read_list, db_name, es, streaming_bulk)
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