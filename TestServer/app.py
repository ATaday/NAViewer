#!/usr/bin/env python
import json
from flask import Flask, request
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

# receiving all data to database 

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

# sorting entire logs by packet size 

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

# specific time of entire logs

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

# total packet size of entire logs

@app.route('/total_size', methods=['GET'])

def total_size():	    	

    html = '<table width="80%"><td><u><b>Total Size</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': 'null', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['Total Size']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting packet size of any source address

@app.route('/saddr_size', methods=['GET'])

def saddr_size():	
    	
    html = '<table width="80%"><td><u><b>Source Address</b></u></td><td><u><b>Packet Size</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$source address', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
 
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Size']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting packet size of any destination address

@app.route('/daddr_size', methods=['GET'])

def daddr_size():	
    
    html = '<table width="80%"><td><u><b>Destination Address</b></u></td><td><u><b>Packet Size</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$destination address', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }])
     
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Size']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting packet size of any destination port

@app.route('/dport_size', methods=['GET'])

def dport_size():	
    	
    html = '<table width="80%"><td><u><b>Destination Port</b></u></td><td><u><b>Packet Size</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$destination port', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Size': -1 } }] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Size']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# total average size of entire logs

@app.route('/avg_size', methods=['GET'])

def avg_size():	

    html = '<table width="80%"><td><u><b>Total Average Size</b></u></td>'
    	
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': 'null', 
        'Total Average': { 
            '$avg': "$packet size" 
        }
    } 
}] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['Total Average']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting average size of any source address

@app.route('/saddr_avg', methods=['GET'])

def saddr_avg():	
    	
    html = '<table width="80%"><td><u><b>Source Address</b></u></td><td><u><b>Average Size</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$source address', 
        'Total Average': { 
            '$avg': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Average': -1 } }])
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Average']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting average size of any destination address

@app.route('/daddr_avg', methods=['GET'])

def daddr_avg():	
    	
    html = '<table width="80%"><td><u><b>Destination Address</b></u></td><td><u><b>Average Size</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$destination address', 
        'Total Average': { 
            '$avg': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Average': -1 } }])
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Average']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting average size of any destination port

@app.route('/dport_avg', methods=['GET'])

def dport_avg():	

    html = '<table width="80%"><td><u><b>Destination Port</b></u></td><td><u><b>Average Size</b></u></td>'
    	
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$destination port', 
        'Total Average': { 
            '$avg': "$packet size" 
        }
    } 
}, { '$sort': { 'Total Average': -1 } }])
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Average']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# total count of entire logs

@app.route('/total_count', methods=['GET'])

def total_count():	

    html = '<table width="80%"><td><u><b>Total Count</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': 'null', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
} ] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['Total Count']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting count of any source address

@app.route('/saddr_count', methods=['GET'])

def saddr_count():	

    html = '<table width="80%"><td><u><b>Source Address</b></u></td><td><u><b>Count</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$source address', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
}, { '$sort': { 'Total Count': -1 } } ] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Count']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting count of any destination address

@app.route('/daddr_count', methods=['GET'])

def daddr_count():	

    html = '<table width="80%"><td><u><b>Destination Address</b></u></td><td><u><b>Count</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$destination address', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
}, { '$sort': { 'Total Count': -1 } } ] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Count']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# sorting count of any destination port

@app.route('/dport_count', methods=['GET'])

def dport_count():	

    html = '<table width="80%"><td><u><b>Destination Port</b></u></td><td><u><b>Count</b></u></td>'

    packet_size = mongo.db.netactivity.aggregate([ {   
       '$group': {
	 '_id': '$destination port', 
        'Total Count': { 
            '$sum': 1 
        }
    } 
}, { '$sort': { 'Total Count': -1 } } ] )
    
    for record in packet_size['result']:
        html = html + '<tr>'
        html = html + '<td>%s</td>' % record['_id']
        html = html + '<td>%s</td>' % record['Total Count']
        html = html + '</tr>'

    html = html + '</table>'

    return html

# percent size of source address

@app.route('/saddr_per', methods=['GET'])

def saddr_per():	    	

    html = '<table width="80%"><td><u><b>Source Address</b></u></td><td><u><b>Percentage</b></u></td>'
  
    t_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': 'null', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}] )
    
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$source address', 
        'Packet Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Packet Size': -1 } }] )
 
    for record in packet_size['result']:
	for record2 in t_size['result']:
    	    html = html + '<tr>'
    	    html = html + '<td>%s</td>' % record['_id']
	    a= 100*float(record['Packet Size']) / float(record2['Total Size'])       
	    html = html + '<td>%s</td>' % a
    	    html = html + '</tr>'

    html = html + '</table>'

    return html

# percent size of destination address

@app.route('/daddr_per', methods=['GET'])

def daddr_per():	    	

    html = '<table width="80%"><td><u><b>Destination Address</b></u></td><td><u><b>Percentage</b></u></td>'
  
    t_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': 'null', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}] )
    
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$destination address', 
        'Packet Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Packet Size': -1 } }] )
 
    for record in packet_size['result']:
	for record2 in t_size['result']:
    	    html = html + '<tr>'
    	    html = html + '<td>%s</td>' % record['_id']
	    a= 100*float(record['Packet Size']) / float(record2['Total Size'])       
	    html = html + '<td>%s</td>' % a
    	    html = html + '</tr>'

    html = html + '</table>'

    return html

# percent size of destination port

@app.route('/dport_per', methods=['GET'])

def dport_per():	    	

    html = '<table width="80%"><td><u><b>Destination Port</b></u></td><td><u><b>Percentage</b></u></td>'
  
    t_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': 'null', 
        'Total Size': { 
            '$sum': "$packet size" 
        }
    } 
}] )
    
    packet_size = mongo.db.netactivity.aggregate( [{ 
    '$group': { 
        '_id': '$destination port', 
        'Packet Size': { 
            '$sum': "$packet size" 
        }
    } 
}, { '$sort': { 'Packet Size': -1 } }] )
 
    for record in packet_size['result']:
	for record2 in t_size['result']:
    	    html = html + '<tr>'
    	    html = html + '<td>%s</td>' % record['_id']
	    a= 100*float(record['Packet Size']) / float(record2['Total Size'])       
	    html = html + '<td>%s</td>' % a
    	    html = html + '</tr>'

    html = html + '</table>'

    return html


if __name__ == '__main__':
	app.run(debug=True)
