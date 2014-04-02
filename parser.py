"""
bike_locations[0] is a dictionary
bike_locations[0]["location"] is a dictionaries

an example of bike_locations[0]:

{u'description': u'Proposed Station Location for System Launch', 
u'name': u'Fox Plaza', 
u'updated_datetime': u'2013-05-30T16:59:45.491Z', 
u'created_datetime': u'2013-05-30T16:59:45.491Z', 
u'id': 18, 
u'dataset': {u'url': u'http://10.25.181.61:81/api/v1/sfbike/datasets/sfbike/'}, 
u'visible': True, 
u'location': {u'lat': 37.776752824, u'lng': -122.417345524}, 
u'url': u'http://10.25.181.61:81/api/v1/sfbike/datasets/sfbike/places/18/', 
u'submitter_name': u'SFMTA', 
u'submissions': [{u'url': u'http://10.25.181.61:81/api/v1/sfbike/datasets/sfbike/places/18/support/', u'length': 27, u'type': u'support'}], 
u'location_type': u'bikesite', 
u'attachments': []}
"""
"""
#####################
K-Means Clustering:

Find an optimal location (hot spot) based on clustering the data into n number of clusters

Example Output: 
the first part of the array is the hotspots
the second part of the array is the grouping each spot is in
(array([[  37.8771551 , -122.17164591],
       [  45.11379599,  -35.08469081],
       [  47.25426942, -116.5809617 ],
       [  37.37687755, -122.01158114],
       [  37.76956281, -122.43318015]]), array([4, 3, 3, ..., 2, 2, 1]))
#####################

"""

from sys import argv
import json
from operator import itemgetter, attrgetter
import numpy
from scipy.cluster.vq import *
import model
import permutations


# loop through the list of dictionaries to find all of the lats/longs and votes for each location
def position_and_votes(bike_locations):	
	lats_and_longs = []
	# if there are no up-votes, add just the lat/long once
	for l in bike_locations:
		# an example of l is bike_locations[0]
		if l["submissions"] == []:
			lats_and_longs.append(l["location"])
		else:
			# if the location has up-votes, add the lat/longs as many times as there are up-votes
			num_of_appends = l["submissions"][0]["length"]
			for x in range(num_of_appends):
				lats_and_longs.append(l["location"])

	#print lats_and_longs
	return lats_and_longs

# sort the list of lats/longs by lats (x's)
# TODO: refactor by putting in a list comprehension
def sort_lats(lats_and_longs):
	tmp_list_lats_lngs = []
	for i in lats_and_longs:
		tmp_list_lats_lngs.append((i["lat"], i["lng"]))

	sorted_by_lats = sorted(tmp_list_lats_lngs, key=itemgetter(0))
	return sorted_by_lats

# clean the data by ONLY lats and longs that fit inside the SF box
def clean_data(sorted_latslngs):
	clean_lats_and_longs = []
	for i in sorted_latslngs:
		lat = i[0]		
		lng = i[1]
		upper_right_corner = lat < 37.81 and lng > -122.52
		lower_left_corner = lat > 37.735 and lng < -122.377
		urc_cbs = lat < 37.794061 and lng < -122.408001
		llc_cbs = lat > 37.774679 and lng < -122.388593
		#bad 37.787619, -122.392711
		#good 37.779411, -122.464379
		if upper_right_corner:
			if lower_left_corner:
				# if urc_cbs:
				# 	if llc_cbs:
				clean_lats_and_longs.append((lat, lng))

	return clean_lats_and_longs


