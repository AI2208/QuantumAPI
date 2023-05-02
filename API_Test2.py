# -*- coding: utf-8 -*-
import requests

# Send a POST request to create a job
response = requests.post('http://localhost:5000/job', json={'circuit': [{'axis': 'X', 'amount': 2}, {'axis': 'Y', 'amount': 3}]})
job_id = response.json()['job_id']

# Send a GET request to retrieve the result for the job
response = requests.get(f'http://localhost:5000/job/{job_id}')

# Print the response
print(response.json())