import appdaemon.plugins.hass.hassapi as hass
import appdaemon.appapi as appapi
from time import *
import datetime
import appdaemon.appapi as appapi

class ComeAndGo(hass.Hass):
    
    def initialize(self):
        self.debug = False
        if "debug" in self.args:
            self.debug = self.args["debug"]

        self.sensor = self.args["startHour"]
        self.listen_state(self.hasLeft, self.sensor, new="on")

    def hasLeft(self, entity, attribute, old, new, kwargs):
        

     def debugInfo(mesg):
          if(self.debug):
               self.notify(mesg)
