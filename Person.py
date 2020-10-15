# Class for person with contact and covid contact log
from flask import Flask,jsonify # server
from flask import request
from Log import Log
# Preparation of Flask server (micro web framework)
app = Flask(__name__)
app.config["DEBUG"] = True
people = []

class Person(object):
    def __init__(self, deviceId, x, y):
        self.deviceId = deviceId
        self.x = x
        self.y = y
        self.contact_log = Log([])
        self.covid_contact_log = Log([])

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

# a=Person('a',10,10)
# c=Person('c',10,10)
# people.append(a)
# people.append(c)

# REST endpoint: GET test1
# just returns OK

@app.route('/contact', methods=['GET'])
def getContact():
    message = []
    for person in people :
        message.append({"name":person.deviceId,"contact": person.getContactLog(),"covid": person.getCovidLog()})
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
    # nlog = Log(normal_contact_list)
    # clog = Log(covid_contact_list)
    
    nlog = Log([])
    nlog.setContact(normal_contact_list)
    
    clog = Log([])
    clog.setContact(covid_contact_list)
    
    #define person
    person = Person(id,x,y)
    person.setContactLog(nlog)
    person.setCovidLog(clog)
    
    #add new person to the list of people
    people.append(person)

    return "new person added" + str(nlog)    

@app.route('/contact', methods=['PUT'])
def putContact():
    #extract data
    data = request.json
    id = data['id']
    x = data['x']
    y = data['y']
    normal_contact_list = data['normal']
    covid_contact_list = data['covid']

    #update contact of user with the id
    for person in people:
        if(person.getId() == id):
            person.x = x
            person.y = y
            person.contact_log.setContact(normal_contact_list)
            person.covid_contact_log.setContact(covid_contact_list)
    
    return "update person contact"
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)