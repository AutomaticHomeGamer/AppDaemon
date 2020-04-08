import appdaemon.plugins.hass.hassapi as hass
import appdaemon.appapi as appapi
from time import *
import datetime
import appdaemon.appapi as appapi

class LightsOut(hass.Hass):
    
    def initialize(self):
        self.Motions = self.args["sensors"]
        self.Lights = self.args["lights"]
        self.startHour = self.args["startHour"]
        self.startMin = self.args["startMin"]
        self.endHour = self.args["endHour"]
        self.endMin = self.args["endMin"]
        for motion in self.Motions:
            self.listen_state(self.turnOffLight, motion, new="on")


    def turnOffLight(self, *args, **kwargs):
        self.startTime = datetime.datetime.now()
        self.endTime = datetime.datetime.now()
        self.startTime = self.startTime.replace(hour=self.startHour, minute=self.startMin, second=0, microsecond=0)
        self.endTime = self.endTime.replace(hour=self.endHour, minute=self.endMin, second=0, microsecond=0)
        self.log("Turning off the lights")
        if (self.startTime.time() < datetime.datetime.now().time() < self.endTime.time()):
            self.log(self.get_state(self.Lights[0]))
            self.log(self.Lights[0])
            for Light in self.Lights:
                if( self.get_state(Light) == "on"):
                    self.turn_off(Light)

    #def hasLeft(self, entity, attribute, old, new, kwargs):
        

