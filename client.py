from person import Person
import requests
import random as rd
import math as m
import datetime as t
people_no = 20
people = list()
walk_dist = 15
for i in range(people_no):
    people.append(Person(rd.randrange(-200,200),rd.randrange(-200,200),i))


def checkroom(p):
    if p.x < 0 and p.y < 0:
        return "3"
    elif p.x > 0 and p.y > 0:
        return "1"
    elif p.x > 0 and p.y < 0:
        return "2"
    else:
        return "4"

def alarm_check(ppl):
    total = len(ppl)
    for i in range(total):
        for j in range(i+1,total):
            dist = m.sqrt(m.pow(ppl[i].x-ppl[j].x,2)+m.pow(ppl[i].y-ppl[j].y,2))
            if dist <= 30:
                bluetooth_data_load1 = {
                    'sender': str(ppl[i].id),
                    'receiver': str(ppl[j].id),
                    'distance' : dist + rd.uniform(-0.1,0.1),
                    'time' : str(t.datetime.now())

                }
                bluetooth_data_load2 = {
                    'sender': str(ppl[j].id),
                    'receiver': str(ppl[i].id),
                    'distance' : dist + rd.uniform(-0.1,0.1),
                    'time' : str(t.datetime.now())

                }

                room_data1 = {
                    'id': str(ppl[i].id),
                    'room': checkroom(ppl[i])
                }
                room_data2 = {
                    'id': str(ppl[j].id),
                    'room': checkroom(ppl[j])
                }

                requests.post(bluetooth_data_load1,'http://0.0.0.0:3000/event')
                requests.post(room_data1,'http://0.0.0.0:3000/room')
                requests.post(room_data2,'http://0.0.0.0:3000/room')

def pos_update(ppl):
    for p in ppl:
        p.x = p.x + rd.randrange(-walk_dist,walk_dist)
        p.y = p.y + rd.randrange(-walk_dist,walk_dist)

if __name__ == "__main__":
    for i in range(10):
        for p in people:
            print(f"x:{p.x} y:{p.y}")
        alarm_check(people)
        pos_update(people)
        
