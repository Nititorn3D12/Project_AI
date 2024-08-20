from flask import Flask, jsonify, request
from flask_cors import CORS #comment this on deployment
import sqlite3
import pickle;
import numpy as np;


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
con = sqlite3.connect("dsproject2023.db", check_same_thread=False)
cur = con.cursor()

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.route('/dummy/city')
def dummy_city_list():
    result = dict()
    result["columns"] = ["ชื่อจังหวัด", "จำนวนร้าน"]
    result["rows"] = [("A", 10), ("B", 20), ("C", 30)]
    response = jsonify(result)
    return result

@app.route('/api/ex01')
def ex01():
    result = dict()
    result["Key1"] = ["6", 2, "X"]
    result["3"] = "Hello"
    result["A1"] = ("Dog", "Cat")
    
    response = jsonify(result)
    return response  

@app.route('/api/ex02')
def ex02():
    result = dict()
    result["A"] = ["6", 2, "X"]
    result["B"] = "Hello"
    result["C"] = {"X":6, "Y" : 7}
    
    response = jsonify(result)
    return response  


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=8000)