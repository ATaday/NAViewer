#!/usr/bin/env python
import json
from flask import Flask, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

# receiving data to database 

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

# view of entire logs

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

# sorting logs by packet size 

@app.route('/size_sort', methods=['GET'])

def size_sort():

    activity = mongo.db.netactivity.find({ 'packet size':{"$gt": 0}}).sort( [('packet size', -1) ] )

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

# specific time of logs

@app.route('/specific_time', methods=['GET'])

def specific_time():

    activity = mongo.db.netactivity.find({ 'time':{"$gt": 1405001664.18 , "$lt": 1405001855.31}})

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

# total packet size of logs

@app.route('/total_size', methods=['GET'])

def total_size():	
    	
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': 'null', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}] )
    
    html = '%s' % packet_size['result']	

    return html

# sorting total packet size of any source address

@app.route('/saddr_size', methods=['GET'])

def saddr_size():	
    	
    html = ""
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$source address', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
    
    html = '%s' % packet_size['result']	

    return html

# sorting total packet size of any destination address

@app.route('/daddr_size', methods=['GET'])

def daddr_size():	
    
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$destination address', 
        'TotalSize': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'TotalSize': -1 } }])
     
    html = '%s' % packet_size['result']	

    return html

# sorting total packet size of any destination port

@app.route('/dport_size', methods=['GET'])

def dport_size():	
    	
    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$destination port', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
    
    html = '%s' % packet_size['result']

    return html

# total count of entire logs

@app.route('/total_count', methods=['GET'])

def total_count():	

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': 'null', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
} ] )
    
    html = '%s' % packet_size['result']

    return html

# total count of any source address

@app.route('/saddr_count', methods=['GET'])

def saddr_count():	

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$source address', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
}, { '$sort': { 'Total Count': -1 } } ] )
    
    html = '%s' % packet_size['result']

    return html

# total count of any destination address

@app.route('/daddr_count', methods=['GET'])

def daddr_count():	

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$destination address', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
}, { '$sort': { 'Total Count': -1 } } ] )
    
    html = '%s' % packet_size['result']

    return html

# total count of any destination port

@app.route('/dport_count', methods=['GET'])

def dport_count():	

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$destination port', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
}, { '$sort': { 'Total Count': -1 } } ] )
    
    html = '%s' % packet_size['result']

    return html

if __name__ == '__main__':
	app.run(debug=True)
