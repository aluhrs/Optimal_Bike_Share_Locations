"""
This file used kmeans clustering to determine optimal locations based on crowdsourced 
data pulled from the database OR on a specified file in the command line.

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

def position_and_votes(bike_locations):
	"""loop through the list of dictionaries to find all of the lats/longs and votes for each location"""	
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

	return lats_and_longs

def sort_lats(lats_and_longs):
	"""sort the list of lats/longs by lats (x's)"""
	tmp_list_lats_lngs = []
	for i in lats_and_longs:
		tmp_list_lats_lngs.append((i["lat"], i["lng"]))

	sorted_by_lats = sorted(tmp_list_lats_lngs, key=itemgetter(0))
	return sorted_by_lats

def clean_data(sorted_latslngs):
	"""clean the data by ONLY lats and longs that fit inside the SF box"""
	clean_lats_and_longs = []
	for i in sorted_latslngs:
		lat = i[0]		
		lng = i[1]
		# considering updating lower_left_corner < -122.38634777
		# there should not be anything above the lat
		upper_right_corner = lat < 37.81 and lng > -122.52
		lower_left_corner = lat > 37.735 and lng < -122.377
		#urc_cbs = lat < 37.794061 and lng < -122.408001
		#llc_cbs = lat > 37.774679 and lng < -122.388593
		#bad 37.787619, -122.392711
		#good 37.779411, -122.464379
		if upper_right_corner:
			if lower_left_corner:
				# if urc_cbs:
				# 	if llc_cbs:
				clean_lats_and_longs.append((lat, lng))

	#print sorted(clean_lats_and_longs)
	return clean_lats_and_longs

def create_file(hotspots):
	new_file = open("./static/hot_spots1.txt", 'w')
	new_file.write(json.dumps(hotspots))
	new_file.close()

	print "Your file hot_spots.txt has been created."

def kmeans(data):
	"""Put the sorted lats and longs into a useable format (numpy array matrix)
	for the k-means clustering algorithm use the kmeans2 method and specify 
	the number of hot spots"""
	
	#print data
	num = numpy.array(data)
	#print num
	hot_spots_data = kmeans2(num, 100, minit='points')

	return hot_spots_data

def kmeans_array_length(kmeans_tuple):
	"""Identifies the size of the cluster"""

	lats_lngs = kmeans_tuple[0]
	clusters = kmeans_tuple[1]

	lists = []
	for x in range(len(lats_lngs)):
		d = {}
		for r in range(len(lats_lngs)):
			d["lat"] = lats_lngs[x][0]
			d["lng"] = lats_lngs[x][1]
			d["cluster_length"] = 0
			#d["num_in_clusters"] = 0
			for c in clusters:
				if c == x:
					d["cluster_length"] += 1
					d["cluster"] = c
		lists.append(d)

	return lists

def convert_kmeans_to_list(kmeans_tuple):
	"""Adds the lats and longs created from the kmeans to a list"""
	kmeans_array = kmeans_tuple[0]

	ret = []

	for k in kmeans_array:
		latitude = k[0]
		longitude = k[1]
		ret.append((latitude, longitude))

	return ret


def upvote(db_data):
	"""Identify the amount of votes for each lat and long and then
	add the lat and long to the list that amount of times. This will 
	cause the point to be ranked higher in the kmeans algorithm.
	Run the list through the kmeans algorithm, and then add the 
	newly created optimal locations to the database."""

	db_lats_and_longs = []

	for data in db_data:
		#print data
		lat = float(data.latitude)
		lng = float(data.longitude)
		num_of_appends = int(data.votes)

		
		if num_of_appends > 0:
			#print data
			for x in range(num_of_appends):
				db_lats_and_longs.append((lat,lng))
				#print db_lats_and_longs
		else:
			db_lats_and_longs.append((lat,lng))

		#print db_lats_and_longs
	return db_lats_and_longs

	#hot_spots = kmeans(db_lats_and_longs)
	#converted_kmeans = convert_kmeans_to_list(hot_spots)
	#kmeans_cluster_arrays = kmeans_array_length(hot_spots)
	#converted_kmeans = kmeans_array_length(hot_spots)
	#create_file(converted_kmeans)
	#print converted_kmeans

	
def rank_cluster_length(converted_kmeans):
	#Rank each point by the amount of points in the cluster.

	ranked = []

	for x in range(len(converted_kmeans)):
		lat = converted_kmeans[x]['lat']
		lng = converted_kmeans[x]['lng']
		cluster_length = converted_kmeans[x]['cluster_length']
		cluster = converted_kmeans[x]['cluster']
		ranked.append((lat, lng, cluster_length, cluster))

	ranked_cluster = sorted(ranked, key=itemgetter(2), reverse=True)

	#print ranked_cluster
	return ranked_cluster


def add_to_database(converted_kmeans):
	#Add the point to the database.

	for x in range(len(converted_kmeans)):
		lat = converted_kmeans[x][0]
		lng = converted_kmeans[x][1]
		cluster_length = converted_kmeans[x][2]
		cluster = converted_kmeans[x][3]
		cluster_rank = x + 1
		key = 'c'
		new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key, cluster=cluster, 
										cluster_length=cluster_length, cluster_rank=cluster_rank)
		model.session.add(new_point)
		print "Point: %r, %r, Key: %r, Cluster %r, Cluster Rank: %r, Cluster Length: %r" % (lat, lng, key, cluster, cluster_rank, cluster_length)

	model.session.commit()
	print "The points have been added to the Possible Stations table."


	
	# for x in range(len(converted_kmeans)):
	# 	lat = converted_kmeans[x]['lat']
	# 	lng = converted_kmeans[x]['lng']
	# 	cluster_length = converted_kmeans[x]['cluster_length']
	# 	cluster = converted_kmeans[x]['cluster']
	# 	#cluster_rank = converted_kmeans[x] + 1
	# 	key = 'c'
	# 	new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key, cluster=cluster, 
	# 										cluster_length=cluster_length, cluster_rank=cluster_rank)
	# 	model.session.add(new_point)
	# 	print "Point: %r, %r, Key: %r, Cluster %r, Cluster Length: %r" % (lat, lng, key, cluster, cluster_length)

	# model.session.commit()
	# print "The points have been added to the Possible Stations table."


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
		all_data = model.session.query(model.Crowd_Sourced).all()
		db_lat_lng = upvote(all_data)
		hot_spots = kmeans(db_lat_lng)
		converted_kmeans = kmeans_array_length(hot_spots)
		ranked = rank_cluster_length(converted_kmeans)
		add_to_database(ranked)
		create_file(ranked)


if __name__ == "__main__":
	main()
   