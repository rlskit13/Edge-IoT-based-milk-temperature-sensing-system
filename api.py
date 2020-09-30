import flask
from flask import request, jsonify
import sqlite3
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import numpy as np


app = flask.Flask(__name__)
app.config["DEBUG"] = True

#@app.route('/', methods=['GET'])

#def home():
#    return '''<h1>Test 1.</h1>'''
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
  
@app.route('/api/v1/SensorData/all', methods=['GET'])
# Fetch all data from Tank_1 & Tank_2 tables
def api():
    conn = sqlite3.connect('Milk_Tank_Temperature.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_reading_1 = cur.execute('SELECT * FROM Tank_1_Data;').fetchall()

    all_reading_2 = cur.execute('SELECT * FROM Tank_2_Data;').fetchall()

    results = []
    results.append(all_reading_1)
    results.append(all_reading_2)

    return jsonify(results)

# Fetch all data from selected tables
@app.route('/api/v1/SensorData/tables/', methods=['GET'])

def api_table():
    if 'table' in request.args:
        table = request.args['table']
        conn = sqlite3.connect('Milk_Tank_Temperature.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        results = cur.execute(f'SELECT * FROM {table};').fetchall()
        return jsonify(results)
    else:
        return "Error: No such table."

# Fetch all data from selected tables on selected date
@app.route('/api/v1/SensorData/date/', methods=['GET'])
def date():
    table = request.args['table']
    date = request.args['date']

    conn = sqlite3.connect('Milk_Tank_Temperature.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(f'SELECT Temperature FROM {table} where Date_n_Time LIKE "{date}%";').fetchall()
    
    return jsonify(results)

# Fetch all data from selected tables within specific time (e.g. 16-Sep-2020_14:2*: *2:20-29pm) and calculate average
@app.route('/api/v1/SensorData/avg/', methods=['GET'])
def avg():
    table = request.args['table']
    date = request.args['date']

    conn = sqlite3.connect('Milk_Tank_Temperature.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results_1 = cur.execute(f'SELECT Temperature FROM {table} where Date_n_Time LIKE "{date}%";').fetchall()
    
    results = []

    i = 0
    while i != len(results_1):
        results.append(results_1[i]['Temperature'])
        print((results_1[i]['Temperature']))
        i += 1

    avg = np.mean(results)
    
    return jsonify({"Temperature_date":"{}".format(date)}, results_1, {"Avg Temp":"{:.4f}".format(avg)})


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404




if __name__ == '__main__':
    app.run(debug=True)
