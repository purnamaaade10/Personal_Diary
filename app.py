from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
database = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/list_diary', methods=['GET'])
def list_diary():
    lists = list(database.personal_diary.find({},{'_id': False}))
    return jsonify({'lists': lists})

@app.route('/diary', methods=['POST'])
def add_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    today = datetime.now()
    time = today.strftime('%Y-%m-%d-%H-%M-%S')

    #image post
    file = request.files['file_give']
    extention = file.filename.split('.')[-1]
    galery = f'static/send-{time}.{extention}'
    file.save(galery)

    #profile post
    img = request.files['img_give']
    extention = img.filename.split('.')[-1]
    img_galery = f'static/img-{time}.{extention}'
    img.save(img_galery)

    #timestamp
    time = today.strftime('%Y-%m-%d')

    doc = {
        'file': galery,
        'img_profile': img_galery,
        'title':title_receive,
        'content':content_receive,
        'time': time
    }
    database.personal_diary.insert_one(doc)

    return jsonify({'message':'Upload Berhasil!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)