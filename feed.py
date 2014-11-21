import feedparser
from time import sleep

text_length_to_display = 16

displays = []
display_index = 0;

def formatMetres(data):
	return data.replace(" metres" , "m").replace(" metre" , "m")

class Beach:
	def __init__(self, name, advice, high_tide, low_tide):
		self.name = name
		self.advice = advice
		self.high_tide = high_tide
		self.low_tide = low_tide

	def displayName(self):
		print "Name: %s" % self.name


def printStringToLines(text):

	words = text.split(" ");
	return_string = []
	temp_string = ""

	for word in words:
		if(len(temp_string + word) > 16):
			return_string.append(temp_string)
			temp_string = word + " "
		else:
			temp_string = temp_string + word + " "

	return_string.append(temp_string)

	return return_string;

def renderTextToLines(text):
	for data in printStringToLines(text):
		print data
	print "-" * 10

def addScreen(title, text):
	global displays
	data_dict = {'title': title, 'text': text}
	displays.append(data_dict)

data = feedparser.parse('http://www.environment.nsw.gov.au/beachapp/SydneyBulletin.xml')


for beach_data in data.entries:
	if(beach_data.title == "Little Manly Cove"):
		print ""
		addScreen("Beach", beach_data.title)
		addScreen("Advice", beach_data['bw_advice'])
		addScreen("Stars", beach_data['bw_starrating'])
		#display_text = renderText(display_text, beach_data['bw_bsgcomment'])


addScreen("High tide", formatMetres(data['channel']['bw_hightide']))
addScreen("Low tide" , formatMetres(data['channel']['bw_lowtide']))
addScreen("Air temp" , data['channel']['bw_airtemp'] + 'C')
addScreen("Ocean temp" , data['channel']['bw_oceantemp']+'C')
addScreen("Swell", formatMetres(data['channel']['bw_swell']))
addScreen("Rain", formatMetres(data['channel']['bw_rainfall']))
addScreen("Weather", data['channel']['bw_weather'])
addScreen("Winds", data['channel']['bw_winds'])



def renderScreen(title, text):
	ended = False
	print "-" * 18
	print "|" + title  + ":" + (" " * (15 - len(title))) + "|"
	if(len(text)<=16):
		print  "|" + text + (" " * (16 - len(text)))+ "|"
		print "-" * 18
		sleep(2)
		ended = True
	else:
		ended = buffer_scroll(text)
		print "-" * 18
	return ended

def buffer_scroll(text):
	global i

	ended = False

	if(i > (len(text)+16)):
		i = 0
		ended = True

	text_buffer = (" " * 16) + text + (" " * 16)

	print "|" + text_buffer[i:i+16] + "|"
	i = i + 1

	return ended

i = 0;

animation_end = False

while (1):
	print chr(27) + "[2J"
	screen_data = displays[display_index]
	print screen_data
	animation_end = renderScreen(screen_data['title'],formatMetres(screen_data['text']))
	if(animation_end):
		display_index = display_index + 1
	if(display_index >= len(displays)):
		display_index = 0

	sleep(0.1)

