import feedparser
from time import sleep

text_length_to_display = 16
i = 0;
displays = []
display_index = 0;

def formatMetres(data):
	return data.replace(" metres" , "m").replace(" metre" , "m")

def clear_screens():
	global displays
	displays = []

def addScreen(title, text):
	global displays
	data_dict = {'title': title, 'text': text}
	displays.append(data_dict)


def renderScreen(title, text):
	_title = render_title(title)
	_text = render_detail(text)

	print chr(27) + "[2J"
	print _title
	print _text['text']

	return _text['wait']


def render_title(title):
	return title  + ":" + (" " * (15 - len(title)))

def render_detail(text):
	render_text = False
	sleep = 0
	if(len(text)<=16):
		render_text = text + (" " * (16 - len(text)))
		sleep = 2
	else:
		render_text = buffer_scroll(text)
		if(render_text == False):
			sleep = -1
		else:
			sleep = 0.1

	return {'text' : render_text, 'wait' : sleep}


def buffer_scroll(text):
	global i

	if(i > (len(text)+16)):
		i = 0
		render_text = False
	else:

		text_buffer = (" " * 16) + text + (" " * 16)
		render_text = text_buffer[i:i+16]

	i = i + 1

	return render_text



def draw():
	global display_index

	screen_data = displays[display_index]
	wait_interval = renderScreen(screen_data['title'],formatMetres(screen_data['text']))

	if(wait_interval < 0):
		display_index = display_index + 1
		wait_interval = 0

	if(wait_interval > 1):
		display_index = display_index + 1

	if(display_index >= len(displays)):
		display_index = 0

	sleep(wait_interval)

def get_data():
	clear_screens()
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

	while (1):
		draw()

except KeyboardInterrupt:
	print "exiting"

finally:
	print "Bye"



