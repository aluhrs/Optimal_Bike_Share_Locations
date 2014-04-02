import json
import model
import numpy
import permutations
from scipy.cluster.vq import *

def kmeans(data):
	#print data
	num = numpy.array(data)
	#print num
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

def create_file(hotspots):
	new_file = open("./static/hot_spots1.txt", 'w')
	new_file.write(json.dumps(hotspots))
	new_file.close()

	print "Your file hot_spots.txt has been created."

def main(): 
	#loop through the permutation.py tuples
	perm = permutations.per()
	tup = permutations.tuples(perm)
	# if e is in the list:
	for t in tup:
		k = ''.join(t)
		print k
		# loop through the points in the crowd_sourced table
		the_app = model.Crowd_Sourced()
		all_data = the_app.to_dict()
		db_lats_and_longs = []
		for data in all_data:

			lat = data["latitude"]
			lng = data["longitude"]
			num_of_appends = data["votes"]
			#print lat, lng
			# check what's in the tuple
			# grab the corresponding data
			if "e" in t:
				if data["elevation_reason"]:
					#print "e" 
					num_of_appends += 3
			if "f" in t:
				if data["food_reason"]:
					#print "f" 
					num_of_appends += 3
			if "g" in t:
				if data["grocery_reason"]:
					#print "g"
					num_of_appends += 5
			if "o" in t:
				if data["other_poi_reason"]:
					#print "o"
					num_of_appends += 3
			if "t" in t:
				if data["transportation_reason"]:
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
		converted_kmeans = convert_kmeans_to_list(hot_spots)

		for i in converted_kmeans:
			lat = i[0]
			lng = i[1]
			key = k
			new_point = model.Possible_Station(latitude=lat, longitude=lng, key=key)
			model.session.add(new_point)
			#print "A point with lat: %r and lng: %r and key: %r has been added to the database." % (lat, lng, key)

		create_file(converted_kmeans)
		model.session.commit()
		print "The points have been added to the Possible Stations table."
		db_lats_and_longs = []


if __name__ == "__main__":
	main()