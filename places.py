"""This file gets places data from each of the points in the 
crowd_sourced table in the database from the Google Maps Places API."""

import model
import urllib2
import json
import config

#test with limit 1
points = model.session.query(model.Crowd_Sourced).all()

# encode the url
def get_location(points):
	locations_list = []
	
	for i in range(len(points)):
			if len(locations_list) < 995:
				if points[i].grocery_reason == None and points[i].transportation_reason == None and points[i].food_reason == None and points[i].other_poi_reason == None:
					id = points[i].id
					#print id
					curr = model.session.query(model.Crowd_Sourced).filter_by(id=id).one()
					latitude = points[i].latitude
					longitude = points[i].longitude				
					url = build_url(latitude, longitude)
					json_data = get_data(url)
					
					# print json_data
					for e in range(len(json_data["results"])):
						types = json_data["results"][e]["types"]
						# types_len = len(types)
						# print types_len
						for i in range(len(types)):
							# if i == types_len:
							if types[i] == "grocery_or_supermarket":
								#print "For %r: For groceries: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (id, types, i, types[i])
								curr.grocery_reason = True
								model.session.add(curr)
								model.session.commit()
							if types[i] in ["bus_station", "subway_station", "train_station"]:
								#print "For %r: For transportation: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (id, types, i, types[i])
								curr.transportation_reason = True
								model.session.add(curr)
								model.session.commit()
							if types[i] == "food":
								#print "For %r: For food: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (id, types, i, types[i])
								curr.food_reason = True
								model.session.add(curr)
								model.session.commit()
							if types[i] in ["home_goods_store", "movie_theater", "park", "shopping_mall"]:
								#print "For %r: For other: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (id, types, i, types[i])
								curr.other_poi_reason = True
								model.session.add(curr)
								model.session.commit()
					locations_list.append(id)			
	#create_file(locations_list)				
	#print locations_list
	print len(locations_list)
			
	#model.session.commit()
	print "The points of interest information have been added to the database"

# use urllib2 to open the url
def build_url(latitude, longitude):
	locations = str(latitude) + "," + str(longitude)
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=300&types=bar|bus_station|food|grocery_or_supermarket|home_goods_store|movie_theater|park|shopping_mall|subway_station|train_station&sensor=false&key="+config.GOOGLE_API_KEY
	return url % locations

# get elevation
def get_data(url):
	response = urllib2.urlopen(url)
	json_data = json.loads(response.read())
	return json_data

def create_file(data):
	new_file = open("./static/places.txt", 'w')
	new_file.write(json.dumps(data))
	new_file.close()

	print "Your file places.txt has been created."

# def parse(json_data):
# 	# for loop to go through length of the list of types

# 	for e in range(len(json_data["results"])):
# 		types = json_data["results"][e]["types"]
# 		for i in range(len(types)):
# 			if types[i] == "neighborhood":
# 				print types[i]

# 	return json_data["results"][0]["types"]

"""
 {
         "geometry" : {
            "location" : {
               "lat" : 37.7759073,
               "lng" : -122.4245247
            },
            "viewport" : {
               "northeast" : {
                  "lat" : 37.7787572,
                  "lng" : -122.4222133
               },
               "southwest" : {
                  "lat" : 37.7704571,
                  "lng" : -122.4299304
               }
            }
         },
         "icon" : "http://maps.gstatic.com/mapfiles/place_api/icons/geocode-71.png",
         "id" : "0e890421d78810c3bd713026d7125de4e09ba5b6",
         "name" : "Hayes Valley",
         "reference" : "CpQBjwAAAJcok0QoCLu74YkjZU2pt5A7Nz2s2eXvhJBU9prMCW9qQG40POUlfhtMAicenyfEvfzsG-FnJyvtoR6tLrpr7GefMfuVydNZaOM5VSvseKSOMCXt65fMs-yfhvvXC9mSS2s4Ul76rI8FpPNIRDitFK7oO0PSIKCsuumlroYgNMBiQqsz4JqxxJyv_BzBwGE2ZBIQ2Hc-nPF3FmRS6M6uXPUz3RoUU28DnEnHNgkkDVvchZ6u3JV4KtE",
         "types" : [ "neighborhood", "political" ],
         "vicinity" : "San Francisco"
      },

"""

"""
for e in range(len(json_data["results"])):
	print json_data["results"][e]

for i in range(len(types)):
...     if types[i] == "neighborhood":
...             print types[i]

>>> for e in range(len(json_data["results"])):
...     types = json_data["results"][e]["types"]
...     for i in range(len(types)):
...             if types[i] == "neighborhood":
...                     print types[i]

"""
if __name__ == "__main__":
	url = get_location(points)