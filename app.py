import time
import flask # server
import jsonpickle

from .Person import Person
from flask import request, jsonify
#import requests # client

# Preparation of Flask server (micro web framework)
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# REST endpoint: GET test1
# just returns OK
@app.route('/contac', methods=['GET'])
def test1():
    # time.sleep(5) # This is for exercise of timeouts
    return 'Test1 OK' # no response object, because this is just a test -> response is auto created

# REST endpoint: GET test2
# call test1 and just returns response from test1 and test2
@app.route('/test2', methods=['GET'])
def test2():
    response = request.get('http://localhost:54321/test1', timeout=1) # call EP test1
    print(response.content)
    if response.ok:
        # response content is binary, str() does not: we need to decode that, make sure the content is really UTF-8
        return response.content.decode('utf-8') + ' and Test2 OK'
    else:
        return 'Test2 Error' # Also a HTTP 200 !


# Map (dictionary) for Persons (PersonId -> key, Person -> value)
people = dict()

# Config
sleep_duration = 6

# REST endpoint: GET all Persons
# returns all Persons as a JSON list
@app.route('/person', methods=['GET'])
def getAllPersons():
    jsonString = jsonpickle.encode(list(people.values()))
    response = app.response_class(
        response=jsonString,
        mimetype='application/json'
    )
    app.logger.info('Get         : %i people', len(people))
    return response

# REST endpoint: PATCH Person (upsert)
# inserts or updates a person
@app.route('/person', methods=['PATCH'])
def upsertPerson():
    jsonString = jsonpickle.encode(list(people.values()))
    response = app.response_class(
        response=jsonString,
        mimetype='application/json'
    )

    global people
    if sleep_duration > 0: time.sleep(sleep_duration)
    person = jsonpickle.decode(request.json)
    people[person.deviceId] = person
    app.logger.info('Upsert         : %i people', len(people))
    return response


@app.route('/person', methods=['DELETE'])
def deletePerson():
    global people
    people = dict()
    return "OK"


# Main
# Start the web server and Flask
# use port 54321
if __name__ == "__main__":
    person = Person(1,"Tommy")
    people[person.deviceId] = person
    app.run(host='0.0.0.0', port=54321)


