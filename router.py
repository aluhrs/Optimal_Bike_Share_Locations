from flask import Flask, render_template, redirect, request, g, session, url_for
import model
import config
import json
import math
import os
import parser
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
	crowd_sourced_hs = the_app.to_dict()
	# go through a loop and only add the ones that have key = c
	ret = []
	for i in crowd_sourced_hs:
		if i["key"] == "c":
			ret.append(i)

	return json.dumps(ret)

@app.route("/getelevation")
def get_elevation():
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
			if lat_i != lat_j and lng_i != lng_j:
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

@app.route("/ajax/elevation")
def toggle_elevation():
	the_app = model.Possible_Station()
	elevation = the_app.to_dict()
	# create new kmeans-created hot_spots
	# recalc = parser.create_lat_lng_list_from_db(elevation)
	# hot_spots = parser.kmeans(recalc)
	# converted_kmeans = parser.convert_kmeans_to_list(hot_spots)
	# hot_spots = parser.create_file(converted_kmeans)
	# # run a function to drop the hot_spots table and re-seed it
	# # re-query the database for the updated hotspots
	# the_app1 = model.Possible_Station()
	# hotspots = the_app1.to_dict()
	# print hotspots

	# return json.dumps(hotspots)
	ret = []
	for i in elevation:
		if i["key"] == "e":
			ret.append(i)

	return json.dumps(ret)


# def drop_and_recreate_hot_spots():
# 	model.Possible_Station.drop(model.engine, checkfirst=True)
# 	seed.load_possible_stations(session)


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
# 2112 is approximately .4 miles which is the difference between the highest points possible
def calc_elevation_grade(dictionary):
	for d in dictionary:
		if dictionary[d]["eldiff"] != 0 and dictionary[d]["dictel"]["el"] > 0:
			dictionary[d]["eldiffpercent"] = (dictionary[d]["eldiff"]/dictionary[d]["distance"]) * 100
		else:
			dictionary[d]["eldiffpercent"] = 0

	return dictionary


def send_to_db_elevation(dictionary):
	for d in dictionary:
		if dictionary[d]["eldiffpercent"] > 15:
			# add 1 to the vote data in the db
			# add elevation as a reason
			id = d
			upvote = model.session.query(model.Crowd_Sourced).filter_by(id=id).one()
			print upvote.votes
			upvote.votes += 1
			upvote.el_reason = True
			model.session.add(upvote)
			print "%r now has a vote of: %r" % (id, upvote.votes)

	model.session.commit()
	print "All of the votes have been added to the db."






#rank them from dissimilar to highly similar based on the difference
#if similar, add additional vote(s)
#if dissimilar, leave it alone	

#48.2803 meters in .03 miles - run

#15.207 - difference in elevation from highest to lowest
# - elevation grade

#25.8669 - highest elevation
#31.5 - elevation grade
#37.77675282, -122.41734552
#37.77758387, -122.41662455





if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)


