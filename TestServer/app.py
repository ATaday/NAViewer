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

def view():

    activity = mongo.db.netactivity.find()

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

@app.route('/size_sort', methods=['GET'])

def size_sort():

    activity = mongo.db.netactivity.find({ 'packet size':{"$gt": 1 }}).sort( [('packet size', -1) ] )

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


@app.route('/saddr_sort', methods=['GET'])

def saddr_sort():	
    
    html = '<table width="80%"><td><u><b>Packet Size</b></u></td>'
    	
    packet_size = mongo.db.netactivity.aggregate([ { 
    '$group': { 
        '_id': '$source address', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
    
    html = html + '<tr>' 
    html = html + '<td>%s</td>' % packet_size
    html = html + '</tr>'
    html = html + '</table>'

    response = html

    return response

@app.route('/daddr_sort', methods=['GET'])

def daddr_sort():	
    
    html = '<table width="80%"><td><u><b>Packet Size</b></u></td>'
    	
    packet_size = mongo.db.netactivity.aggregate([ { 
    '$group': { 
        '_id': '$destination address', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
    
    html = html + '<tr>' 
    html = html + '<td>%s</td>' % packet_size
    html = html + '</tr>'
    html = html + '</table>'

    response = html

    return response

@app.route('/dport_sort', methods=['GET'])

def dport_sort():	
    
    html = '<table width="80%"><td><u><b>Packet Size</b></u></td>'
    	
    packet_size = mongo.db.netactivity.aggregate([ { 
    '$group': { 
        '_id': '$destination port', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
    
    html = html + '<tr>' 
    html = html + '<td>%s</td>' % packet_size
    html = html + '</tr>'
    html = html + '</table>'

    response = html

    return response

if __name__ == '__main__':
	app.run(debug=True)
