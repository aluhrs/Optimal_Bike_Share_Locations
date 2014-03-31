import model
import urllib2
import json
import math

"""
This file:
1) Pulls elevation data from Google Maps API for all of the points in the Crowd_Sourced table in the database.
2) Reads the json data from Google Maps and updates the elevation column in the database with the elevation data.
3) Pulls the elevation data back out, creates a radius of about 3 block radius around each point
4) Calculates the elevation grade
5) Send back to the database a key to let the database know a point has been flagged as upvoted for elevation

"""

points = model.session.query(model.Crowd_Sourced).all()

# encode the url
def get_location(points):
	elevations = []
	
	for i in range(len(points)):
			if points[i].elevation == None:
				if len(elevations) < 2400:
					id = points[i].id
					latitude = points[i].latitude
					longitude = points[i].longitude				
					url = build_url(latitude, longitude)
					elevation_data = get_elevation(url)
					elevation = parse(elevation_data)
					curr = model.session.query(model.Crowd_Sourced).filter_by(id=id).one()
					curr.elevation = float(elevation)
					model.session.add(curr)
					elevations.append(elevation)
			
	model.session.commit()
	print "The elevations have been added to the database"
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

def update_elevation():
	the_app = model.Crowd_Sourced()
	all_elevation = the_app.to_dict()
	# for each point, get the elevation, and check for the elevation of 
	# surrounding data points within .004 range of each lat/lng
	d = {}
	for i in all_elevation:
		lat_i = i["latitude"]
		high_lat_i = lat_i + .002
		low_lat_i = lat_i - .002
		lng_i = i["longitude"]
		high_lng_i = lng_i + .002
		low_lng_i = lng_i - .002
		d[i["id"]] = {}
		d[i["id"]]["lat_o"] = lat_i
		d[i["id"]]["lng_o"] = lng_i
		d[i["id"]]["el_o"] = i["elevation"]
		d[i["id"]]["dictel"] = {}
		d[i["id"]]["dictel"]["el"] = 0
		for j in all_elevation:
			lat_j = j["latitude"]
			lng_j = j["longitude"]
			el_j = j["elevation"]
			# if the lats and longs don't equal each other
			if lat_i != lat_j and lng_i != lng_j:
				# create a radius of .002 in any direction
				if lat_j < high_lat_i and lat_j > low_lat_i and lng_j < high_lng_i and lng_j > low_lng_i:
					if el_j >= d[i["id"]]["dictel"]["el"]:
						d[i["id"]]["dictel"]["lat"] = lat_j
						d[i["id"]]["dictel"]["lng"] = lng_j
						d[i["id"]]["dictel"]["el"] = el_j

	rise = calc_rise(d)
	run = calc_run(rise)
	percentage = calc_elevation_grade(rise)
	upvoted = send_to_db_elevation(percentage)
	return json.dumps(percentage)

# get the difference between the lowest and the highest
# this is in meters
def calc_rise(dictionary):
	for d in dictionary:

		if dictionary[d]["dictel"]["el"] != []:
			#diff = max(dictionary[d]["list of elevations"])
			maximum = dictionary[d]["dictel"]["el"]
			original = dictionary[d]["el_o"]
			dictionary[d]["eldiff"] = maximum - original 
		else:
			dictionary[d]["eldiff"] = 0

	return dictionary


def calc_run(dictionary):

	for d in dictionary:
		if dictionary[d]["dictel"]["el"] > 0:
			lat1 = dictionary[d]["lat_o"]
			long1 = dictionary[d]["lng_o"]
			lat2 = dictionary[d]["dictel"]["lat"]
			long2 = dictionary[d]["dictel"]["lng"]

			#Convert latitude and longitude to 
			#spherical coordinates in radians.
			degrees_to_radians = math.pi/180.0
			    
			# phi = 90 - latitude
			phi1 = (90.0 - lat1)*degrees_to_radians
			phi2 = (90.0 - lat2)*degrees_to_radians
			    
			# theta = longitude
			theta1 = long1*degrees_to_radians
			theta2 = long2*degrees_to_radians
			    
			# Compute spherical distance from spherical coordinates.
			    
			# For two locations in spherical coordinates 
			# (1, theta, phi) and (1, theta, phi)
			# cosine( arc length ) = 
			#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
			# distance = rho * arc length

			cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
			       math.cos(phi1)*math.cos(phi2))
			arc = (math.acos( cos )) * 6373000
			dictionary[d]["distance"] = arc


    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
	return dictionary

# calculte the elevation incline by dividing the rise by the run
def calc_elevation_grade(dictionary):
	for d in dictionary:
		if dictionary[d]["eldiff"] != 0 and dictionary[d]["dictel"]["el"] > 0:
			dictionary[d]["eldiffpercent"] = (dictionary[d]["eldiff"]/dictionary[d]["distance"]) * 100
		else:
			dictionary[d]["eldiffpercent"] = 0

	return dictionary


def send_to_db_elevation(dictionary):
	for d in dictionary:
		if dictionary[d]["eldiffpercent"] < 5:
			# add 1 to the vote data in the db
			# add elevation as a reason
			id = d
			upvote = model.session.query(model.Crowd_Sourced).filter_by(id=id).one()
			#upvote.votes += 1
			upvote.elevation_reason = True
			model.session.add(upvote)
			print "%r has added elevation as a reason" % id

	model.session.commit()
	print "All of the points have been added to the db as elevation_reason."

if __name__ == "__main__":
	#url = get_location(points)
	elevation = update_elevation()