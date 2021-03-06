#!/usr/bin/env python
import jinja2
import json
from flask import Flask, request, render_template
from flask.ext.pymongo import PyMongo

app = Flask(__name__)

mongo = PyMongo(app)

# saving all data to database

@app.route('/', methods=['GET', 'POST'])

def save_data():

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

    activity = mongo.db.netactivity.find( { 'time': { "$gt": 1405520605.82 , "$lt": 1405520614.3 } } )
    
    log = [record for record in activity]

    return render_template('specific_time.html', records=log)

# sorting all logs as packet size 

@app.route('/size_sort', methods=['GET'])

def size_sort():

    activity = mongo.db.netactivity.find( { 'packet size': { "$gt": 0 } } ).sort( [ ('packet size', -1) ] )
  
    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Size': { '$sum': "$packet size" } } } ] )
    
    log_per = [record_per for record_per in t_size['result']] 
 
    log = [record for record in activity]    

    return render_template('size_sort.html', records=log, records_per=log_per)

# total packet size of all logs

@app.route('/total_size', methods=['GET'])

def total_size():	    	

    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Size': { '$sum': "$packet size" } } } ] )

    log = [record for record in packet_size['result']]    

    return render_template('total_size.html', records=log)

# sorting packet size of source address

@app.route('/saddr_size', methods=['GET'])

def saddr_size():	
    	    
    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$source address', 'SAddr Size': { '$sum': "$packet size" } } } , { '$sort': { 'SAddr Size': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Size': { '$sum': "$packet size" } } } ] )
    
    log_per = [record_per for record_per in t_size['result']] 

    log = [record for record in packet_size['result']]    

    return render_template('saddr_size.html', records=log, records_per=log_per)

# sorting packet size of destination address

@app.route('/daddr_size', methods=['GET'])

def daddr_size():	
   
    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$destination address', 'DAddr Size': { '$sum': "$packet size" } } } , { '$sort': { 'DAddr Size': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Size': { '$sum': "$packet size" } } } ] )
    
    log_per = [record_per for record_per in t_size['result']] 

    log = [record for record in packet_size['result']]    

    return render_template('daddr_size.html', records=log, records_per=log_per)   

# sorting packet size of destination port

@app.route('/dport_size', methods=['GET'])

def dport_size():	
    	
    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$destination port', 'DPort Size': { '$sum': "$packet size" } } } , { '$sort': { 'DPort Size': -1 } } ] )
      
    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Size': { '$sum': "$packet size" } } } ] )
    
    log_per = [record_per for record_per in t_size['result']] 

    log = [record for record in packet_size['result']]    

    return render_template('dport_size.html', records=log, records_per=log_per)

# total average size of all logs

@app.route('/total_avg', methods=['GET'])

def total_avg():	
    	
    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Average': { '$avg': "$packet size" } } } ] )
    
    log = [record for record in t_size['result']]    

    return render_template('total_avg.html', records=log)

# sorting average size of source address

@app.route('/saddr_avg', methods=['GET'])

def saddr_avg():	

    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$source address', 'SAddr Average': { '$avg': "$packet size" } } } , { '$sort': { 'SAddr Average': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Average': { '$avg': "$packet size" } } } ] )

    log_per = [record_per for record_per in t_size['result']] 

    log = [record for record in packet_size['result']]    

    return render_template('saddr_avg.html', records=log, records_per=log_per)

# sorting average size of destination address

@app.route('/daddr_avg', methods=['GET'])

def daddr_avg():	

    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$destination address', 'DAddr Average': { '$avg': "$packet size" } } } , { '$sort': { 'DAddr Average': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Average': { '$avg': "$packet size" } } } ] )

    log_per = [record_per for record_per in t_size['result']] 
    
    log = [record for record in packet_size['result']]    

    return render_template('daddr_avg.html', records=log, records_per=log_per)

# sorting average size of destination port

@app.route('/dport_avg', methods=['GET'])

def dport_avg():	
 	
    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$destination port', 'DPort Average': { '$avg': "$packet size" } } } , { '$sort': { 'DPort Average': -1 } } ] )
    
    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Average': { '$avg': "$packet size" } } } ] )

    log_per = [record_per for record_per in t_size['result']] 

    log = [record for record in packet_size['result']]    

    return render_template('dport_avg.html', records=log, records_per=log_per)

# total count of all logs

@app.route('/total_count', methods=['GET'])

def total_count():	

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Count': { '$sum': 1 } } } ] )
    
    log = [record for record in t_size['result']]    

    return render_template('total_count.html', records=log)

# sorting count of source address

@app.route('/saddr_count', methods=['GET'])

def saddr_count():	

    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$source address', 'SAddr Count': { '$sum': 1 } } } , { '$sort': { 'SAddr Count': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Count': { '$sum': 1 } } } ] )

    log_per = [record_per for record_per in t_size['result']]  

    log = [record for record in packet_size['result']]    

    return render_template('saddr_count.html', records=log, records_per=log_per)

# sorting count of destination address

@app.route('/daddr_count', methods=['GET'])

def daddr_count():	

    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$destination address', 'DAddr Count': { '$sum': 1 } } } , { '$sort': { 'DAddr Count': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Count': { '$sum': 1 } } } ] )

    log_per = [record_per for record_per in t_size['result']]  

    log = [record for record in packet_size['result']]    

    return render_template('daddr_count.html', records=log, records_per=log_per)

# sorting count of destination port

@app.route('/dport_count', methods=['GET'])

def dport_count():	

    packet_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': '$destination port', 'DPort Count': { '$sum': 1 } } } , { '$sort': { 'DPort Count': -1 } } ] )

    t_size = mongo.db.netactivity.aggregate( [ { '$group': { '_id': 'null', 'Total Count': { '$sum': 1 } } } ] )

    log_per = [record_per for record_per in t_size['result']]  

    log = [record for record in packet_size['result']]    

    return render_template('dport_count.html', records=log, records_per=log_per)

if __name__ == '__main__':
    app.run(debug=True)
