# -*- coding: utf-8 -*-
import requests
import json

# Define the request data
circuit = [
    {'axis': 'X', 'amount': 1},
    {'axis': 'Y', 'amount': 2},
    {'axis': 'Z', 'amount': 3},
]
data = {'circuit': circuit}

# Send the request to the Flask app
response = requests.post('http://localhost:5000/job', json=data)

# Print the response
print(response.status_code)
print(json.loads(response.content))