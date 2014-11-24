import feedparser
from time import sleep

text_length_to_display = 16

displays = []
display_index = 0;

def formatMetres(data):
	return data.replace(" metres" , "m").replace(" metre" , "m")

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






def renderScreen(title, text):
	render_title = title  + ":" + (" " * (15 - len(title)))
	render_text = render_detail(text)

	print render_title
	print render_text[0]

	return render_text[1]



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

	return [render_text, sleep]


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

i = 0;

def draw():
	global display_index

	print chr(27) + "[2J"

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

while (1):
	draw()


