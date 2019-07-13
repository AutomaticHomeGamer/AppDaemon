import appdaemon.plugins.hass.hassapi as hass
import appdaemon.appapi as appapi
from time import *
import datetime
import appdaemon.appapi as appapi

class ContactOpen(hass.Hass):
    
    def initialize(self):
        self.currentTimer = None
        self.currentOpenContacts = {}
        self.contacts = self.args["contacts"]
        self.time = self.args["time"]
        for contact in self.contacts:
            self.listen_state(self.sendAlert, contact, new="on")
            self.listen_state(self.cancelAlert, contact, new="off")
            self.currentOpenContacts[contact] = None


    def sendAlert(self, entity, attribute, old, new, kwargs):
            self.currTimer = self.run_in(self.findOpenContacts, self.time, cont=entity)
            self.currentOpenContacts[entity] = self.currTimer

    def findOpenContacts(self, *args, **kwargs):
        self.report = "Contact is open: " + args[0]['cont']
        #self.report = 
        #for key, value in kwargs.items():
        #    self.report += key
        #self.answer = kwargs["cont"]
        #for contact in self.currentOpenContacts:
        #    self.answer += contact + "\n"
        #self.answer += " is open."
        self.currentOpenContacts[args[0]["cont"]] = self.run_in(self.findOpenContacts, self.time*2, cont=args[0]['cont'])
        self.notify(self.report)
        #self.notify(self.answer)
            

    def cancelAlert(self, entity, attribute, old, new, kwargs):
        if(self.currentOpenContacts[entity] != None):
            self.cancel_timer(self.currentOpenContacts[entity])

