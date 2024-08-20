from flask import Flask, jsonify, request
from flask_cors import CORS #comment this on deployment
import sqlite3
import pickle;
import numpy as np;

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
clf= pickle.load(open("decisiontree.pickle", 'rb'))
CORS(app) #comment this on deployment
con = sqlite3.connect("dsproject2023.db", check_same_thread=False)
cur = con.cursor()

def getResponse(rows,columns):
    sql = """SELECT category_name,count(*) 
             FROM restuarant
             WHERE city_name = ?
             GROUP BY category_name
             ORDER BY count(*) DESC
             LIMIT 0,10"""
    
    #สร้าง BarChart Data
    labels = []
    data = []
    for row in rows :
        labels.append(row[0])
        data.append(row[1])

    result = dict()
    result["columns"] = columns
    result["rows"] = rows
    result["chart"] = dict()
    result["chart"]["labels"] = labels
    result["chart"]["data"] = data


    response = jsonify(result)
    
    return response

def getHistogram(listData,bins):
    hist, bin_edges = np.histogram(listData, bins=bins)
    rows = []
    for i in range(len(hist)):
        middle = (bin_edges[i] +  bin_edges[i+1])/2;
        row = (float(middle), int(hist[i]))
        rows.append(row)
    return rows


@app.route('/')
def index():
    return 'Python is fun'
#ex01 combobox ดูตัวอย่างจากนี้ได้
@app.route('/resturant/citynames/')
def getCityNames():
    #เลือกเฉพาะจังหวัดที่มีร้าน > 1000
    sql = """SELECT city_name, count(*)
             FROM restuarant
             GROUP BY city_name
             HAVING count(*) > 1000"""
    res = cur.execute(sql)
    rows = res.fetchall()
    columns =  ["ชื่อจังหวัด", "จำนวนร้าน"]

    response = getResponse(rows,columns)
    
    return response
#ex01combobox
@app.route('/api/ex01combobox/a')
def ex01combobox():
    #คอลัมที่เลือกให้มี 2 คอลัมเท่านั้นเช่น "ชื่อจังหวัด", "จำนวนร้าน"
    sql = """SELECT city_name, count(*) FROM restuarant GROUP BY city_name"""
    res = cur.execute(sql)
    rows = res.fetchall()
    columns =  ["city", "numberOfshops"]

    response = getResponse(rows,columns)
    
    return response

#ex01combobox
@app.route('/api/ex01combobox/b')
def ex01comboboxB():
    rows = [('Samut Songkhram',10)
            , ('Phra Nakhon Si Ayutthaya',20)
            , ('Bangkok Metropolitan Region', 30)
            , ('Chon Buri', 40)]
    columns =  ["city", "numberOfshops"]

    response = getResponse(rows,columns)
    
    return response

#ex02combobox
@app.route('/api/ex02combobox/a')
def ex02comboboxA():
    #คอลัมที่เลือกให้มี 2 คอลัมเท่านั้นเช่น "ชื่อจังหวัด", "จำนวนร้าน"
    sql = """SELECT category_name, count(*) 
             FROM restuarant GROUP BY category_name 
             ORDER BY Count(*) DESC 
             LIMIT 0,20
          """
    res = cur.execute(sql)
    rows = res.fetchall()
    columns =  ["category_name", "numberOfshops"]

    response = getResponse(rows,columns)
    
    return response


@app.route('/resturant/categories/')
def getCategoryNames():
    #เลือกเฉพาะจังหวัดที่มีร้าน > 1000
    sql = """SELECT category_name, count(*)
             FROM restuarant
             GROUP BY category_name
             HAVING count(*) > 1000"""
    res = cur.execute(sql)
    rows = res.fetchall()
    columns =  ["ประเภทร้าน", "จำนวนร้าน"]

    response = getResponse(rows,columns)
    
    return response


#ใช้เป็นตัวอย่างสำหรับ api  ดึงข้อมูลตาม input ที่ user เลือก
@app.route('/resturant/top10categories/<city_name>')
def top10catetoriesByCity(city_name):
    sql = """SELECT category_name,count(*) 
             FROM restuarant
             WHERE city_name = ?
             GROUP BY category_name
             ORDER BY count(*) DESC
             LIMIT 0,10"""
    param = [str(city_name)]
    res = cur.execute(sql,param)
    rows = res.fetchall()
    columns =  ["ประเภทร้าน", "จำนวนร้าน"]
    response = getResponse(rows,columns)
    
    return response
#ex01UserInput
#http://127.0.0.1:5000/api/userInput/Samut%20Songkhram

