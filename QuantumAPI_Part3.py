# -*- coding: utf-8 -*-
"""
Created on Mon May 1 15:11:58 2023

@author: aamna

This file defines a REST API for processing quantum circuits.

"""

# Import necessary modules and packages
import json
from flask import Flask, request, jsonify
from collections import OrderedDict
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create a Flask application instance
app = Flask(__name__)

# Configure the application to use a PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/QuantumAPIdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)

# Create a Migrate instance
migrate = Migrate(app, db)

# Define the Job database model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    circuit = db.Column(db.JSON, nullable=False)
    result = db.Column(db.JSON, nullable=False) 
    
# API POST endpoint
@app.route('/job', methods=['POST'])
def process_job():
    try:
        circuit = request.json.get('circuit')
        
        # Verify existence and data type of circuit nd ensure at least one gate
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

        # Create a new Job object and add it to the database
        job = Job(circuit=circuit, result=result)
        db.session.add(job)
        db.session.commit()

        # Return the response
        response = {
            'status': 'completed',
            'job_id': job.id,
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

    job = Job.query.filter_by(id=job_id).first()
    if job is None:
        response = {
            'error_code': 404,
            'error_reason': f"Job ID {job_id} not found."
        }
        return jsonify(response), 404
    
    # Sort the keys in the result dictionary by their integer values
    sorted_keys = sorted(job.result, key=lambda k: int(k))

    # Create an ordered dictionary with the sorted keys
    result = OrderedDict()
    for key in sorted_keys:
        result[str(key)] = job.result[key]

    # Create an ordered dictionary with the response keys in the desired order
    response = OrderedDict([
        ('status', 'completed'),
        ('job_id', job_id),
        ('circuit', job.circuit),
        ('result', job.result)
    ])
    
    # Convert the dictionary to a JSON string
    json_response = json.dumps(response)
    
    # Add a newline character to the end of the response - this just cleans up the result
    json_response += '\n'
    
    return json_response, 200

def process_circuit(circuit):
    # This function should take the circuit as input and return the result
    # This is currently just a hardcoded result, but circuit processing logic should go here
    result = {'0': 203, '1': 797}
    return result

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
