import datetime

class Log(object):
    def __init__(self, contact):
        self.contact = contact
        self.time = datetime.datetime.utcnow().isoformat()
        