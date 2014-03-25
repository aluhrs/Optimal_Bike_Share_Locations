from flask import Flask, render_template, redirect, request, g, session, url_for
import model
import config
import json
import math
#import distance
#import elevation

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def load_map():
	# load from the db and pass them to jinja
	return render_template("map.html")

@app.route("/ajax/currentstations")
def current_stations():
	the_app = model.Current_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

@app.route("/ajax/possiblestations")
def possible_stations():
	the_app = model.Possible_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

@app.route("/getelevation")
def get_elevation():
	the_app = model.Crowd_Sourced()
	all_elevation = the_app.get_elevation()
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
		d[i["id"]]["latitude"] = lat_i
		d[i["id"]]["longitude"] = lng_i
		d[i["id"]]["elevation"] = i["elevation"]
		d[i["id"]]["list of elevations"] = []
		for j in all_elevation:
			lat_j = j["latitude"]
			lng_j = j["longitude"]
			if lat_i != lat_j and lng_i != lng_j:
				#TODO: need to somehow add lat/lng into this so i can calc the run
				if lat_j < high_lat_i and lat_j > low_lat_i and lng_j < high_lng_i and lng_j > low_lng_i:
					d[i["id"]]["list of elevations"].append(j["elevation"])

	sorted_dict = sort_list_of_elevations(d)
	rise = calc_rise(sorted_dict)
	#run = calc_run(rise)
	percentage = calc_incline(rise)
	return json.dumps(percentage)


# sort the list of elevations
def sort_list_of_elevations(dictionary):
	for d in dictionary:
		new_list = sorted(dictionary[d]["list of elevations"])
		dictionary[d]["list of elevations"] = new_list
		
	return dictionary


#get the difference between the lowest and the highest
def calc_rise(dictionary):
	for d in dictionary:
		if dictionary[d]["list of elevations"] != []:
			#diff = max(dictionary[d]["list of elevations"])
			maximum = max(dictionary[d]["list of elevations"])
			original = dictionary[d]["elevation"]
			dictionary[d]["elevation difference"] = maximum - original 
		else:
			dictionary[d]["elevation difference"] = 0

	return dictionary

def calc_run(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
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
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc

# calculte the elevation incline by dividing the rise by the run
# 2112 is approximately .4 miles which is the difference between the highest points possible
def calc_incline(dictionary):
	for d in dictionary:
		if dictionary[d]["elevation difference"] != 0:
			dictionary[d]["elevation difference percentage"] = (dictionary[d]["elevation difference"]/2112) * 100
		else:
			dictionary[d]["elevation difference percentage"] = 0

	return dictionary



#rank them from dissimilar to highly similar based on the difference
#if similar, add additional vote(s)
#if dissimilar, leave it alone	

#1584 - distance

#15.207 - difference in elevation from highest to lowest
#.96 - elevation grade

#25.8669 - highest elevation
#1.633 - elevation grade




if __name__ == "__main__":
    app.run(debug=True)