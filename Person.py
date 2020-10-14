# Class for person with contact and covid contact log

class Person(object):
    def __init__(self, customerId, x, y):
        self.customerId = customerId
        self.x = x
        self.y = y
        self.contact_log = []
        self.covid_contact_log = []