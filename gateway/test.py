import requests
import time
from datetime import datetime

from model.RawLog import RawLog

if __name__ == '__main__':
    # body = {
    #     "senderId": "A",
    #     "receiverId": "B",
    #     "timestamp": "2020-10-29T16:11:11",
    #     "covidDistance": True
    # }

    body = RawLog("A", "B", datetime.now(), True)
    response = requests.post('localhost:8000', data=body)
    print(response)
