"""The urlopen() function is bring back different information 
	than what is in the inspect element"""


from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://sfbikeshare.sfmta.com/"

# use the BASE_URL for the url
def get_dots(url):
	html = urlopen(url).read()
	soup = BeautifulSoup(html, "lxml")

	all_dots = soup.find("div", "leaflet-container leaflet-fade-anim").string
	dot = [div.string for div in soup.findAll("img", "leaflet-marker-icon  leaflet-clickable leaflet-zoom-animated")]
	return {"all_dots": all_dots,
			"dot": dot}

get_dots("http://sfbikeshare.sfmta.com/")