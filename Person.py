# Class for person with contact and covid contact log
from flask import Flask,jsonify # server

# Preparation of Flask server (micro web framework)
app = Flask(__name__)
app.config["DEBUG"] = True

# REST endpoint: GET test1
# just returns OK
@app.route('/test', methods=['GET'])
def test():
    return "test"

@app.route('/contact', methods=['GET'])
def getContact():
    Log = [['b',0],['c',0],['d',1]]
    # p = Person('a',100,100,{'b':0, 'c':0, 'd':1},{'b':1})
    message = {
            'personId' : 'a', 
            'contact' : 'test'
        }
    res = jsonify(message)
    return jsonify({
            'personId' : 'a', 
            'contact' : Log
        })

class Person(object):
    def __init__(self, customerId, x, y):
        self.customerId = customerId
        self.x = x
        self.y = y
        self.contact_log = []
        self.covid_contact_log = []

    def getId():
        return self.customerId
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)