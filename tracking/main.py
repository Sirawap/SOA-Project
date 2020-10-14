from fastapi import FastAPI, Body
import uvicorn
from pydantic import BaseModel

# Global var
event_id = 0


# Class
class BluetoothEvent:
    def __init__(self, uid, sender, receiver, distance, time):
        self.id = uid
        self.sender = sender
        self.receiver = receiver
        self.distance = distance
        self.time = time



# Model
class BluetoothObject(BaseModel):
    sender: str
    receiver: str
    distance: float
    time: str


app = FastAPI()
db = []

''' FastAPI Examples
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}
'''


@app.get("/locations")
async def get_locations():
    pass


@app.get("/location/{item_id}")
async def get_location(item_id):
    return db[item_id]


@app.post("/location")
async def post_location(req_body: BluetoothObject = Body(...)):
    global event_id
    event = BluetoothEvent(event_id, req_body.sender, req_body.receiver, req_body.distance, req_body.time)
    db.append(event)
    event_id += 1
    return {"message": f"{req_body.sender} {req_body.receiver} added to the Event DB", }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)