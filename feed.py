import feedparser
from time import sleep

i = 0;
displays = []
screen_index = 0

class Display():

	def __init__(self):
		self.index = 0

	def draw(self, title, detail):

		print chr(27) + "[2J"
		self.render_title(title)
		animating_data = self.render_detail(detail)
		return animating_data

	def render_title(self, title):
		print title  + ":" + (" " * (15 - len(title)))

	def render_detail(self, detail):
		if(len(detail)<=16):
			print detail + (" " * (16 - len(detail)))
			return {'animating':False,'next_screen':True}
		else:
			if(self.index > (len(detail)+16)):
				self.index = 0
				print ""
				return {'animating':True,'next_screen':True}

			else:
				text_buffer = (" " * 16) + detail + (" " * 16)
				print text_buffer[self.index:self.index+16]
				self.index = self.index + 1
				return {'animating':True,'next_screen':False}


def formatMetres(data):
	return data.replace(" metres" , "m").replace(" metre" , "m")

def clear_screens():
	global displays
	displays = []

def addScreen(title, text):
	global displays
	data_dict = {'title': title, 'text': text}
	displays.append(data_dict)

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
	print displays
	print screen_index
	sleep(2)
	display = Display()


	while (1):

		screen_data = displays[screen_index]
		animating_data = display.draw(screen_data['title'], screen_data['text'])

		if(animating_data['animating']):
			sleep(0.1)
			if(animating_data['next_screen']):
				screen_index = screen_index + 1
		else:
				sleep(2)
				screen_index = screen_index + 1

		if(screen_index >= len(displays)):
			screen_index = 0



except KeyboardInterrupt:
	print "exiting"

finally:
	print "Bye"



