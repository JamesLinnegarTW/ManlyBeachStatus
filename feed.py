import feedparser
import RPi.GPIO as GPIO
import time
from CharLCD import CharLCD

GPIO.setmode(GPIO.BCM)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

i = 0;
displays = []
screen_index = 0
next_draw = time.time()
last_draw = time.time()
button_down = False

class Display():

  def __init__(self, GPIO):
    self.index = 0

    self.lcd = CharLCD(25, 24, [23, 17, 27, 22], GPIO)

    self.lcd.begin(16, 2)

  def clear(self):
    self.index = 0

  def draw(self, title, detail):

    print chr(27) + "[2J"
    self.render_title(title)
    animating_data = self.render_detail(detail)
    animating_data['last_draw'] = time.time()
    return animating_data

  def render_title(self, title):
    to_render = title  + ":" + (" " * (15 - len(title)))
    print to_render
    self.lcd.setCursor(0,0)
    self.lcd.message(to_render)

  def render_detail(self, detail):
    if(len(detail)<=16):
      to_render = detail + (" " * (16 - len(detail)))
      animating_data =  {'animating':False,'next_screen':True}
    else:
      if(self.index > (len(detail)+16)):
        self.index = 0
        to_render = ""
        animating_data = {'animating':True,'next_screen':True}

      else:
        text_buffer = (" " * 16) + detail + (" " * 16)
        to_render = text_buffer[self.index:self.index+16]
        self.index = self.index + 1
        animating_data =  {'animating':True,'next_screen':False}

    print to_render
    self.lcd.setCursor(0,1)
    self.lcd.message(to_render)
    return animating_data

def formatMetres(data):
  return data.replace(" metres" , "m").replace(" metre" , "m")

def clear_screens():
  global displays
  displays = []

def addScreen(title, text):
  global displays
  data_dict = {'title': title, 'text': text}
  displays.append(data_dict)

#def inc_button_pressed(channel):
#  global next_draw
#  global button_down
#  button_down = True
#  next_draw = time.time()
#  increment_screen_index()
#
#def dec_button_pressed(channel):
#
#  global next_draw
#  global button_down
#  button_down = True
#  next_draw = time.time()
#  decrement_screen_index()


def increment_screen_index():
  global display
  global screen_index

  display.clear()

  screen_index = screen_index + 1
  if(screen_index > len(displays)):
      screen_index = 0


def decrement_screen_index():
  global display
  global screen_index


  display.clear()

  if(screen_index > 0):
    screen_index = screen_index - 1
  else:
    screen_index = len(displays)-1



def get_data():
  print "getting data"
  data = feedparser.parse('http://www.environment.nsw.gov.au/beachapp/SydneyBulletin.xml')

  for beach_data in data.entries:
    if(beach_data.title == "Little Manly Cove"):

      addScreen("Beach", beach_data.title)
      addScreen("High tide", formatMetres(data['channel']['bw_hightide']))
      addScreen("Low tide" , formatMetres(data['channel']['bw_lowtide']))
      addScreen("Air temp" , data['channel']['bw_airtemp'] + 'C')
      addScreen("Ocean temp" , data['channel']['bw_oceantemp']+'C')
      addScreen("Swell", formatMetres(data['channel']['bw_swell']))
      addScreen("Rain", formatMetres(data['channel']['bw_rainfall']))
      addScreen("Weather", data['channel']['bw_weather'])
      addScreen("Winds", data['channel']['bw_winds'])
      addScreen("Advice", beach_data['bw_advice'])
      addScreen("Stars", beach_data['bw_starrating'])


try:

  get_data()

  display = Display(GPIO)

  #GPIO.add_event_detect(24, GPIO.FALLING, callback=inc_button_pressed, bouncetime=300)
  #GPIO.add_event_detect(23, GPIO.FALLING, callback=dec_button_pressed, bouncetime=300)


  while (1):
    if(time.time() >= next_draw):
      screen_data = displays[screen_index]
      animating_data = display.draw(screen_data['title'], screen_data['text'])

      if(animating_data['animating']):
        next_draw = time.time() + 0.2
        if(animating_data['next_screen']):
          increment_screen_index()
      else:
          next_draw = time.time() + 3
          increment_screen_index()



except KeyboardInterrupt:
  print "exiting"
  GPIO.cleanup()
finally:
  print "Bye"
  GPIO.cleanup()