def upvote(db_data):
	db_lats_and_longs = []
	#print db_data
	for data in db_data:
		lat = data["latitude"]
		lng = data["longitude"]
		num_of_appends = data["votes"]

		# loop the list from permutations.py
		perm = permutations.per()
		tup = permutations.tuples(perm)
		 
		# if e is in the list:
		for t in tup:
			k = ''.join(t)
			if "e" in t:
				num_of_appends += 3
			if "f" in t:
				num_of_appends += 3
			if "g" in t:
				num_of_appends += 5
			if "o" in t:
				num_of_appends += 3
			if "t" in t:
				num_of_appends += 5

		# if data["crowd_sourced_reason"]:
		# 	crowd_sourced_reason = data["crowd_sourced_reason"]

		# if data["elevation_reason"]:
		# 	#print "elevation: %r" % num_of_appends
		# 	num_of_appends += 3
		# 	#print "elevation: %r" % num_of_appends

		# if data["food_reason"]:
		# 	#print num_of_appends
		# 	num_of_appends += 3
			#print num_of_appends

		# if data["grocery_reason"]:
		# 	#print "grocery: %r" % num_of_appends
		# 	num_of_appends += 5
		# 	#print "grocery: %r" % num_of_appends

		# if data["other_poi_reason"]:
		# 	#print num_of_appends
		# 	num_of_appends += 5
		# 	#print num_of_appends

		# if data["transportation_reason"]:
		# 	#print num_of_appends
		# 	num_of_appends += 5
		# 	#print num_of_appends

		
		if num_of_appends > 0:
			#print data
			for x in range(num_of_appends):
				db_lats_and_longs.append((lat,lng))
				#print db_lats_and_longs
		else:
			db_lats_and_longs.append((lat,lng))

		#print db_lats_and_longs

	hot_spots = kmeans(db_lats_and_longs)
	converted_kmeans = convert_kmeans_to_list(hot_spots)

	for i in converted_kmeans:
		lat = i[0]
		lng = i[1]
		key = k
		new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key)
		model.session.add(new_point)
		print "A point with lat: %r and lng: %r and key: %r has been added to the database." % (lat, lng, key)

	model.session.commit()
	print "The points have been added to the Possible Stations table."
	return db_lats_and_longs



def kmeans(data):
	# put the sorted lats and longs into a useable format
	# (numpy array matrix)
	# for the k-means clustering algorithm
	#print data
	num = numpy.array(data)
	print num
	# use the kmeans2 method on the data and specify the
	# number of hot spots
	hot_spots_data = kmeans2(num, 30)

	return hot_spots_data

def convert_kmeans_to_list(kmeans_tuple):
	kmeans_array = kmeans_tuple[0]

	ret = []

	for k in kmeans_array:
		latitude = k[0]
		longitude = k[1]
		ret.append((latitude, longitude))

	return ret


def update_db_elevation(hotspots, k):
	for i in hotspots:
		lat = i[0]
		lng = i[1]
		key = k
		new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key)
		model.session.add(new_point)
		print "A point with lat: %r and lng: %r and key: %r has been added to the database." % (lat, lng, key)

	model.session.commit()
	print "The points have been added to the Possible Stations table."

def create_file(hotspots):
	new_file = open("./static/hot_spots.txt", 'w')
	new_file.write(json.dumps(hotspots))
	new_file.close()

	print "Your file hot_spots.txt has been created."

def main():
	if len(argv) == 2:
		script, filename = argv
		f = open(filename)
		data_string = f.read()
		f.close

		bike_locations = json.loads(data_string)
		lats_and_longs = position_and_votes(bike_locations)
		sorted_by_lats = sort_lats(lats_and_longs)
		cleaned_data = clean_data(sorted_by_lats)
		hot_spots = kmeans(cleaned_data)
		converted_kmeans = convert_kmeans_to_list(hot_spots)
		create_file(converted_kmeans)
	else:
		the_app = model.Crowd_Sourced()
		all_data = the_app.to_dict()
		#db_lat_lng = upvote_elevation_reason(all_data)
		db_lat_lng = upvote(all_data)
		# hot_spots = kmeans(db_lat_lng)
		# converted_kmeans = convert_kmeans_to_list(hot_spots)
		#update_db_grocery(converted_kmeans)
		#update_db_grocery(converted_kmeans)
		#create_file(converted_kmeans)
	





#else:
#call the functions and add the hot_spots to the database
# def load_possible_stations(session):
# 	with open("./static/hot_spots.txt") as f:
# 		hot_spots = json.loads(f.read())
# 		for spot in hot_spots:
# 			latitude = float(spot[0])
# 			longitude = float(spot[1])
# 			# add a name at some point
# 			hotspot = model.Possible_Station(latitude=latitude, longitude=longitude)
# 			session.add(hotspot)
# 		session.commit()
# 		print "The Possible Stations have been added to the database."



if __name__ == "__main__":
	main()
   