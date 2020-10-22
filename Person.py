# Class for person with contact and covid contact log
from flask import Flask,jsonify # server
from flask import request
import jsonpickle
import requests
from Log import Log
# Preparation of Flask server (micro web framework)
app = Flask(__name__)
app.config["DEBUG"] = True
people = []

class Person(object):
    def __init__(self, id):
        self.id = id
        self.contact_log = []

    def getId(self):
        return self.deviceId

    def addLog(self,target,time,covidDis):
        newLog = Log(target,time,covidDis)
        self.contact_log.append(newLog)

    def getNewestContactid(self):
        index = len(self.contact_log) - 1
        return self.contact_log[index].getidContact()

    def getNewestTime(self):
        index = len(self.contact_log) - 1
        return self.contact_log[index].getTime()

    def getNewestCovidDis(self):
        index = len(self.contact_log) - 1
        return self.contact_log[index].getCovidDis()

a=Person('0')
b=Person("1")
c=Person('2')
d=Person("3")
e=Person('4')
f=Person("5")
g=Person('6')
h=Person("7")
i=Person('8')
j=Person("9")
a2=Person('10')
b2=Person("11")
c2=Person('12')
d2=Person("13")
e2=Person('14')
f2=Person("15")
g2=Person('16')
h2=Person("17")
i2=Person('18')
j2=Person("19")
people.append(a)
people.append(b)
people.append(c)
people.append(d)
people.append(e)
people.append(f)
people.append(g)
people.append(h)
people.append(i)
people.append(j)
people.append(a2)
people.append(b2)
people.append(c2)
people.append(d2)
people.append(e2)
people.append(f2)
people.append(g2)
people.append(h2)
people.append(i2)
people.append(j2)
# REST endpoint: GET test1
# just returns OK

@app.route('/contact_log', methods=['GET'])
def getContact():
    message = []
    for person in people:
        for i in person.contact_log:
            message.append({"senderId": person.deviceId, "receiverId": i.getidContact(),"tiemstamp": i.getTime(), "covidDistance" : i.getCovidDis()})
    message = jsonify(message)
    return message

@app.route('/contact_log', methods=['PUT'])
def postContact():

    #extract data
    data = request.json
    data = jsonpickle.decode(data)

    sender = data['id']
    receiver = data['contactWith']
    is_covid = data['covidDistance']
    time = data['time']
    print(data)
    print("sender : "+sender+" || receiver : "+receiver)


    message = {
        "senderId": sender,
        "receiverId": receiver,
        "tiemstamp": time,
        "covidDistance": is_covid
    }
    #send to dewkul(Mr.Tech)
    message = jsonpickle.encode(message)
    requests.put("http://localhost:4000/covid", json=message)
    #requests.post("http://localhost:1234/covid", message)



    return "event updated"

# @app.route('/contact', methods=['PUT'])
# def putContact():
#     #extract data
#     data = request.json
#     id = data['id']
#     x = data['x']
#     y = data['y']
#     normal_contact_list = data['normal']
#     covid_contact_list = data['covid']

#     #update contact of user with the id
#     for person in people:
#         if(person.getId() == id):
#             person.x = x
#             person.y = y
#             person.contact_log.setContact(normal_contact_list)
#             person.covid_contact_log.setContact(covid_contact_list)
    
#     return "update person contact"
    
if __name__ == "__main__":
    app.run(port=3000)