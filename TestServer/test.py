#!/usr/bin/python
import requests
import json
from receivedata import receiveData

while True:

    data = receiveData()
    r = requests.post('http://127.0.0.1:5000', data=json.dumps(data))

    print r.text
