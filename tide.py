import feedparser
import RPi.GPIO as GPIO
from CharLCD import CharLCD

from time import sleep


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
    lcd.message("Air temp: %sc" % air_temp)
    lcd.setCursor(0,1)
    lcd.message("Sea temp: %sc" % sea_temp)

try:
    lcd = Adafruit_CharLCD(25, 24, [23, 17, 27, 22], GPIO)
    lcd.begin(16, 2)

    while 1:
        beach_data = getData()
        high_tide, low_tide = getTides(beach_data)
        air_temperature, sea_temperature = getTemperatures(beach_data);

        clear()
        for beach in beach_data.entries:
           if(beach.title == "Little Manly Cove"):
               tides(high_tide, low_tide)
               sleep(5)
               temperature(air_temperature, sea_temperature)
               sleep(5)


except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+C
    clear()

finally:
    GPIO.cleanup()


