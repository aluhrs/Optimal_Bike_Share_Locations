"""

This script scrapes the BikeShare crowdsourcing website.
It does not currently save to a file, but prints to the screen.
The data needs to copied and pasted to an outside file and slightly cleaned up.

"""
from bs4 import BeautifulSoup
from urllib2 import urlopen
import json

BASE_URL = "http://sfbikeshare.sfmta.com/"

# use the BASE_URL for the url
def get_dots(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")
	print soup
	# all_dots = soup.find("div", "leaflet-container leaflet-fade-anim").string
	# dot = [div.string for div in soup.findAll("img", "leaflet-marker-icon  leaflet-clickable leaflet-zoom-animated")]
	# return {"all_dots": all_dots,
	# 		"dot": dot}

def create_file(data):
	new_file = open("./static/bikesharemetadata1.txt", 'w')
	new_file.write(json.dumps(data))
	new_file.close()

	print "Your file hot_spots.txt has been created."

dots = get_dots("http://sfbikeshare.sfmta.com/")
#create_file(dots)
