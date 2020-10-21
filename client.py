from personMRQandA import Person
from flask import Flask,jsonify # server
from flask import request
import requests
import random as rd
import math as m
import datetime as t
import time
import json
import jsonpickle

people_no = 20
people = list()
walk_dist = 15
for i in range(people_no):
    people.append(Person(rd.randrange(-50, 50), rd.randrange(-50, 50), i))


def checkroom(p):
    if p.x < 0 and p.y < 0:
        return "Electrical Room"
    elif p.x > 0 and p.y > 0:
        return "Medbay"
    elif p.x > 0 and p.y < 0:
        return "Storage Room"
    else:
        return "Engine Room"


def alarm_check(ppl):
    total = len(ppl)
    for i in range(total):
        for j in range(i + 1, total):
            dist = m.sqrt(m.pow(ppl[i].x - ppl[j].x, 2) + m.pow(ppl[i].y - ppl[j].y, 2))
            if dist <= 30:
                bluetooth_data_load1 = {
                    "sender": str(ppl[i].id),
                    "sender_room": checkroom(ppl[i]),
                    "receiver": str(ppl[j].id),
                    "receiver_room": checkroom(ppl[j]),
                    "distance": str(dist + rd.uniform(-0.1, 0.1)),
                    "time": str(t.datetime.now())
                }

                bluetooth_data_load2 = {
                    'sender': str(ppl[j].id),
                    'sender_room': checkroom(ppl[j]),
                    'receiver': str(ppl[i].id),
                    'receiver_room': checkroom(ppl[i]),
                    'distance': dist + rd.uniform(-0.1, 0.1),
                    'time': str(t.datetime.now())
                }

                print(bluetooth_data_load1)
                data = jsonpickle.encode(bluetooth_data_load1)
                print(bluetooth_data_load2)
                data2 = jsonpickle.encode(bluetooth_data_load2)
                # print(bluetooth_data_load1)
                # print(type(bluetooth_data_load1))

                requests.post("http://localhost:8000/event", json = data)
                requests.post("http://localhost:8000/event", json = data2)


def pos_update(ppl):
    for p in ppl:
        p.x = p.x + rd.randrange(-walk_dist, walk_dist)
        p.y = p.y + rd.randrange(-walk_dist, walk_dist)


if __name__ == "__main__":
    for i in range(20):
        for p in people:
            print(f"id: {p.id} x:{p.x} y:{p.y}")
        alarm_check(people)
        pos_update(people)
        time.sleep(1)

