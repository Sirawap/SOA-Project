import datetime

class Log(object):

    def __init__(self, contact, time):
        self.contact = contact
        self.time = time

    def  getContact(self):
        return self.contact
        
    def setContact(self,contact):
        self.contact.append(contact)

    def toJson(self):
        return {
            "contact" : self.contact,
            "time": self.time
        }
        