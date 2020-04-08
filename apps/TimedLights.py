import appdaemon.plugins.hass.hassapi as hass
import appdaemon.appapi as appapi
from time import *
import datetime
import appdaemon.appapi as appapi

class TimedLight(hass.Hass):
    
    def initialize(self):
        self.isGoing = False;
        self.currentTimer = None;
        self.startHour = self.args["startHour"]
        self.startMin = self.args["startMin"]
        self.endHour = self.args["endHour"]
        self.endMin = self.args["endMin"]
        self.timeout = self.args["timeout"]
        self.sensor = self.args["sensor"]
        self.lights = self.args["lights"]
        if( "mode" in self.args.keys()):
            self.mode = self.args["mode"]
        else:
            self.mode = "None"
        self.level = 255
        if "level" in self.args:
            self.level = self.args["level"]
        self.debug = False
        if "debug" in self.args:
            self.debug = self.args["debug"]

        self.listen_state(self.motion, self.sensor, new="on")

    def motion(self, entity, attribute, old, new, kwargs):
        currTime = datetime.datetime.now()
        endTime = datetime.datetime.now()
        startTime = datetime.datetime.now()
        startTime = startTime.replace(hour=self.startHour, minute=self.startMin, second=0, microsecond=0)
        endTime = endTime.replace(hour=self.endHour, minute=self.endMin, second=0, microsecond=0)

        self.debugInfo ( "Start: " + startTime.strftime("%H:%M:%S") + " | Now: " + currTime.strftime("%H:%M:%S") + " | End; " + endTime.strftime("%H:%M:%S") );
       
        if (self.mode == self.get_state("sensor.home_mode") or self.mode == "None"):
            if(self.now_is_between( startTime.strftime("%H:%M:%S"), endTime.strftime("%H:%M:%S"))):
                 
                if "switch" in self.lights:
                    self.debugInfo("This is a switch");
                    self.turn_on(self.lights)
                else:
                    self.debugInfo("This is a group/light")
                    self.turn_on(self.lights, brightness=self.level)

                #self.turn_on(self.lights)
                if(self.isGoing == False):
                    self.debugInfo("Turning " + self.lights + " on for " + str(self.timeout) + " seconds")
                    self.currentTimer = self.run_in(self.light_off, self.timeout)
                    self.isGoing=True
                else:
                    #self.notify("Resetting timer")
                    self.debugInfo("Resetting timer")
                    self.cancel_timer(self.currentTimer)
                    self.currentTimer = self.run_in(self.light_off, self.timeout)

    def light_off(self, kwargs):
        self.turn_off(self.lights)
        self.isGoing = False

    def light_on(self, *args, **kwargs):
        self.eID = args[0]['entity_id']
        self.turn_on(self.eID)

    def debugInfo(self, mesg):
        if(self.debug):
            self.notify(mesg)
