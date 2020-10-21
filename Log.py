import datetime

class Log(object):

    def __init__(self, idContact, time,boolean):
        self.idContact = idContact
        self.time = time
        self.covidDis = boolean

    def getidContact(self):
        return self.idContact

    def setContact(self,contact):
        self.idContact = contact

    def getTime(self):
        return self.time

    def getCovidDis(self):
        return self.covidDis
        