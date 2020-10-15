# Class for person with contact and covid contact log
from flask import Flask,jsonify # server
from flask import request
from Log import Log
# Preparation of Flask server (micro web framework)
app = Flask(__name__)
app.config["DEBUG"] = True
people = []

class Person(object):
    def __init__(self, deviceId):
        self.deviceId = deviceId
        # self.x = x
        # self.y = y
        self.contact_log = []
        self.covid_contact_log = []

    def getId(self):
        return self.deviceId

    def getContactLog(self):
        return self.contact_log.getContact()

    def getCovidLog(self):
        return self.covid_contact_log.getContact()

    def setContactLog(self,Log):
        self.contact_log = Log

    def setCovidLog(self,Log):
        self.covid_contact_log = Log

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

# REST endpoint: GET test1
# just returns OK

@app.route('/contact', methods=['GET'])
def getContact():
    message = []

    for person in people :
        contact = []
        covid = []
        for x in person.contact_log:
            contact.append(x.toJson())
        for y in person.covid_contact_log:
            covid.append(y.toJson())    
        message.append({"id":person.deviceId,"contact": contact,"covid": covid})
    message = jsonify(message)

    return message

@app.route('/contact', methods=['PUT'])
def postContact():
    #extract data
    data = request.json
    # id = data['id']
    # x = data['x']
    # y = data['y']

    sender = data['sender']
    receiver = data['receiver']
    is_covid = data['is_covid']
    time = data['time']

    for person in people:
        if(person.deviceId == sender):
            contact = Log(receiver ,time)
            person.contact_log.append(contact)
            app.logger.info(is_covid)
            if(is_covid):
                person.covid_contact_log.append(contact)
            
    
    #define person
    
    #add new person to the list of people
    people.append(person)

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
    app.run(host='0.0.0.0', port=3000)