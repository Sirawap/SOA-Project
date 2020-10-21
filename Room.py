from flask import Flask, jsonify, request 
# Preparation of Flask server (micro web framework)
app = Flask(__name__)
app.config["DEBUG"] = True

class Room(object):
  def __init__(self):
    self.log = {}

  def setRoom(self,id,room):
    self.log[id] = room

  def getLog(self):
    return self.log

room = Room()

# REST endpoint: GET getroom
@app.route('/room', methods=['GET'])
def getRoom():
  return room.getLog()
  # return "GET"

# REST endpoint: POST postroom
@app.route('/room', methods=['POST'])
def postRoom():
  data = request.json
  id = data['id']
  _room = data['room']
  room.setRoom(id,_room)
  return "successful"


if __name__ == "__main__":
    app.run( port=3030)

  
