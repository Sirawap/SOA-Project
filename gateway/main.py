from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta
import uvicorn


class Data(BaseModel):
    senderId: str
    recieverId: str
    timestamp: datetime
    covidDistance: bool


response = {
    'normalEdges': set(),  # Set of tuple[str, str]
    'covidEdges': set(),  # Set of tuple[str, str]
    'nodes': set()        # Set of str
}


app = FastAPI()

contacts = dict()
timeout = timedelta(seconds=30)


def create_edge(sender, receiver):
    return (sender, receiver) if sender < receiver else (receiver, sender)


def remove(edge):
    # print(f'Remove: {edge}')
    response['covidEdges'].discard(edge)
    response['normalEdges'].discard(edge)


@app.get("/")
async def root():
    return {"message": "Hello World. This is a Gateway"}


@app.post("/covid")
async def add_data(req: Data):
    # edge = (req.senderId, req.recieverId) if req.senderId < req.recieverId else (
    #     req.recieverId, req.senderId)
    edge = create_edge(req.senderId.upper(), req.recieverId.upper())

    # Add to discovered node
    response["nodes"].update([edge[0], edge[1]])

    key = f'{edge[0]}#{edge[1]}'
    # print(key)
    if key in contacts:
        is_covid = contacts[key]['isCovid']

        #  Check if covidDis status is changed
        # try:
        #     if is_covid is not req.covidDistance:
        #         print(f'Remove: {edge}')
        #         response['covidEdges'].remove(
        #             edge) if is_covid else response['normalEdges'].remove(edge)
        # except KeyError as e:
        #     return f'Failed: Set.remove() => {e}'

        if is_covid is not req.covidDistance:
            remove(edge)
        else:
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


@app.get("/graph")
async def transform_graph():
    # print(f'Contacts:\n{contacts}')

    now = datetime.now()

    to_be_removed = list()
    for key, contact in contacts.items():
        # print(now - contact['timestamp'])
        if now - contact['timestamp'] > timeout:
            a, b = key.split('#')
            edge = create_edge(a, b)

            remove(edge)
            to_be_removed.append(key)

    for c in to_be_removed:
        del contacts[c]

    return response


@app.get("/graph/timeout")
async def get_timeout():
    return timeout


@app.get("/graph/timeout/set")
async def set_timeout(sec: float):
    global timeout
    timeout = timedelta(seconds=sec)
    return "OK"

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True)
