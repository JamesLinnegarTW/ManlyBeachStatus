import feedparser
import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD

from time import sleep

lcd = Adafruit_CharLCD()
lcd.begin(16, 2)

def getData():
    data = feedparser.parse('http://www.environment.nsw.gov.au/beachapp/SydneyBulletin.xml')
    return data

def getTides(data):
    high_tide = data['channel']['bw_hightide'].replace(" metres at", "m ").strip(".")
    low_tide = data['channel']['bw_lowtide'].replace(" metres at", "m ").strip(".")
    return high_tide, low_tide


def getTemperatures(data):
    air_temperature =  data['channel']['bw_airtemp']
    sea_temperature =  data['channel']['bw_oceantemp']
    return air_temperature, sea_temperature


def clear():
    lcd.clear()

def tides(high_tide, low_tide):
    clear()
    lcd.setCursor(0,0)
    lcd.message("H: %s" % high_tide)
    lcd.setCursor(0,1)
    lcd.message("L: %s" % low_tide)

def temperature(air_temp, sea_temp):
    clear()
    lcd.setCursor(0,0)
    lcd.message("Air: %sc" % air_temp)
    lcd.setCursor(0,1)
    lcd.message("Sea: %sc" % sea_temp)

while 1:
    beach_data = getData()
    high_tide, low_tide = getTides(beach_data)
    air_temperature, sea_temperature = getTemperatures(beach_data);

    clear()
    for beach in beach_data.entries:
       if(beach.title == "Little Manly Cove"):
#           tides(high_tide, low_tide)
           temperature(air_temperature, sea_temperature)
    sleep(5)


#while 1:
#    lcd.clear()
#    lcd.message('Hello world')
#    sleep(2)


