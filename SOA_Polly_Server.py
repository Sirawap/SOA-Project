from flask import Flask, redirect, url_for, request, jsonify, make_response, Response
import requests

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


class BluetoothEvent:
    def __init__(self, event_id, sender, receiver, distance, time):
        self.event_id = event_id
        self.sender = sender
        self.receiver = receiver
        self.distance = distance
        self.time = time
        self.isCovid = False

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
        event = BluetoothEvent(event_id, request.json["sender"], request.json["receiver"],
                               request.json["distance"], request.json["time"])

        # Check Room
        get_room = requests.get("0.0.0.0:3000/room")
        # Temp Variable name
        if calculateDistance(request.json["sender"], get_room[event.sender], get_room[event.receiver]):
            event.is_covid()

        event_id += 1
        db.append(event)
        requests.post(event.toJson(), "0.0.0.0:3000/contact")

        return make_response("Post Successful", 200)
    else:
        result = []
        for x in db:
            result.append(x.toJson())
        print(result)
        return make_response(jsonify(result), 200)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
