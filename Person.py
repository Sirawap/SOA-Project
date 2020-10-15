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

    def setContactLog(self,Log):
        self.contact_log.append(Log)

    def setCovidLog(self,Log):
        self.covid_contact_log.append(Log)

# REST endpoint: GET test1
# just returns OK

@app.route('/contact', methods=['GET'])
def getContact():
    Log = [['b',0],['c',0],['d',1]]
    # p = Person('a',100,100,{'b':0, 'c':0, 'd':1},{'b':1})
    return jsonify({
            'personId' : 'a', 
            'contact' : Log
        })

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
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)