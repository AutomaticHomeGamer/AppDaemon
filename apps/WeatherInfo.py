import appdaemon.plugins.hass.hassapi as hass
import appdaemon.appapi as appapi
from time import *
import datetime
import appdaemon.appapi as appapi

class Report(hass.Hass):
    
    def initialize(self):
        runtime = datetime.time(6, 0, 0) #Run everyday at 6am 
        #self.run_in(self.dailyWeatherStatement, 5)
        self.run_daily(self.dailyWeatherStatement, runtime)
        
        afternoon = datetime.time(16, 0, 0) #Run everyday at 4pm
        self.run_daily(self.twoHourWeatherStatement, afternoon)

       
    def dailyWeatherStatement(self, *args, **kwargs):
        self.dailyPrecip = self.get_state("sensor.dark_sky_precip_0d")
        self.dailyHighTemp = self.get_state("sensor.dark_sky_daily_high_temperature_0d")
        self.dailyLowTemp = self.get_state("sensor.dark_sky_daily_low_temperature_0d")
        self.dailyHumidity = self.get_state("sensor.dark_sky_humidity_0d")
        self.dailyCloud = self.get_state("sensor.dark_sky_cloud_coverage_0d")
        self.dailySummary = self.get_state("sensor.dark_sky_summary_0d")
        self.dailyWindBearing = "Wind out of the " + self.prettyBearing(self.get_state("sensor.dark_sky_wind_bearing_0d")) + "."


        self.weatherStatement = "Today calls for {0} with a high of {1} and a low of {2}. \
                                The skies will be {3} and it will be {4}% humid. {5}".format(self.dailyPrecip, 
                                                                                self.dailyHighTemp, 
                                                                                self.dailyLowTemp, 
                                                                                self.dailyCloud, 
                                                                                self.dailyHumidity,
                                                                                self.dailyWindBearing)

        self.notify(self.weatherStatement)
        self.notify(self.dailySummary)
        return self.weatherStatement

    def twoHourWeatherStatement(self, *args, **kwargs):
        self.currTemp = self.get_state("sensor.dark_sky_temperature_0h")
        self.currPrecip = self.get_state("sensor.dark_sky_precip_0h")
        self.currPrecipIntensity = self.get_state("sensor.dark_sky_precip_intensity_0h")
        self.currStorm = self.get_state("sensor.dark_sky_nearest_storm_distance_0h")
        self.currWindBearing = self.prettyBearing(self.get_state("sensor.dark_sky_wind_bearing_0h"))
        self.currWindSpeed = self.get_state("sensor.dark_sky_wind_speed_0h")
        self.currClouds = self.get_state("sensor.dark_sky_cloud_coverage_0h")

        self.nextTemp = self.get_state("sensor.dark_sky_temperature_1h")
        self.nextPrecip = self.get_state("sensor.dark_sky_precip_1h")
        self.nextPrecipIntensity = self.get_state("sensor.dark_sky_precip_intensity_1h")
        self.nextStorm = self.get_state("sensor.dark_sky_nearest_storm_distance_1h")
        self.nextWindBearing = self.prettyBearing(self.get_state("sensor.dark_sky_wind_bearing_1h"))
        self.nextWindSpeed = self.get_state("sensor.dark_sky_wind_speed_1h")
        self.nextClouds = self.get_state("sensor.dark_sky_cloud_coverage_1h")

        self.stormText = ""
        if (self.currStorm is None):
            self.currStorm = 0
        if (self.nextStorm is None):
            self.nextStorm = 0

        if( float(self.currStorm) > float(self.nextStorm)):
            self.stormText = "Storms headed your way."

        self.biggestWind = None
        self.biggestWindDirection = None
        if(self.currWindSpeed > self.nextWindSpeed):
            self.biggestWind = self.currWindSpeed
            self.biggestWindDirection = self.currWindBearing
        else: 
            self.biggestWind = self.nextWindSpeed
            self.biggestWindDirection = self.nextWindBearing
        self.windText = self.prettyWindSpeed(self.biggestWind, self.biggestWindDirection )


        self.precipText = ""
        if(self.currPrecip != "unknown"):
            self.precipText = "Currently " + self.prettyPrecipText(self.currPrecip, self.currPrecipIntensity)
        if(self.nextPrecip != "unknown"):
            self.nextPrecipText = "In the next hour " + self.prettyPrecipText(self.nextPrecip, self.nextPrecipIntensity)
            if(len(self.precipText) > 0):
                self.precipText += self.nextPrecipText
            else:
                self.precipText = self.nextPrecipText
        if(len(self.precipText) == 0):
            self.precipText = "Clear weather"

        self.tempText = ""
        if(self.currTemp > self.nextTemp):
            self.tempText = "Temperature is {0} dropping to {1}".format(self.currTemp, self.nextTemp)
        elif(self.nextTemp > self.currTemp):
            self.tempText = "Temperature is {0} rising to {1}".format(self.currTemp, self.nextTemp)
        elif(self.currTemp == self.nextTemp):
            self.tempText = "Temperature holding steady at {0}".format(self.currTemp)

        self.AfternoonText = "{0} {1} {2} {3}".format( self.tempText,
                                                  self.stormText,
                                                  self.windText,
                                                  self.precipText)
        self.notify(self.AfternoonText)
        return self.AfternoonText


    def prettyPrecipText(self, val, amount):
        self.prettyString = "expecting {0} inches of {1}."
        return self.prettyString.format(amount, val)


    def prettyWindSpeed(self, speed, direction):
        speed = float(speed)
        self.prettyString = "No wind."

        if( 0 < speed < 5):
            self.prettyString = "Low winds of {0}mph out of the {1}.".format(speed, direction)
        elif(5 < speed < 10):
            self.prettyString = "Medium wind of {0}mph out of the {1}.".format(speed, direction)
        elif(10 < speed < 15):
            self.prettyString = "Strong wind of {0}mph out of the {1}.".format(speed, direction)
        elif(15 < speed):
            self.prettyString = "Very high wind of {0}mph out of the {1}.".format(speed, direction)

        return self.prettyString

    def prettyBearing(self, bearing):
        self.prettyString = ""
        bearing = int(bearing) 
        if(0 < bearing < 22.5):
            self.prettyString = "North"
        elif ( 22.5 < bearing < 67.5):
            self.prettyString = "North East"
        elif(67.5 < bearing < 112.5):
            self.prettyString = "East"
        elif(112.5 < bearing < 157.5):
            self.prettyString = "South East"
        elif(157.5 < bearing < 202.5):
            self.prettyString = "South"
        elif(202.5 < bearing < 247.5):
            self.prettyString = "South West"
        elif(247.5 < bearing < 292.5):
            self.prettyString = "West"
        elif(292.5 < bearing < 337.5):
            self.prettyString = "North West"
        elif(337.5 < bearing < 360):
            self.prettyString = "North"

        return self.prettyString
