from datetime import datetime

from pydantic import BaseModel


class RawLog(BaseModel):
    def __init__(self, send_id, receive_id, time, distance):
        self.senderId = send_id
        self.receiverId = receive_id
        self.timestamp = time
        self.covidDistance = distance

    senderId: str
    receiverId: str
    timestamp: datetime
    covidDistance: bool
