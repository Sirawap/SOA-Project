from flask import Flask, redirect, url_for, request, jsonify, make_response, Response
import requests
import jsonpickle
# Global
app = Flask(__name__)
db = []
event_id = 0


# Class


def calculateDistance(distance, senderRoom, receiverRoom):
    covidDistance = 5
    if senderRoom is not receiverRoom:
        return False
    if distance <= covidDistance:
        return True
    else:
        return False


class Event:
    def __init__(self, event_id, sender, receiver, distance, time):
        self.event_id = event_id
        self.sender = sender
        self.receiver = receiver
        self.distance = distance
        self.time = time
        self.isCovid = False
    def getId(self):
        return self.sender
    def getContactWith(self):
        return self.receiver
    def getTime(self):
        return self.time
    def getCovidDis(self):
        return self.isCovid

    def toJson(self):
        return {
            "id": self.sender,  # sender
            "contactWith": self.receiver,  # receiver
            "time": self.time,
            "covidDistance": self.is_covid,

        }

    def is_covid(self):
        self.isCovid = True


@app.route('/event', methods=['POST', 'GET'])
def event():
    if request.method == 'POST':
        global event_id

        # sender = request.args.get("sender")
        # receiver = request.args.get("receiver")
        # distance = request.args.get("distance")
        # time = request.args.get("time")
<<<<<<< HEAD

        data = request.json
        data = jsonpickle.decode(data)
        print(data)
        print(type(data))
        print(event_id)
        sender = data["sender"]
        receiver = data['receiver']
        distance = float(data['distance'])
        time = data['time']

        event = Event(event_id, sender, receiver,
                      distance, time)
        # event = Event(event_id, request.args.json['sender'], request.args.json['receiver'],
        #               request.args.json['distance'], request.args.json['time'])

=======
        event = Event(event_id, request.json["sender"], request.json["receiver"],
                      request.json["distance"], request.json["time"])
>>>>>>> 145b78bafa5e2587cb3e554d0ddaef1465be7548

        # Check Room
        sender_room =  data['sender_room']
        receiver_room = data['receiver_room']
        # Temp Variable name
        if calculateDistance(sender, sender_room, receiver_room):
            event.is_covid()

        event_id += 1
        db.append(event)
        newData = {
            "id": event.getId(),
            "contactWith": event.getContactWith(),
            "time": event.getTime(),
            "covidDistance": event.getCovidDis()
        }
        newData = jsonpickle.encode(newData)
        requests.put("http://localhost:3000/contact_log",json=newData)

        return make_response("Post Successful", 200)
    else:
        result = []
        for x in db:
            result.append(x.toJson())
        print(result)
        return make_response(jsonify(result), 200)


if __name__ == '__main__':
    app.run(debug=True, port=8000)