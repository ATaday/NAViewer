#!/usr/bin/env python
import jinja2
import json
from flask import Flask, request
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
	
    template = jinja2.Template("""{% for record in records %}
			          {{ record }}
				  {% endfor %}""")

    log = [record['time'] for record in activity]
    result = template.render(records=log) 

    return result
