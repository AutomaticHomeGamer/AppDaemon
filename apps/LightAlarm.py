import appdaemon.plugins.hass.hassapi as hass
import appdaemon.appapi as appapi
from time import *
import datetime
import appdaemon.appapi as appapi

class AlarmLight(hass.Hass):
    
    def initialize(self):
        self.startHour = self.args["startHour"]
        self.startMin = self.args["startMin"]
        self.lights = self.args["lights"]
        self.duration = self.args["duration"]
        self.level = 255
        if "level" in self.args:
            self.level = self.args["level"]
        
        self.debug = False
        if "debug" in self.args:
            self.debug = self.args["debug"]

        runTime = datetime.time(int(self.startHour),int(self.startMin))
        self.run_once(self.turnOnLights, runTime)
        #self.listen_state(self.motion, self.sensor, new="on")

    def turnOnLights(self, lights, **kwargs):
        self.debugInfo(self.lights + " is now turning on over " + str(self.duration) + " seconds.");
        self.turn_on(self.lights, brightness=self.level, transition=self.duration)

    def debugInfo(self, mesg):
        if(self.debug):
            self.notify(mesg)
