import datetime

class Log(object):

    def __init__(self, contact):
        self.contact = contact
        self.time = datetime.datetime.utcnow().isoformat()

    def  getContact(self):
        return self.contact
        
    def setContact(self,contact):
        self.contact.append(contact)
        