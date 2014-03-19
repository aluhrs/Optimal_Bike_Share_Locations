from sys import argv
import json
from operator import itemgetter, attrgetter
import numpy
from scipy.cluster.vq import *

# put this in a function so that it can do this
# but otherise pull from the db
# allow the command line to take in arguments
script, filename = argv

# open the file
f = open(filename)
# read the file
data_string = f.read()
# close the file
f.close

# convert the data from json to python
# bike_locations is a list of dictionaries
bike_locations = json.loads(data_string)

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
		lower_left_corner = lat > 37.72 and lng < -122.36
		# upper right corner = 37.81, -122.52
		if upper_right_corner:
			# lower left corner = 37.72, -122.36
			if lower_left_corner:
				clean_lats_and_longs.append((lat, lng))

	return clean_lats_and_longs

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

def kmeans(sorted_data):
	# put the sorted lats and longs into a useable format
	# (numpy array matrix)
	# for the k-means clustering algorithm
	num = numpy.array(cleaned_data)
	# use the kmeans2 method on the data and specify the
	# number of hot spots
	hot_spots_data = kmeans2(num, 5)

	return hot_spots_data

def convert_kmeans_to_list(kmeans_tuple):
	#squeezed = numpy.squeeze(kmeans_array).shape
	kmeans_array = kmeans_tuple[0]

	ret = []

	for k in kmeans_array:
		latitude = k[0]
		longitude = k[1]
		ret.append((latitude, longitude))

	return ret



# call the functions
lats_and_longs = position_and_votes(bike_locations)
sorted_by_lats = sort_lats(lats_and_longs)
cleaned_data = clean_data(sorted_by_lats)
hot_spots = kmeans(cleaned_data)
converted_kmeans = convert_kmeans_to_list(hot_spots)

