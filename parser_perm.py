"""This file creates optimal locations based indiviually and any combination of elevation, 
points of interest, and proxmiity to grocery stores, transporation, or food establishments."""

import json
import model
import numpy
from operator import itemgetter, attrgetter
import permutations
from scipy.cluster.vq import *

def kmeans(data):
	num = numpy.array(data)
	hot_spots_data = kmeans2(num, 100, minit='points')

	return hot_spots_data

def kmeans_array_length(kmeans_tuple):
	#lats_lngs = kmeans_tuple[0]
	#kmeans_clusters = kmeans_tuple[1]
	lats_lngs = kmeans_tuple[0]
	clusters = kmeans_tuple[1]

	lists = []
	for x in range(len(lats_lngs)):
		d = {}
		for r in range(len(lats_lngs)):
			d["lat"] = lats_lngs[x][0]
			d["lng"] = lats_lngs[x][1]
			d["cluster_length"] = 0
			for c in clusters:
				if c == x:
					d["cluster_length"] += 1
					d["cluster"] = c
		lists.append(d)

	return lists


def convert_kmeans_to_list(kmeans_tuple):
	kmeans_array = kmeans_tuple[0]

	ret = []

	for k in kmeans_array:
		latitude = k[0]
		longitude = k[1]
		ret.append((latitude, longitude))

	return ret

def create_file(hotspots):
	new_file = open("./static/hot_spots1.txt", 'w')
	new_file.write(json.dumps(hotspots))
	new_file.close()

	print "Your file hot_spots.txt has been created."

def query_db():
	the_app = model.Crowd_Sourced()
	db_data = the_app.to_dict()
	return db_data

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

def upvote_crowd_sourced():
	db_data = query_db()
	db_lats_and_longs = []
	for data in db_data:
		lat = data["latitude"]
		lng = data["longitude"]
		num_of_appends = data["votes"]
		
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
	kmeans_cluster_arrays = kmeans_array_length(hot_spots)
	#create_file(converted_kmeans)

	for x in range(len(converted_kmeans)):
		lat = converted_kmeans[x]['lat']
		lng = converted_kmeans[x]['lng']
		cluster = converted_kmeans[x]['num_in_cluster']
		#new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key, num_in_clusters=cluster)
		#model.session.add(new_point)
		print "A point with lat: %r, lng: %r, key: %r, and cluster length of %r has been added to the database." % (lat, lng, key, cluster)

	#model.session.commit()
	print "The points have been added to the Possible Stations table."
	#return db_lats_and_longs


def upvote_reasons():
	#loop through the permutation.py tuples
	perm = permutations.per()
	tup = permutations.tuples(perm)
	# if e is in the list:
	for t in tup:
		k = ''.join(t)
		#print k
		# loop through the points in the crowd_sourced table
		all_data = query_db()
		#print all_data
		db_lats_and_longs = []
		for data in all_data:
			lat = data["latitude"]
			lng = data["longitude"]
			num_of_appends = data["votes"]
			#print lat, lng
			# check what's in the tuple
			# grab the corresponding data
			if "e" in t:
				if data.get("elevation_reason"):
					#print "e" 
					num_of_appends += 3
			if "f" in t:
				if data.get("food_reason"):
					#print "f" 
					num_of_appends += 3
			if "g" in t:
				if data.get("grocery_reason"):
					#print "g"
					num_of_appends += 5
			if "o" in t:
				if data.get("other_poi_reason"):
					#print "o"
					num_of_appends += 3
			if "t" in t:
				if data.get("transportation_reason"):
					#print "t"
					num_of_appends += 5

			if num_of_appends > 0:
				#print num_of_appends
				for x in range(num_of_appends):
					#print "yes"
					db_lats_and_longs.append((lat,lng))
					#print db_lats_and_longs
			else:
				print db_lats_and_longs
				db_lats_and_longs.append((lat,lng))

		#print db_lats_and_longs
		hot_spots = kmeans(db_lats_and_longs)
		#converted_kmeans = convert_kmeans_to_list(hot_spots)
		kmeans_cluster_arrays = kmeans_array_length(hot_spots)
		ranked = rank_cluster_length(kmeans_cluster_arrays)


		for i in range(len(ranked)):
			lat = ranked[i][0]
			lng = ranked[i][1]
			key = k
			cluster_length = ranked[i][2]
			cluster = ranked[i][3]
			cluster_rank = i + 1
			key = k
			new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key, cluster=cluster, 
										cluster_length=cluster_length, cluster_rank=cluster_rank)
			model.session.add(new_point)
			print "Point: %r, %r, Key: %r, Cluster %r, Cluster Rank: %r, Cluster Length: %r" % (lat, lng, key, cluster, cluster_rank, cluster_length)

			#new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key)
			#model.session.add(new_point)
			#print "%r, %r with key: %r has been added to the database." % (lat, lng, key)

		create_file(ranked)
		model.session.commit()
		print "The points have been added to the Possible Stations table."
		db_lats_and_longs = []


def main():
	#upvote_crowd_sourced() 
	upvote_reasons()

if __name__ == "__main__":
	main()