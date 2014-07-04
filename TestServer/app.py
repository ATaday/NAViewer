#!/usr/bin/env python
import json
from flask import Flask, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])

def saveData():

    if request.method == 'POST':

        data = request.get_json(force=True)

        mongo.db.netactivity.insert(data)

        response = 'ok'

    elif request.method == 'GET':

        print "GET"

        response = """
        <p>This URL is reserved for posting data from clients.</p>
        """

    return response

@app.route('/view', methods=['GET'])

def index():

    activity = mongo.db.netactivity.find() 
    size_total = 0 
    html = '<table width="80%"><td><u><b>Time</b></u></td><td><u><b>Protocol</b></u></td><td><u><b>Source Address</b></u></td><td><u><b>Destination Address</b></u></td><td><u><b>Destination Port</b></u></td><td><u><b>Packet Size</b></u></td>'

    for record in activity:
        html = html + '<tr>' 
	html = html + '<td>%s</td>' % record['time']
	html = html + '<td>%s</td>' % record['protocol']
	html = html + '<td>%s</td>' % record['source address']
        html = html + '<td>%s</td>' % record['destination address']
	html = html + '<td>%s</td>' % record['destination port']
        html = html + '<td>%s</td>' % record['packet size']
        html = html + '</tr>'
    html = html + '</table>'

    response = html

    return response

@app.route('/length', methods=['GET'])

def size():

    activity = mongo.db.netactivity.find() 

    size_total = 0 
	
    html = '<table width="80%"><td><u><b>Total Size</b></u></td><td><u><b>Source Address</b></u></td><td><u><b>Destination Port</b></u></td>'

    for record in activity:
        html = html + '<tr>' 
	size_total = size_total + record['packet size']
    	html = html + '<td>%s</td>' % size_total
        html = html + '<td>%s</td>' % record['source address']
        html = html + '<td>%s</td>' % record['destination port']
        html = html + '</tr>'
    html = html + '</table>'

    response = html

    return response

if __name__ == '__main__':
	app.run(debug=True)
