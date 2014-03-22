import model
import urllib2
import json

points = model.session.query(model.Crowd_Sourced).all()

# encode the url
def get_location(points):
	elevations = []
	
	for i in range(len(points)):
			if points[i].elevation == None:
				if len(elevations) < 1500:
					id = points[i].id
					latitude = points[i].latitude
					longitude = points[i].longitude				
					url = build_url(latitude, longitude)
					elevation_data = get_elevation(url)
					elevation = parse(elevation_data)
					curr = model.session.query(model.Crowd_Sourced).filter_by(id=id).one()
					#print curr.elevation
					curr.elevation = float(elevation)
					#print curr.elevation
					#db_elevation = float(elevation)
					model.session.add(curr)
					elevations.append(elevation)
			
	model.session.commit()
	#print len(elevations)
	print "The elevations have been added to the database"
	#print elevations
	#return elevations

# use urllib2 to open the url
def build_url(latitude, longitude):
	locations = str(latitude) + "," + str(longitude)
	url = "https://maps.googleapis.com/maps/api/elevation/json?locations=%s&sensor=false&key=AIzaSyC5k5lbiAeixFr-jxt4Oay-IAc0TgSp_To"
	return url % locations

# get elevation
def get_elevation(url):
	response = urllib2.urlopen(url)
	json_data = json.loads(response.read())
	return json_data

def parse(json_data):
	return json_data["results"][0]["elevation"]


url = get_location(points)