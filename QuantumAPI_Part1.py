# -*- coding: utf-8 -*-
"""
Created on Mon May 1 13:51:58 2023

@author: aamna

This file defines a REST API for processing quantum circuits.

"""

from flask import Flask, request, jsonify

app = Flask(__name__)

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
        

        # Process the circuit and generate the result
        result = process_circuit(circuit)

        # Generate a unique job ID
        job_id = generate_job_id()

        # Return the response
        response = {
            'status': 'completed',
            'job_id': job_id,
            'result': result
        }
        return jsonify(response), 200

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
