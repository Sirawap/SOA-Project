from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from dotenv import load_dotenv
from typing import Tuple
import uvicorn
import os


# Request body format for endpoint POST: /covid
class Data(BaseModel):
    senderId: str
    recieverId: str
    timestamp: datetime
    covidDistance: bool


# Response format form endpoint GET: /graph
response = {
    'normalEdges': set(),  # Set of pairs - tuple[str, str]
    'covidEdges': set(),   # Set of pairs - tuple[str, str]
    'nodes': set()         # Set of nodes - str
}


app = FastAPI()

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


@app.get("/")
async def root():
    return {"message": "Hello World. This is a gateway :)"}


# For recieving data from Mr.Time + Girb ()
@app.post("/covid")
async def add_data(req: Data):
    sender_id = req.senderId.upper()
    reciever_id = req.recieverId.upper()

    if sender_id == reciever_id:
        raise HTTPException(status_code=400, detail="Duplicated IDs (╥_╥)")

    edge = create_edge(sender_id, reciever_id)

    # Add to discovered nodes
    response["nodes"].update([edge[0], edge[1]])

    key = f'{edge[0]}#{edge[1]}'

    # Check whether we have discovered this node or not
    if key in contacts:
        is_covid = contacts[key]['isCovid']

        #  Check if covid status is changed or not
        if is_covid is not req.covidDistance:
            remove(edge)
        else:
            # Update lastest time
            contacts[key]['timestamp'] = req.timestamp

    contacts[key] = {
        "isCovid": req.covidDistance,
        "timestamp": req.timestamp
    }

    if req.covidDistance:
        response['covidEdges'].add(edge)
    else:
        response['normalEdges'].add(edge)

    return req


# For sending data to GUI
@app.get("/graph")
async def transform_graph():
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

    return response


# Return current timeout setting
@app.get("/graph/timeout")
async def get_timeout():
    return f"Data is valid for {timeout}"


# Update timeout settings
@app.get("/graph/timeout/set")
async def set_timeout(sec: float):
    global timeout
    timeout = timedelta(seconds=sec)
    return "OK"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True)
