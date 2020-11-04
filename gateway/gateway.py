
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Tuple
from flask import Flask, request, jsonify
import json
import jsonpickle
import os


# Convert datatype set -> list for json responding
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


# Response format for endpoint GET: /graph

response = {
    'normalEdges': set(),  # Set of pairs - tuple[str, str]
    'covidEdges': set(),   # Set of pairs - tuple[str, str]
    'nodes': set()         # Set of nodes - str
}


app = Flask(__name__)

contacts = dict()

load_dotenv()

# Set default data timeout (expire)
timeout = timedelta(seconds=float(os.getenv('DATA_TIMEOUT')))


def create_edge(sender, receiver) -> Tuple[str, str]:
    # Forcing entities to be in ascending order e.g. (A, B) NOT (B, A)
    return (sender, receiver) if sender < receiver else (receiver, sender)


def remove(edge):
    response['covidEdges'].discard(edge)
    response['normalEdges'].discard(edge)


@app.route("/", methods=["GET"])
def root():
    return {"message": "Hello World. This is a gateway :)"}


@app.route("/covid", methods=["POST"])
def add_data():
    req_data = request.get_json()
    req_data = jsonpickle.decode(req_data)

    # print(req_data, type(req_data))
    # print(req_data['senderId'])
    # print(req_data['receiverId'])
    # print(req_data['timestamp'])
    # print(req_data['covidDistance'], end='\n\n')

    req_sender_id = str(req_data['senderId']).upper()
    req_receiver_id = str(req_data['receiverId']).upper()
    req_timestamp = datetime.strptime(
        str(req_data['timestamp']), "%Y-%m-%d %H:%M:%S.%f")
    req_covid_distance = bool(req_data['covidDistance'])

    if req_sender_id == req_receiver_id:
        return "Duplicated IDs (╥_╥)", 400

    edge = create_edge(req_sender_id, req_receiver_id)


    # Add to discovered nodes
    response["nodes"].update([edge[0], edge[1]])

    key = f'{edge[0]}#{edge[1]}'

    # Check whether we have discovered this node or not
    if key in contacts:
        is_covid = contacts[key]['isCovid']

        #  Check if covid status is changed or not
        if is_covid is not req_covid_distance:
            remove(edge)
        else:
            # Update lastest time
            contacts[key]['timestamp'] = req_timestamp

    contacts[key] = {
        "isCovid": req_covid_distance,
        "timestamp": req_timestamp
    }

    if req_covid_distance:
        response['covidEdges'].add(edge)
    else:
        response['normalEdges'].add(edge)
    print(response)
    return 'ok'


@app.route("/graph", methods=['GET'])
def transform_graph():
    # global response
    print(response)

    now = datetime.now()

    to_be_removed = list()
    for key, contact in contacts.items():

        # Find outdated data
        if now - contact['timestamp'] > timeout:
            a, b = key.split('#')
            edge = create_edge(a, b)

            remove(edge)
            to_be_removed.append(key)

    for c in to_be_removed:
        del contacts[c]

    return json.dumps(response, cls=SetEncoder)


if __name__ == '__main__':
    app.run(debug=True, port=8000)  # run app in debug mode on port 5000
