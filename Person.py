# Class for person with contact and covid contact log
from flask import Flask,jsonify # server
from flask import request
import Log
# Preparation of Flask server (micro web framework)
app = Flask(__name__)
app.config["DEBUG"] = True
people = []

class Person(object):
    def __init__(self, customerId, x, y):
        self.customerId = customerId
        self.x = x
        self.y = y
        self.contact_log = []
        self.covid_contact_log = []

    def getId(self):
        return self.customerId

    def getContactLog(self):
        return self.contact_log

    def getCovidLog(self):
        return self.covid_contact_log

    def setContactLog(self,Log):
        self.contact_log.append(Log)

    def setCovidLog(self,Log):
        self.covid_contact_log.append(Log)

a=Person('a',10,10)
b=Person('b',10,10)
c=Person('c',10,10)
people.append(a)
people.append(b)
people.append(c)

# REST endpoint: GET test1
# just returns OK

@app.route('/contact', methods=['GET'])
def getContact():
    message = []
    for person in people :
        message.append({"name":person.customerId,"contact":person.contact_log,"covid": person.covid_contact_log})
    message = jsonify(message)

    return message

@app.route('/contact', methods=['POST'])
def postContact():
    #extract data
    data = request.json
    id = data['id']
    x = data['x']
    y = data['y']
    normal_contact_list = data['normal']
    covid_contact_list = data['covid']
    
    #create normal and covid contact log
    nlog = Log(normal_contact_list)
    clog = Log(covid_contact_list)
    
    #define person
    person = Person(id,x,y)
    person.setContactLog(nlog)
    person.setCovidLog(clog)
    
    #add new person to the list of people
    people.append(person)

    return "new person added"

@app.route('/contact', methods=['PUT'])
def putContact():
    #extract data
    data = request.json
    id = data['id']
    normal_contact_list = data['normal']
    covid_contact_list = data['covid']

    #create normal and covid contact log
    nlog = Log(normal_contact_list)
    clog = Log(covid_contact_list)

    #update contact of user with the id
    for person in people:
        if(person.getId == id):
            person.contact_log.append(nlog)
            person.contact_log.append(clog)
    
    return "update person contact"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)