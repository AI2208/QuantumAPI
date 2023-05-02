# -*- coding: utf-8 -*-
"""
Created on Mon May 1 16:09:04 2023

@author: aamna

This file defines a REST API for processing quantum circuits.

"""
import json
from flask import Flask, request, jsonify
from collections import OrderedDict

app = Flask(__name__)

# A dictionary to store the circuit information and results for each job id
jobs = {}

# A global counter to generate unique job ids
job_counter = 0

# API POST endpoint
@app.route('/job', methods=['POST'])
def process_job():
    try:
        circuit = request.json.get('circuit')
        
        # Verify existence and data type of circuit and ensure at least one gate
        if circuit is None or not isinstance(circuit, list) or len(circuit) < 1:
            raise ValueError('Invalid circuit format. The circuit must be a non-empty list.')

        # Validate the input - gate must be a dictionary with an axis (must be X, Y or Z) and an amount (must be an integer) key
        for i, gate in enumerate(circuit):
            if not isinstance(gate, dict):
                raise ValueError(f"Invalid gate format at index {i}. The gate must be a dictionary.")
              
            if not set(gate.keys()) == {'axis', 'amount'}:
                raise ValueError(f"Invalid gate at index {i}. The gate must have 'axis' and 'amount' keys only.")
              
            if gate['axis'] not in ['X', 'Y', 'Z']:
                raise ValueError(f"Invalid axis value at index {i}. The axis must be 'X', 'Y', or 'Z'.")
              
            if not isinstance(gate['amount'], int):
                raise ValueError(f"Invalid amount value at index {i}. The amount must be an integer.")
        
        # Optimize the circuit
        optimized_circuit = optimize_circuit(circuit)
        
        # Process the circuit and generate the result
        result = process_circuit(optimized_circuit)
        
        
        # If the optimized circuit is identical to the original, then 'optimized_circuit' will not need to be sent in the response body
        if optimized_circuit == circuit:
            optimized_circuit = None
            
        # Generate a unique job ID
        job_id = generate_job_id()

        # Store the circuit information and result for the job
        jobs[job_id] = {'circuit': circuit, 'optimized_circuit': optimized_circuit, 'result': result}

        # Return the ordered response
        response = OrderedDict([
            ('status', 'completed'),
            ('job_id', job_id),
            ('circuit', circuit),
            ('optimized_circuit',optimized_circuit),
            ('result', result)
        ])
        # Convert the dictionary to a JSON string
        json_response = json.dumps(response)
         
        # Add a newline character to the end of the response - this just cleans up the result
        json_response += '\n'
         
        return json_response, 200

    except ValueError as e:
        response = {
            'error_code': 400,
            'error_reason': str(e)
        }
        return jsonify(response), 400

    except Exception as e:
        response = {
            'error_code': 500,
            'error_reason': str(e)
        }
        return jsonify(response), 500
    
# API GET endpoint
@app.route('/job/<job_id>', methods=['GET'])
def get_job(job_id):
    try:
        # Verify that the job_id is an integer
        job_id = int(job_id)
    except ValueError:
        response = {
            'error_code': 400,
            'error_reason': 'Job ID must be an integer.'
        }
    return jsonify(response), 400

    if job_id not in jobs:
        response = {
            'error_code': 404,
            'error_reason': f"Job ID {job_id} not found."
        }
        return jsonify(response), 404

    # Sort the keys in the result dictionary by their integer values
    sorted_keys = sorted(jobs[job_id]['result'], key=lambda k: int(k))

    # Create an ordered dictionary with the sorted keys
    result = OrderedDict()
    for key in sorted_keys:
        result[str(key)] = jobs[job_id]['result'][key]

    # Create an ordered dictionary with the response keys in the desired order
    response = OrderedDict([
        ('status', 'completed'),
        ('job_id', job_id),
        ('circuit', jobs[job_id]['circuit']),
        ('result', result)
    ])
    
    # Create an ordered dictionary with the response keys in the desired order
    if jobs[job_id]['optimized_circuit']:
        response = OrderedDict([
            ('status', 'completed'),
            ('job_id', job_id),
            ('circuit', jobs[job_id]['circuit']),
            ('optimized_circuit',jobs[job_id]['optimized_circuit']),
            ('result', jobs[job_id]['result'])
        ])
    else:
        response = OrderedDict([
            ('status', 'completed'),
            ('job_id', job_id),
            ('circuit', jobs[job_id]['circuit']),
            ('result', jobs[job_id]['result'])
        ])
        
    # Convert the dictionary to a JSON string
    json_response = json.dumps(response)
    
    # Add a newline character to the end of the response - this just cleans up the result
    json_response += '\n'
    
    return json_response, 200

def optimize_circuit(circuit):
    # Combine consecutive gates of the same axis
    optimized_circuit = []
    for gate in circuit:
        if len(optimized_circuit) > 0 and gate['axis'] == optimized_circuit[-1]['axis']:
            optimized_circuit[-1]['amount'] += gate['amount']
        else:
            optimized_circuit.append(gate)
    return optimized_circuit

def process_circuit(circuit):
    # This function should take the circuit as input and return the result
    # This is currently just a hardcoded result, but circuit processing logic should go here
    result = {'0': 203, '1': 797}
    return result

def generate_job_id():
    # This function should generate and return a unique job ID
    # Implement the job ID generation logic here
     
    global job_counter
    job_id = str(job_counter)
    
    # Increment the job counter
    job_counter += 1
    return job_id

# Error handlers
@app.errorhandler(404)
def bad_request(error):
    return {
        'error_code': 404,
        'error_reason': 'Bad Request'
    }

@app.errorhandler(500)
def internal_server_error(error):
    return {
        'error_code': 500,
        'error_reason': 'Internal Server Error'
    }

if __name__ == '__main__':
    app.run()
