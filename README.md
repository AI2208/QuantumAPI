# QuantumAPI
OQC Technical Test (candidate: Aamna Irfan). This repository contains the solutions to Parts 1, 2, 3, 4 and 5 from the Technical Test document. The purpose of the code is to implement the tasks and requirements as outlined within this document. Instructions are provided below to run and test the solutions.

## Installation and Setup

### Introduction:
The Flask server is a lightweight web application framework that allows you to create and deploy web applications quickly and easily. These instructions will guide you through the process of installing and setting up the Flask server on your local machine.

### System Requirements:
To run the Flask server, you will need to have Python 3 installed on your computer.

### Steps for setup:
1. **Clone the repository:** Start by cloning this repository to your local machine. You can do this by opening a terminal or command prompt window and typing:
`git clone https://github.com/AI2208/QuantumAPI.git`.
2. **Install required packages:** Navigate to the project directory and install the required packages by running the following command: `pip install -r requirements.txt`
3. **Start the server:** Once the packages have been installed, start the Flask server by running the following command: `python QuantumAPI_PartX.py`
where X should be replaced by the relevant task number.
4. **Verify server is running:** The server should now be running on `http://localhost:5000/.` You can verify this by opening a web browser and navigating to that URL.

### Troubleshooting:
If you encounter any issues during installation, please refer to the Flask documentation (https://flask.palletsprojects.com/en/2.3.x/ for most recent version) or search for solutions online. Common issues include package conflicts, incorrect versions of Python or other dependencies, or issues with firewalls or security settings.

## Design & Implementation Process
### Part 1
#### Defining the problem
The endpoint `/job` accepts POST requests in the form of "circuits" which have the following format:
```
Post Request : {
        “circuit”: [gate]
}
```

The gate object has the following schema:
```
{
‘axis’ : “X” or “Y” or “Z”
‘amount’ : Int
}
```
Therefore, the circuit object contains a list of gates, with an axis key (must be "X", "Y", or "Z") and an amount key (must be an integer) specified for each gate. An example is provided below:
```
{
    "circuit": [
        {
            "axis": "X",
            "amount": 90
        },
        {
            "axis": "Y",
            "amount": -90
        },
        {
            "axis": "Z",
            "amount": 180
        }
    ]
}
```

The endpoint `/job` responds with a JSON object with the following format:
```
{
    "status": "completed",
    "job_id": "1",
    "result": {
        "0": 203,
        "1": 797
    }
}
```
The status key indicates whether the request was successful or not, the `job_id` key is a unique identifier for the job, and the result key is a dictionary containing the results of the circuit processing.

#### Required tests
As expected in TDD, I have converted these software requirements to test cases prior to implementation. As I am developing the POST endpoint, my test cases will consist of both valid and invalid POST requests to the `/job` endpoint, which should return a custom error message for an invalid input or a suitable response body in the case of a valid input to confirm the successful creation of a new `job`. 

This collection of predefined tests and the expected outputs from the program are provided in the `Part1_Tests.txt` file. The instructions for explicitly testing the code on your local machine by inputting these test circuits are included in the 'Testing' section below; this section is reserved for defining the tests prior to implementation and discussing the reasoning behind selecting these test cases. Although the actual test cases are included in the 'Part1_Tests.txt' file, 
the general types of inputs for the test cases have been listed below:

1. Valid POST request with a **single gate**
2. Valid POST request with **multiple gates**
3. Invalid POST request with **empty circuit**
4. Invalid POST request with **invalid circuit format**
5. Invalid POST request with **invalid gate format**
6. Invalid POST request with **unknown gate key**
7. Invalid POST request with **invalid axis value**
8. Invalid POST request with **non-integer amount**
9. Invalid POST request with **multiple errors**
10. Invalid POST request with **unexpected error**

These test cases do not claim to be exhaustive, but do provide a general framework for testing to determine whether the program satisfies the constraints defined in the problem. As shown in `Part1_Tests.txt`, each of these sections has some explicit cases which involve a different data type or a different arrangement of gates in the circuit. These tests will be used in the 'Testing' section to determine the success and robustness of the solution.

#### Implementation

To implement the solution, I created a new Python file called `QuantumAPI_Part1.py` and  I chose to use the Flask web framework for the application, as opposed to the Django framework, as I have more experience with it. 

Firstly, an instance of the Flask class is created and a single POST endpoint `/job` is created using the `@app.route` decorator, with the methods parameter set to `['POST']`. The `process_job()` function handles the incoming POST requests. It validates the request payload, processes the circuit, generates a unique job ID, and constructs the response accordingly. The `process_job()` function has been provided below for ease of reference:

```
# API POST endpoint
@app.route('/job', methods=['POST'])
def process_job():
    try:
        circuit = request.json.get('circuit')
        
        # Verify existence and data type of circuit
        if circuit is None or not isinstance(circuit, list):
            raise ValueError('Invalid circuit format. The circuit must be a list.')

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
```

Inside the `process_job()` function, there is a try-except block to catch any unhandled exceptions that might occur while processing the request. If an exception is caught, a 500 (Internal Server Error) is raised and a custom error response is returned. 

Within this block, JSON data is first extracted from the request using `request.get_json()` in order to retrieve the circuit information. This implementation checks if the "circuit" key exists in the request JSON object and if the "circuit" object is a list; if it doesn't exist or is not a list, a custom error message with a 400 (Bad Request) status code is returned. 

It then loops through each gate in the circuit and ensures that every gate is a dictionary with only "axis" and "amount" keys. It also validates the axis and amount values, testing whether the axis is one of 'X', 'Y' or 'Z' and that the amount is an integer. If the input is invalid, it returns a custom error with the 400 error code. Furthermore, the error messages contain specific information about the location and nature of the error, such as the index of the gate that caused the error and a reminder of the allowed values. This can make it easier for the user to understand and correct the error. 

If the circuit is valid, it is processed using the `process_circuit()` function. Currently, it returns a hardcoded result, but the actual circuit processing logic (e.g. applying the rotation to the qubit and returning the result object that contains the measurement outcomes for each qubit) should be implemented here if desired.

After this processing, a `job_id` needs to be generated to uniquely identify the job; it is also currently hardcoded, like the result, however, this is quite an easy fix. Initially, I planned to use the `uuid` library to randomly generate the `job_id`, but I decided to go with an incrementing integer instead, as it is more readable and more memory efficient. It is also easier to update and modify this method than the `uuid` method, if required. The `generate_job_id()` function generates a job ID using a simple counter and increments the counter for each new job. Finally, the response is returned, in JSON format using the `jsonify()` function from Flask, with a 200 status code, including a unique job ID and a hardcoded result.

Lastly, error handlers have been included in the end for common error scenarios, whereas the try-except block in the endpoint implementation is for custom error scenarios to provide more detail on the specific error.

#### Testing
##### Setup 
To test this endpoint, you can send a POST request to `http://localhost:5000/job` with a JSON body with the following format:

```
{
    "circuit": [
        {"axis": "X", "amount": 90},
        {"axis": "Y", "amount": -90},
        {"axis": "Z", "amount": 180}
    ]
}
```
You can send a POST request to `http://localhost:5000/job` using a tool like `curl` or a HTTP client like `Postman` or `Insomnia`. Here is an example using `curl`:

```
curl --location --request POST 'http://localhost:5000/job' \
--header 'Content-Type: application/json' \
--data-raw '{
    "circuit": [
        {"axis": "X", "amount": 1},
        {"axis": "Y", "amount": 2},
        {"axis": "Z", "amount": 3}
    ]
}'

```
This sends a POST request to `http://localhost:5000/job` with a JSON body containing a "circuit" key with a list of gate objects. Note that this command is split over several lines for readability, but you should enter it as a single line in your terminal. 

Here is what each part of the command does:

* `-X POST` specifies that you want to send a **POST** request.
* `http://localhost:5000/job` is the **URL** you want to send the request to.
* `-H 'Content-Type: application/json' ` sets the Content-Type header to application/json as the request body is in JSON format.
* `-d '{ ... }'` specifies the JSON data (payload) you want to send in the request body (i.e. the circuit).

Note that this assumes that you have already started the Flask server and it is listening on port 5000 on your localhost. If you haven't started the server yet, you can run the Flask app by running the Python script that contains the app code, e.g., `python QuantumAPI_Part1.py`.

When you send a POST request with a valid "circuit" JSON object (i.e. circuit contains only known gates with the required keys axis and amount), you should receive a success response with a 200 status code, as shown:

```
{
    "status": "completed",
    "job_id": "1234",
    "result": {
        "0": 203,
        "1": 797
    }
}
```

If the request is invalid and the server returns an error, the response will contain a JSON payload with an error code and error reason. If you intentionally cause an error, you should receive a custom error message with a 500 status code. Or, if there is an issue with your request, a custom error message with a 400 status code is outputted. For example, if you send a request without a "circuit" key or with an empty list, the response should look like this:


```
{
    "error_code": "400",
    "error_reason": "Invalid circuit format. The circuit must be a non-empty list."
}
```

You can modify the curl command to send different JSON payloads to test different scenarios and see how the server responds. You may construct your own test cases, or utilise the cases from the `Part1_Tests.py` file by copying each test case into the payload of the POST request and comparing the output to the expected response. Make sure to test each case thoroughly to ensure that your API is functioning correctly. 

Lastly, there may sometimes be errors with the syntax in the POST request; remember to be very careful and use brackets before certain/illegal characters if you are experiencing issues. For example, due to the many symbols in the payload, I decided to use the following request format to keep everything organised and separate:

```
curl -X POST -H "Content-Type: application/json" -d "{\"circuit\": [{\"axis\": \"X\", \"amount\": 1},{\"axis\":\"Y\",\"amount\":5}] }" http://localhost:5000/job
```

##### Alternative method
Alternatively, a `.py` file can be used to test the '/job' endpoint using the Python requests library. I have included a program called 'API_Test.py" should you wish to use this approach. It is also provided below:

```
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
````

Make sure to replace `http://localhost:5000/job` with the appropriate URL for your Flask app. You would typically run the requests code after running your Flask script so that the Flask app is running and ready to handle incoming requests. Firstly, start your Flask app by running your Python script that contains the Flask app code (`QuantumAPI_Part1.py`). Once the app is running, you can run the requests code (`API_Test.py`) in a separate Python script or in a Jupyter notebook to send requests to the running Flask app and test its functionality.

As with the HTTP clients, this test sends a POST request to the `/job` endpoint with the JSON data containing a valid circuit. The response should contain a status code of 200 (assuming the request was successful) and a JSON object containing the job status, `job_ID`, and result. You can modify the circuit list to test different input values (for example, the test cases provided in the `Part1_Tests.py` file) and verify that the application is working correctly. 

##### Results
All the planned tests were carried out, by using the `curl` HTTP client, and copying the test cases from the `Part1_Tests.txt`. All the outputs matched the expected responses. The screenshots of the testing in the terminal are shown below:

![Screenshot (547)](https://user-images.githubusercontent.com/102755189/235460057-8b8d3929-b604-45c9-be42-dcd0e47cf39b.png)
![Screenshot (548)](https://user-images.githubusercontent.com/102755189/235460074-2531d104-aaeb-466e-9948-adb72f26b588.png)
![Screenshot (551)](https://user-images.githubusercontent.com/102755189/235460083-7921aaa8-b478-4075-b407-6381c8970ba1.png)

Therefore, the code behaves as expected and no refactoring is necessary.
#### Improvements

Although some input validation has been integrated into the solution, there could be further constraints to improve on this; for example, it could be determined whether the circuit is physically valid (i.e. able to be executed on a real quantum computer) or perhaps whether the gates are applied in a suitable order but this requires further context in the problem definition. Furthermore, no authorisation or authentication mechanisms have been included in the code (i.e. anyone can send a request to the `/job` endpoint). To improve this, authorization could be added to ensure that only authroized users can access the API, which would be particularly important in a production environment.

--------------------

### Part 2
#### Defining the problem
To introduce a form of **persistence** for results (so that the jobs can be stored or retrieved for longer than a single program execution), the job information will be stored within an in-memory data structure, such as a **dictionary**. This is a temporary step, as storing the circuit information for each `job_id` in a  dictionary will not scale well for a large number of jobs; hence, in the following part, this will be converted into a SQL database, which is a far more scalable data store.  

Secondly, there will need to be a GET endpoint which, when given a job_id, returns a response in the following format: 
```
GET /job/<job_id>
200 Response :
{
‘status’ : ‘completed’,
‘job_id’ : str
‘Circuit’ : [gate],
‘result’ : {
‘0’ : 203,
‘1’ : 797
}
}
```
Note that this includes the circuit information. Therefore, the circuit information and result will need to be stored for each job, and this is why the dictionary is the most appropriate data structure for the solution. Each element of the dictionary will refer to a given `job_id` and the keys will be `circuit` and `result`.
#### Required Tests
As in Part 1, I have converted these software requirements to test cases prior to implementation. As I am now developing the GET endpoint, my test cases will consist of both valid and invalid GET requests to the /job/<job_id> endpoint using a job ID that is generated in a previous valid POST request. This should return a custom error message for an invalid GET request or a response body consisting of the status, `job_id`, circuit information, and the hardcoded result, for a valid GET request. 

The test cases for this updated program and their expected responses are provided in the `Part2_Tests.txt` file. As before, the instructions for explicitly testing the code on your local machine by inputting these test circuits are included in the 'Testing' section below; this section is, again, reserved for defining the tests prior to implementation. The general cases of inputs have been listed below:

1. Valid GET request with a **valid `job_id`:** Send a GET request with a valid `job_id` returned from a previous POST request. Expected response: a 200 response with the circuit, job_id, and result.
2. Invalid GET request with an **invalid `job_id`:** Send a GET request with an invalid `job_id`. Expected response: a 404 response with a custom error message.

Note that these extend the test cases in `Part1_Tests.txt`. I will indeed test the POST endpoint, with the test cases from Part 1 again, to ensure the previous functionality has not been affected by the refactored code, and will output the `jobs` object throughout the processing to ensure it behaves as expected and contains the correct information. Finally, the explicit test cases in `Part2_Tests.txt` will be used in the 'Testing' section to determine the success and robustness of the solution.

#### Implementation
To add persistence to the API, a dictionary named `jobs` has been defined to store the circuit information for each `job_id`. Now, when a valid POST request is received at the POST endpoint `/job`, the circuit is validated and then the circuit information is stored in the `jobs` dictionary with a new `job_id`. As in Part 1, a successful response with the `job_id` and a hard-coded result is returned and, if the request is invalid, a custom error response with an appropriate error code and reason is returned. Therefore, the `process_job()` function has remained the same as Part 1 with the addition of the following to store the circuit information after validation:  

```
jobs[job_id] = {'circuit': circuit, 'result': result}
```
Furthermore, a new route to handle the GET request is created. This GET endpoint /job/<job_id> returns the result of a job with the specified `job_id`. As shown below, if the `job_id` is not an integer, a 400 error and custom error message is returned. Next, if the `job_id` does not exist, a 404 error code will be returned with a custom error message. For a valid `job_id`, the required response body, which includes the relevant circuit and job information, is returned.

```
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

    # Return the circuit and result for the job
    response = {
        'status': 'completed',
        'job_id': job_id,
        'circuit': jobs[job_id]['circuit'],
        'result': jobs[job_id]['result']
    }
    return jsonify(response), 200
```

The order of the keys in a dictionary is not guaranteed to be preserved in Python. Therefore, the order in which the keys appear in the response may not be the same as the order in which they were added. This makes it slightly more difficult to compare outputs to expected responses, and appears less consistent; therefore, to ensure that the keys in the response dictionary are in a specific order when they are returned to the JSON response, I have used the `collections.OrderedDict` class. Here's an updated version of the get_job function that uses `OrderedDict`:

```
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
    # Convert the dictionary to a JSON string
    json_response = json.dumps(response)

    return json_response, 200
```

In this updated version, I have also sorted the keys in the result dictionary using the sorted function and a lambda function that converts the keys to integers. A new result dictionary is then created using a dictionary comprehension that iterates over the sorted keys and values. The updated result dictionary is then added to the response JSON. This ensures that the all of the response keys will always be in the desired order, regardless of the order in which they were added to the dictionary.
#### Testing
##### Setup
To test the GET endpoint, a GET request must be made to the `/job/<job_id>` endpoint. For a valid request, this `job_id` must already exist (i.e have been generated in a previous POST request). You can send a GET request to `http://localhost:5000/job/<job_id>` using a tool like `curl` or any HTTP client like `Postman` or `Insomnia`.
To send a GET request using curl, you can run the following command in a terminal or command prompt window:
```
curl http://localhost:5000/job/<job_id>
```
Replace `<job_id>` with the ID of the job that you want to retrieve. For example:
```
curl http://localhost:5000/job/0
```
This will send a GET request to the server running on your local machine at port 5000, requesting the job with ID 0. The server will then return a JSON response with the circuit and result for the specified job. For a valid `job_id`, you should see the following response (this result is for the case that the job with ID 0 is X(90)):
```
{ "status": "completed", "job_id": "0", "circuit": [ { "axis": "X", "amount": 90 } ], "result": { "0": 203, "1": 797 } }
```
##### Alternative method
Alternatively, a `.py` file can be used to test the GET endpoint using the Python requests library. I have included a program called 'API_Test2.py" should you wish to use this approach. It is also provided below:
```
import requests

# Send a POST request to create a job
response = requests.post('http://localhost:5000/job', json={'circuit': [{'axis': 'X', 'amount': 2}, {'axis': 'Y', 'amount': 3}]})
job_id = response.json()['job_id']

# Send a GET request to retrieve the result for the job
response = requests.get(f'http://localhost:5000/job/{job_id}')

# Print the response
print(response.json())
```
Note that you will need to run the Flask server locally on your machine for this example to work, using the app.run() function at the end of the code. As with the HTTP clients, this test sends a GET request to the `/job/<job_id>` endpoint. You can modify the circuit list to test whether the response from the GET endpoint matches the circuit as expected. For the GET request, you may use the test cases provided in the `Part2_Tests.py` file) and verify that the application is working correctly. 

##### Results
Before testing the GET endpoint, the POST endpoint was again tested, using test cases from `Part1_Tests.txt`, to ensure it was still functioning as expected after updating the code. Furthermore, to ensure the `jobs` object was implemented correctly, I outputted it at different points in the code and it did indeed behave as expected. The planned tests, as defined in `Part2_Tests.txt` were carried out, by using the `curl` HTTP client, and copying the test cases from the text file. All the outputs matched the expected responses. 

The screenshots of the testing in the terminal are shown below:

![Screenshot (554)](https://user-images.githubusercontent.com/102755189/235567520-64d21bb3-a62c-459d-a28e-f5a255709c61.png)

Once again, the code behaves as expected and no refactoring is necessary.

#### Improvements
As mentioned previously, storing the circuit information for each `job_id` in a  dictionary provides a satisfactory solution for a small number of jobs. However, this in-memory data structure has poor scalability. For a large number of jobs, it is better to use a more scalable data store, such as a database or message queue. This will be implemented in the following section, in which the dictionary will be replaced with a SQL database. 

--------------------
### Part 3
#### Defining the problem
The in-memory datastore will now be converted to a more scalable `postgres` database. `PostgreSQL` is a powerful open-source relational database management system that is often used in applications where data integrity, scalability, and flexibility are critical; thus, a 'postgres' database is an ideal datastore for this project. This will be achieved using the `SQLAlchemy` library (which provides a high-level abstraction layer that works with a wide range of databases, including `PostgreSQL`) for the object-relational mapping, and `alembic`(a lightweight database migration tool for `SQLAlchemy`) to handle migrations. As the endpoint request and responses should remain identical to those in Part 2, the majority of the code will remain unchanged.

#### Required tests
As only the data storage is being updated, the same tests as done in Parts 1 and 2 can again be used to test the POST and END endpoints to ensure the previous functionality has not been affected by the refactoring (i.e. after the implementation). The testing here will be mainly verifying that the database is indeed storing the correct data and behaving as we would expect. This can simply be done by making POST requests with the test cases from `Part1_Tests.txt` and verifying that a new row has indeed been created in the database with the expected circuit, `job_id` and result (which can be done by outputting values or using pgAdmin). Then a GET request can be made to access this data, and all responses should be the same as the previous sections. Note that, as this is persistent storage, the jobs will be stored in the database for more than a single program execution  (i.e. the data can be retrieved even after the application has terminated). 

I have decided to use pgAdmin (graphical user interface for PostgreSQL) to visualise the database in real-time to perform testing. In particular, I will check the database after terminating the application to check whether results do indeed remain stored between program runs, and then confirm this by using the GET request upon rerunning the program to retrieve this stored data. Furthermore, the invalid cases, from Parts 1 and 2, will also be tested; for example, a invalid GET request with a `job_id` that does not exist the database should return a custom error. 

#### Implementation
Although I have used `SQLAlchemy` before, I have not used `PostgreSQL` and so I had to initially refer to the documentation online. After consulting the documentation, I installed the required libraries (PostgreSQL, psycopg2, and Alembic) and began implementing the solution. 

The beginning of the updated code is shown below, and the full code is provided in the `QuantumAPI_Part3.py` file. As shown, I imported the necessary modules and packages to complete the task: Migrate is a Flask extension that simplifies database migrations, and SQLAlchemy is, of course, the ORM (object-relational mapping) library for Python that provides a way to interact with relational databases using Python objects. 

```
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
```

After the Flask application instance, `SQLALCHEMY_DATABASE_URI` and `SQLALCHEMY_TRACK_MODIFICATIONS` are used to configure the Flask application to use a PostgreSQL database. The `SQLALCHEMY_DATABASE_URI` setting specifies the connection string for your PostgreSQL database, which includes the username, password, host, port, and database name. The `SQLALCHEMY_TRACK_MODIFICATIONS` setting is used to suppress a warning message from SQLAlchemy about tracking modifications. Thus, it has been set to false. A SQLAlchemy database instance is then created using `SQLAlchemy(app)` and a Migrate instance is created using `Migrate(app, db)`.

`Job` is a database model class that extends the `db.Model` class provided by SQLAlchemy. It has three fields: `id` (an integer primary key), `circuit` (a JSON field to store the circuit data), and `result` (a JSON field to store the result data). Within the `process_job()` function, the following code has been added after the circuit validation and processing:

```
    # Create a new Job object and add it to the database
    job = Job(circuit=circuit, result=result)
    db.session.add(job)
    db.session.commit()
```
A new Job object is created using the circuit and result variables, and is added to the database using `db.session.add(job)` and `db.session.commit()`. The job ID is obtained from the id attribute of the job object.

Finally, I need to modify the `get_job` function to retrieve the circuit and result from the database; in this updated code, the `Job` object is retrieved from the database using `Job.query.filter_by(id=job_id).first()`, and the circuit and result are obtained from the circuit and result attributes of the job object. The response is then formatted as in the previous sections. 

There also needs to be a script for creating the database schema; so I have created a new file `models.py`, which is shown below, to define the `SQLAlchemy` models for the database tables. This script defines the Flask app, configures the database connection, creates the database object using SQLAlchemy, defines the `Job` model, and initializes the Alembic migration object. When the script is run, it creates the database schema by `calling db.create_all()`.

```
# models.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/QuantumAPIdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    circuit = db.Column(db.JSON)
    result = db.Column(db.JSON)

if __name__ == '__main__':
    db.create_all()
    print('Database schema created.')
    
```    
Before I can use the endpoints for testing, I need to create the database and tables; this can be done by running migration commands or using pgAdmin. I used pgAdmin to create a database `QuantumAPIdb`, and then used the select Query Tool window to enter the following SQL command to create the `Job` table:
```
CREATE TABLE job (
  id SERIAL PRIMARY KEY,
  circuit JSON NOT NULL,
  result JSON NOT NULL
);
```
#### Testing
##### Setup
Firstly, you need to set up the database. The application is configured to use a PostgreSQL database. Ensure that PostgreSQL is installed on the machine and create a database named `QuantumAPIdb` with the following command:

```
createdb QuantumAPIdb
```

Next, run database migrations by navigating to the cloned repository and run the following command to apply database migrations:

```
flask db upgrade
```

Now you can run the application. Start the Flask application by running the following command:

```
python QuantumAPI_Part3.py
```

To test the application, use a HTTP client tool like `curl` to make requests to the endpoints. Recall that the API has two endpoints to test:

* `POST /job`: Submit a quantum circuit to be processed
* `GET /job/<job_id>`: Retrieve the result of a previously submitted job


To test the `/job` endpoint, you can send a `POST` request with a JSON payload containing a valid circuit, like this:

```
curl -X POST -H "Content-Type: application/json" -d '{"circuit": [{"axis": "X", "amount": 1}, {"axis": "Y", "amount": 2}]}' http://localhost:5000/job
```

This will create a new job with the given circuit and return a JSON response with the `job_id` and result. To test the `/job/<job_id>` endpoint, you can send a GET request with the `job_id` returned from the previous request, like this:

```
curl -X GET http://localhost:5000/job/1
```

This will retrieve the circuit and result for the job with the given ID and return a JSON response with the `job_id`, circuit, and result. You can also test error cases by sending invalid or missing parameters in the JSON payload or by requesting a `job_id` that does not exist in the database. To interact with the PostgreSQL server, you can use a graphical user interface like `pgAdmin` or a command-line tool like `psql`. You may need to configure the connection settings to connect to the server, such as the host, port, username, and password.

##### Results

As shown in the below image, I initially sent a valid POST request with a single gate circuit, and then a GET request with a `job_id` of 0. As expected, the data has been stored successfully and the correct information was retrieved. Next, I used a GET request for a `job_id` that does not exist in the database. As expected, this resulted in an error with the message "Job ID 1 not found". 

![Screenshot (559)](https://user-images.githubusercontent.com/102755189/235607432-6d6a94c0-66f3-4e5d-a000-db65c49c197d.png)

I used another valid POST request, with a double gate circuit, and then similarly used the GET endpoint to verify that it has indeed been added to the database correctly. After this, I included an invalid POST request with an empty circuit - the expected error was output (400 error "Invalid circuit format. The circuit must be a non-empty list"). I then added another two valid circuits, one with double gates and one with triple, and again confirmed that they had been stored correctly using the GET endpoint. In total, we expect 4 rows in the database for the 4 valid POST requests. The invalid requests should strictly not be shown on the table. As shown below, the database looks as expected:

![Screenshot (561)](https://user-images.githubusercontent.com/102755189/235607510-92888ef9-fb21-4f77-9c62-9c021f4c1258.png)

In addition, to demonstrate the persistence of the information stored in the database, I terminated the application and reran it. I was indeed able to use GET requests to retrieve the data for the previous job IDs. I did this for the first three job IDs. Next, I tested two invalid inputs, with an invalid circuit format and invalid gate format respectively, and both showed a custom error. Lastly, I added one more valid POST request with a single gate and used the GET request to ensure the job had been created. 

![Screenshot (558)](https://user-images.githubusercontent.com/102755189/235607450-4c10bb88-0a1c-4c5a-8690-9c72c34b6eb5.png)

As expected, the `Job` table in the database has just a single addition (corresponding to the single valid POST request), and no invalid requests are presented. The circuit information, `job_id` and result all match that of the POST request. Furthermore, I have also demonstrated the persistence of the results.

![Screenshot (562)](https://user-images.githubusercontent.com/102755189/235607529-21b98306-8d27-4a22-a5b0-095870bcd049.png)

In summary, the program has responded as expected to the set of inputted POST requests (both valid and invalid). 

--------------------

### Part 4 
#### Defining the problem
In this section, the provided circuit will be optimized such that any consecutive gates of the same axis will be combined. This is very useful as this could potentially reduce the number of gates needed. For example, if an X gate is followed by another X gate these can be combined into a single X gate (e.g. X(90) followed by X(20) is equivalent to X(110). 

If the circuit has been optimised, then this needs to be added to the response (and stored in the database which will be in Part 5). In particular, I need to modify the response object to include an optional field `optimized_circuit` if an optimization of the circuit was performed which will store this optimized circuit.

```
200 Response :
{
‘status’ : ‘completed’,
‘job_id’ : str
‘circuit’ : [gate],
‘optimized_circuit’: [gate]
‘result’ : {
‘0’ : 203,
‘1’ : 797
}
}
```
#### Required Tests
I have again converted these software requirements to test cases, prior to implementation, as required in TDD. The aim of testing for Part 4 is to ensure `optimize_circuit()`, which will be the function within which this optimisation logic will be implemented, is functioning as intended; test cases will, again, consist of both valid and invalid POST requests to the `/job` endpoint, which should return a custom error message for an invalid input or a suitable response body in the case of a valid input (which may or may not include an optimized circuit depending on the input) to confirm that the function optimize_circuit() is outputting the expected result. These test cases have been provided in the `Part4_Tests.txt` file - again, the actual test cases are included in the 'Part4_Tests.txt' file, 
but the general cases have been listed below:

1. Invalid request with **empty circuit**. Expected outcome: there should be no optimized circuit produced.
2. Invalid request with **general errors**. Expected outcome: there should be no optimized circuit produced.
3. Valid request with a **single gate**. Expected outcome: there should be no optimized circuit produced.
4. Valid request with **consecutive gates of the same axis**. Expected outcome: there should be an optimized circuit produced, with the same axis and an amount equal to the sum of the individual amounts. Non-consecutive gates or gates with different axis should not produce an optimized circuit. 
5. Valid request with **gates of different axes**. Expected outcome: there should be no optimized circuit produced, unless two or more consecutive gates have the same axis. If all of the gate axes are different in the circuit, then no optimized circuit should be produced.
6. Valid request with **negative amount gates**. Expected outcome: there may or may not be an optimized circuit produced, depending on the input. Even with negative amount gates, the optimisation should still sum the individual amounts.
7. Valid request with **zero amount gates**. Expected outcome: there may or may not be an optimized circuit produced, depending on the input. Even with zero amount gates, the optimisation should still sum the individual amounts (although this gate will essentially make no difference and is physically equivalent to doing nothing to the qubit).
8. Valid request with **gates of a single axis**. Expected outcome: if all of the gate axes are the same in the circuit, then an optimized circuit should always be produced, given that there is more than one gate in the circuit.

Again, these test cases do not claim to be exhaustive, but do provide a general framework for testing to determine whether the program satisfies the constraints defined in the problem. As shown in `Part4_Tests.txt`, each of these sections has a number of explicit cases to test; these tests will be used in the 'Testing' section to determine the success and robustness of the solution.
 
#### Implementation
To implement the solution, I have used `Part 2` as the base code, as an in-memory data structure `jobs` is currently sufficient to test the optimisation, as we do not wish to involve databases at this point (this will be done in Part 5). Firstly, I have added the following lines of code after the circuit validation in the `process_job()` function:

```
        # Optimize the circuit
        optimized_circuit = optimize_circuit(circuit)
        
        # Process the circuit and generate the result
        result = process_circuit(optimized_circuit)
            
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
    
```
Therefore, the optimized circuit is calculated using the optimize_circuit(circuit) function, which takes in the circuit as input, loop through the gates in the circuit and combines consecutive gates of the same axis. The resulting optimized circuit is then processed and returned as part of the response object. I firstly implemented the following `optimize_circuit` function:
 
 def optimize_circuit(circuit):
    # Combine adjacent gates of the same axis and reduce them to a single gate
    optimized_circuit = []
    prev_gate = None
    for gate in circuit:
        if prev_gate is not None and gate['axis'] == prev_gate['axis']:
            prev_gate['amount'] += gate['amount']
        else:
            if prev_gate is not None:
                optimized_circuit.append(prev_gate)
            prev_gate = gate.copy()
    optimized_circuit.append(prev_gate)
    return optimized_circuit
    
This does indeed give the correct result, but I wanted to implement a more efficient solution. This algorithm successfully combines adjacent gates of the same axis but it creates a copy of the previous gate using the copy() method. I, therefore, implemented another solution for `optimize_circuit`  which avoids this issue and is more memory efficient:

```
        def optimize_circuit(circuit):
            # Combine consecutive gates of the same axis
            optimized_circuit = []
            for gate in circuit:
                if len(optimized_circuit) > 0 and gate['axis'] == optimized_circuit[-1]['axis']:
                    optimized_circuit[-1]['amount'] += gate['amount']
                else:
                    optimized_circuit.append(gate)
            return optimized_circuit
```    
This `optimize_circuit`function uses a list to store the optimized circuit and checks the last gate in the list to see if it has the same axis as the current gate. If it does, it adds the amount of the current gate to the last gate in the list. If it doesn't, it adds the current gate to the list. Therefore, although both algorithms achieve the same result and have the same time complexity of O(n), where n is the number of gates in the circuit, this algorithm uses less memory than the first because it doesn't create a copy of the previous gate. To make this algorithm work properly, I have to add this line to `process_job` after the processing:

```
        # If the optimized circuit is identical to the original, then 'optimized_circuit' will not need to be sent in the response body
        if optimized_circuit == circuit:
            optimized_circuit = None
```
Lastly, the GET endpoint will also need to be updated to include `optimized_circuit` in its response body, if an optimization has actually been done. This can be implemented as shown below, where if there is indeed an `optimized_circuit` produced for the given `job`, then this will be included in the response body. Otherwise, the response body will be identical to the regular case from before.

```
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
```
#### Testing
##### Setup
No additional setup should be required to run and test `QuantumAPI_Part4.py`. Just like the previous section, you can use a HTTP client tool like `curl` to make requests to the endpoints. To send a `POST` request, using `curl`, for example, with a valid circuit:

```
curl -X POST -H "Content-Type: application/json" -d '{"circuit": [{"axis": "X", "amount": 1}, {"axis": "Y", "amount": 2}]}' http://localhost:5000/job
```
This will create a new job with the given circuit and return a JSON response with the `job_id` and result. You can then send a GET request with the `job_id` to retrieve the corresponding circuit and result information, using the following code:

```
curl -X GET http://localhost:5000/job/1
```
Note there will also be an additional `optimized_circuit` key in the response body if an optimisation has been made to the inputted circuit. In this case, no optimisation has been made as there are no consecutive gates in the circuit, so this key will not be outputted in the response body. You should see the following output:
```
{ "status": "completed", "job_id": "0", "circuit": [{"axis": "X", "amount": 1}, {"axis": "Y", "amount": 2}], "result": { "0": 203, "1": 797 } }
```
##### Results
The planned tests, as defined in `Part4_Tests.txt` were carried out one by one, by using the `curl` HTTP client, and copying the test cases from the text file. The screenshots of the testing in the terminal are shown below:

![Screenshot (563)](https://user-images.githubusercontent.com/102755189/235742708-ac92066c-e84c-488b-8bca-b1f7dc209c9d.png)
![Screenshot (564)](https://user-images.githubusercontent.com/102755189/235742717-f5169cda-22a6-4d60-b7dd-06528017cfc8.png)
![Screenshot (565)](https://user-images.githubusercontent.com/102755189/235742713-ce4f1849-31b3-4bdf-a853-ee63c9dbc563.png)

All the outputs matched the expected responses. Once again, the code behaves as expected and no refactoring is necessary.

#### Improvements
As I've reverted to an in-memory data structure, this solution is again not scalable and a database should be used instead for persistent storage. This will be implemented in the following section. Furthermore, although most of the functionality is now implemented, the `result` for the measurement outcomes of the qubit is still hardcoded, and a circuit processing algorithm should be implemented instead. This should take in the `circuit` and output the measurement outcomes for the qubit by operating the gates individually on the qubit. This has also been implemented in the next section.

--------------------
### Part 5
#### Defining the problem
To naturally extend upon Part 4, the optimised circuit should be persisted in the database. A new migration to the database which adds an `optimized_circuit` column to the `Job` table must be performed. Thus, the entire functionality of the previous functions has been combined in this final step.
#### Required Tests
The cases that this program will need to deal with will be identical to that of Part 4, but with some additional database testing and viewing to ensure it behaves as expected. Therefore, I will be testing using the `Part4_Test.txt` explicit cases, and use `pgAdmin` to verify that the correct data is being stored in the `Job` table. The `optimized_circuit` column of the table, which will be implemented in this section, should have values which match that of the `optimized_circuit` expected output, for the corresponding input, as given in the `Part4_Tests.txt` file.
#### Implementation
To perform the migration that adds the `optimized_circuit` column to the `Job` model, I ran the following command in terminal:
```
flask db migrate -m "Add optimized_circuit column to job table"
```
This generates a new migration script in the migrations/versions directory. Next, I opened this new file and verified that the up method contains the following code (if this is not present on your file, add it to the up method):
```
def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('optimized_circuit', sa.JSON(), nullable=False))
    # ### end Alembic commands ###
```
The `up` method in the migration script is responsible for upgrading the database schema to a new version. In this case, the upgrade involves adding a new column `optimized_circuit` to the job table in the database. By checking the up method in the migration script, I ensured that the migration script contained the necessary command to add this column to the `Job` table in the database. I then saved the file, and then run the migration using the following command:

```
flask db upgrade
```
This will apply the migration to the `QuantumAPIdb` database and add the `optimized_circuit` column to the `Job` table. Now that the column has been added and the migration is complete, I can commence with the testing. Also note that the base code for Part 5 was the code from Part 3, as this already created the database and implemented the required functionality; in this section, I am using migration commands to add a new column to this existing table. The only other update I have included in the code is adding some functionality to `process_circuit`, so that is not hardcoded, as this is the final stage and ideally some circuit processing logic should be implemented. 

```
def process_circuit(circuit):
    # Initialize a single qubit in the |0⟩ state
    qubit_state = np.array([1, 0])
    
    # Apply each gate in the circuit to the qubit
    for gate in circuit:
        # Construct the corresponding unitary matrix for the gate
        if gate['axis'] == 'X':
            gate_matrix = np.array([[np.cos(gate['amount']/2), -1j*np.sin(gate['amount']/2)],
                                    [-1j*np.sin(gate['amount']/2), np.cos(gate['amount']/2)]])
        elif gate['axis'] == 'Y':
            gate_matrix = np.array([[np.cos(gate['amount']/2), -np.sin(gate['amount']/2)],
                                    [np.sin(gate['amount']/2), np.cos(gate['amount']/2)]])
        elif gate['axis'] == 'Z':
            gate_matrix = np.array([[np.exp(-1j*gate['amount']/2), 0],
                                    [0, np.exp(1j*gate['amount']/2)]])
        else:
            raise ValueError("Invalid gate axis: {}".format(gate['axis']))
        
        # Apply the gate to the qubit
        qubit_state = np.dot(gate_matrix, qubit_state)
    
    # Measure the qubit in the computational basis
    probabilities = np.abs(qubit_state)**2
    result = {'0': int(probabilities[0]*1000), '1': int(probabilities[1]*1000)}
    return result
```
In `process_circuit()`, the rotation matrices for the X, Y, and Z axes are constructed using the angle of rotation specified in the gate object. The matrices are then multiplied together to obtain the final unitary matrix that represents the entire circuit. The resulting state of the qubit is then measured in the computational basis to obtain the measurement outcome, which is returned as a dictionary containing the probabilities of measuring the qubit in the |0⟩ and |1⟩ states (multiplied by 1000 for convenience). 
#### Testing
##### Setup
To test this application, you need to either use migration commands, as I have demonstrated above, or equally you can use the graphical tool `pgAdmin` to add the `optimized_circuit` column to the `Job` table in your `PostgreSQL` database. To do this, follow these steps:

1. Open `pgAdmin` and connect to your database.
2. In the Object Browser pane, expand the Schemas node and then expand the schema that contains the job table.
3. Right-click on the job table and select Properties from the context menu.
4. In the Properties dialog box, click on the Columns tab.
5. Click the `Add column` button to add a new column and, in the `Name` field, enter `optimized_circuit`.
7. In the Type field, select json.
8. Make sure the `Nullable` checkbox is unchecked.
9. Click the `Save` button to save the changes.

##### Results

The tests defined in `Part4_Tests.txt` were, once again, carried out one by one using the updated code `QuantumAPI_Part5.py`. Again, I used the `curl` HTTP client, and copied the test cases from the text file. The screenshots of the testing in the terminal are shown below, and screenshots of the database at intermediate points are also provided:
![Screenshot (567)](https://user-images.githubusercontent.com/102755189/235755327-dbf85da1-9114-47a3-964d-73839fa2584e.png)
The database is currently composed of the following entries, which are in agreement with the expected results:
![Screenshot (572)](https://user-images.githubusercontent.com/102755189/235757417-dc4f0903-9838-467d-a19a-913323a9e8ba.png)

All of the outputs match the expected results; note that, due to the circuit processing in `process_circuit()`, the `result` key in the response body is not just the hardcoded result from before `{ ‘0’ : 203, ‘1’ : 797}`. It now does indeed correspond to the physical measurement outcomes for the qubit after the circuit is applied, as desired. 

![Screenshot (569)](https://user-images.githubusercontent.com/102755189/235755330-8800c752-984f-4852-990e-7f2c31b63748.png)

As expected, the database is indeed updating in real-time with these POST requests. It is displaying the correct information for all of the cases thus far:

![Screenshot (571)](https://user-images.githubusercontent.com/102755189/235757449-54be6bb0-6932-430b-ab4b-8d3d72c6c053.png)


![Screenshot (568)](https://user-images.githubusercontent.com/102755189/235755331-91ecc54f-d214-4dc8-a2b6-539bebd36e31.png)


![Screenshot (570)](https://user-images.githubusercontent.com/102755189/235757476-344639ad-5207-4711-9714-b9da2eb367db.png)

As shown in this final screenshot, the database has stored all of the valid circuits, their `job_id`, result and their `optimized_circuit`, but none of the circuits associated with the invalid requests. Furthermore, from the initial invalid requests, we can see that the error handling is working as expected and this functionality has not been affected by the updates in the code. In conclusion, once again, the code behaves as expected and no refactoring is necessary.

#### Improvements
Overall, the code does have most of the functionality required; there are, however, many ways to improve it further. Currently, the code connects to the database using a hardcoded username and password, which is not secure, so a configuration file should be used. Next, instead of manually validating the JSON request payload, I could use a schema validation library like `jsonschema`. This will make the code more readable and less error-prone. Lastly, the implementation of the circuit processing and `job_id` generation could be optimised further and made more efficient; in the case of `process_circuit`, more context regarding the physical implementation of the quantum computer may help make the code more accurate.