@app.route('/api/userInput/<input1>')
def ex01UserInput(input1):
    sql = """SELECT zipcode,count(*) 
            FROM restuarant
            WHERE city_name = ? and zipcode is NOT NULL
            GROUP BY zipcode
            ORDER BY count(*) DESC
            LIMIT 0,10"""
    param = [str(input1)]
    res = cur.execute(sql,param)
    rows = res.fetchall()
    columns =  ["รหัสไปรษณีย์", "จำนวนร้าน"]
    response = getResponse(rows,columns)
    
    return response

#ใช้เป็นตัวอย่างสำหรับ api  ดึงข้อมูลตาม input ที่ user เลือก (ex02)
@app.route('/resturant/rating/<city_name>')
def getRating(city_name):
    #เลือกเฉพาะจังหวัดที่มีร้าน > 1000
    sql = """SELECT weighted_average_rating
             FROM restuarant WHERE city_name = ?"""
    param = [str(city_name)]
    res = cur.execute(sql,param)
    rows = res.fetchall()
    listData = []
    for row in rows:
        listData.append(row[0])

    rows = getHistogram(listData,10)
    columns =  ["weighted_average_rating", "จำนวนร้าน"]
    response = getResponse(rows,columns)

    return response

#ใช้เป็นตัวอย่างสำหรับ api  ดึงข้อมูลตาม input ที่ user เลือก (ex02)
#http://127.0.0.1:5000/api/UserInputEx02/Thai
@app.route('/api/UserInputEx02/<input1>')
def ex02UserInput(input1):
    #เลือกเฉพาะจังหวัดที่มีร้าน > 1000
    sql = """SELECT number_of_reviews
             FROM restuarant WHERE category_name = ?"""
    param = [str(input1)]
    res = cur.execute(sql,param)
    rows = res.fetchall()
    listData = []
    for row in rows:
        listData.append(row[0])

    rows = getHistogram(listData,10)
    columns =  ["number_of_reviews", "จำนวนร้าน"]
    response = getResponse(rows,columns)

    return response


@app.route('/resturant/sqltest/')
def top10catetory():
    sql = """SELECT category_name,count(*) 
             FROM restuarant
             GROUP BY category_name
             ORDER BY count(*) DESC
             LIMIT 0,10"""
    res = cur.execute(sql)
    rows = res.fetchall()
    
    #สร้าง BarChart Data
    labels = []
    data = []
    for row in rows :
        labels.append(row[0])
        data.append(row[1])

    result = dict()
    result["columns"] = ["ประเภทร้าน", "จำนวนร้าน"]
    result["rows"] = rows
    result["barchart"] = dict()
    result["barchart"]["labels"] = labels
    result["barchart"]["data"] = data


    response = jsonify(result)
    
    return response


#ตัวอย่าง Ex05 Data
@app.route('/abalone/data/')
def getAbaloneData():
    #columns = '"Sex","Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight","Rings"'
    columns = '"Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight","Rings"'
    sql = "SELECT " + columns + "FROM abalone"
                
    res = cur.execute(sql)
    rows = res.fetchall()
    

    result = dict()
    result["columns"] = ["Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight","Rings"]
    result["rows"] = rows


    response = jsonify(result)
    
    return response
#http://127.0.0.1:5000/api/dataex05
@app.route('/api/dataex05/')
def dataex05():
    #columns = '"Sex","Length","Diameter","Height","Whole weight","Shucked weight","Viscera weight","Shell weight","Rings"'
    columns = '"Length","Height","Shell weight","Rings"'
    sql = "SELECT " + columns + "FROM abalone "
                
    res = cur.execute(sql)
    rows = res.fetchall()
    

    result = dict()
    result["columns"] = ["Length","Height","Shell weight","Rings"]
    result["rows"] = rows


    response = jsonify(result)
    
    return response

#ตัวอย่าง Ex05 Predict
@app.route('/abalone/predict/',methods = ['POST'])
def predictAbaloneRing():
    
    if request.method == 'POST':
      Length = request.form['Length']
      Diameter = request.form['Diameter']
      Height = request.form['Height']
      Wholeweight = request.form['Wholeweight']
      Shuckedweight = request.form['Shuckedweight']
      Visceraweight = request.form['Visceraweight']
      Shellweight = request.form['Shellweight']
      predict_input = np.array([[Length,Diameter,Height,Wholeweight,Shuckedweight,Visceraweight,Shellweight]])
      predict_output = clf.predict(predict_input)
    
    
    return jsonify(predict_output[0])

@app.route('/api/predictex05/',methods = ['POST'])
def predictex05():
    
    if request.method == 'POST':
      Length = request.form['Length']
      Height = request.form['Height']
      Shellweight = request.form['Shellweight']
      predict_input = np.array([[Length,Height,Shellweight]])
      predict_output = clf.predict(predict_input)
    
    
    return jsonify(predict_output[0])

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=8000)