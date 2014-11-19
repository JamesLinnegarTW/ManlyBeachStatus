import feedparser
from Adafruit_CharLCD import Adafruit_CharLCD

from time import sleep

lcd = Adafruit_CharLCD()
lcd.begin(16, 2)

def getData():
    data = feedparser.parse('http://www.environment.nsw.gov.au/beachapp/SydneyBulletin.xml')
    return data

def setTides(data):
    high_tide = data['channel']['bw_hightide'].replace(" metres at", "m ").strip(".")
    low_tide = data['channel']['bw_lowtide'].replace(" metres at", "m ").strip(".")
    return high_tide, low_tide

def printBeach():
    lcd.message('hello')

def clear():
    lcd.clear()

def tides(high_tide, low_tide):
    clear()
    lcd.setCursor(0,0)
    lcd.message("H: %s" % high_tide)
    lcd.setCursor(0,1)
    lcd.message("L: %s" % low_tide)
    
while 1:
    beach_data = getData()
    high_tide, low_tide = setTides(beach_data)
    clear()
    for beach in beach_data.entries:
       if(beach.title == "Little Manly Cove"):
           tides(high_tide, low_tide)
    sleep(5)


#while 1:
#    lcd.clear()
#    lcd.message('Hello world')
#    sleep(2)


