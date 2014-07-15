#!/usr/bin/env python
import jinja2
import json
from flask import Flask, request, render_template
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app)

# saving all data to database

@app.route('/', methods=['GET', 'POST'])

def saveData():

    if request.method == 'POST':

        data = request.get_json(force=True)

        mongo.db.netactivity.insert(data)

        response = 'ok'

    elif request.method == 'GET':

        print "GET"

        response = """<p>This URL is reserved for posting data from clients.</p>"""

    return response

# view of all logs

@app.route('/view', methods=['GET'])

def view():

    activity = mongo.db.netactivity.find()

    log = [record for record in activity]

    return render_template('view.html', records=log)

# specific time of all logs

@app.route('/specific_time', methods=['GET'])

def specific_time():

    activity = mongo.db.netactivity.find( { 'time': { "$gt": 1405434044.88 , "$lt": 1405434167.98 } } )
    
    log = [record for record in activity]

    return render_template('specific_time.html', records=log)

if __name__ == '__main__':
	app.run(debug=True)
