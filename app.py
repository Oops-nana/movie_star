from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def show_stars():
    
    movie_star = list(db.mystar.find({}, {'_id' : False}).sort('like', -1))

    return jsonify({'result' : movie_star, 'msg': 'list 연결되었습니다!'})


@app.route('/api/like', methods=['POST'])
def like_star():
    star_name = request.form['star_name']
    current_like = db.mystar.find_one({'name' : star_name}, {'_id' : False})['like'] + 1 
    db.mystar.update_one({'name' : star_name}, {"$set" : {"like" : current_like}})

    return jsonify({'msg': 'like 연결되었습니다!'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    star_name = request.form['star_name']
    
    db.mystar.delete_one({"name" : star_name})

    return jsonify({'msg': 'delete 연결되었습니다!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)