import model
import urllib2
import json

#test with limit 1
points = model.session.query(model.Crowd_Sourced).limit(1).all()

# encode the url
def get_location(points):
	locations_list = []
	
	for i in range(len(points)):
			if len(locations_list) < 950:
				if points[i].grocery_reason and points[i].transportation_reason and points[i].transportation_reason and points[i].food_reason and points[i].other_poi_reason
				id = points[i].id
				curr = model.session.query(model.Crowd_Sourced).filter_by(id=id).one()
				latitude = points[i].latitude
				longitude = points[i].longitude				
				url = build_url(latitude, longitude)
				json_data = get_data(url)
				for e in range(len(json_data["results"])):
					types = json_data["results"][e]["types"]
					for i in range(len(types)):
						if types[i] == "grocery_or_supermarket":
							print "For groceries: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (types, i, types[i])
							curr.grocery_reason = True
							curr.votes += 1
							model.session.add(curr)
							locations_list.append(types[i])
						if types[i] in ["bus_station", "subway_station", "train_station"]:
							print "For transportation: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (types, i, types[i])
							curr.transportation_reason = True
							curr.votes += 1
							model.session.add(curr)
							locations_list.append(types[i])
						if types[i] == "food":
							print "For food: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (types, i, types[i])
							curr.food_reason = True
							curr.votes += 1
							model.session.add(curr)
							locations_list.append(types[i])
						if types[i] in ["home_goods_store", "movie_theater", "park", "shopping_mall"]:
							print "For other: These are the types: %r. This is the number in the list: %r. This is what I am adding: %r" % (types, i, types[i])
							curr.other_poi_reason = True
							curr.votes += 1
							model.session.add(curr)
							locations_list.append(types[i])
			
	model.session.commit()
	print "The points of interest information have been added to the database"

# use urllib2 to open the url
def build_url(latitude, longitude):
	locations = str(latitude) + "," + str(longitude)
	url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=%s&radius=500&types=bar|bus_station|food|grocery_or_supermarket|home_goods_store|movie_theater|park|shopping_mall|subway_station|train_station&sensor=false&key=AIzaSyC5k5lbiAeixFr-jxt4Oay-IAc0TgSp_To"
	return url % locations

# get elevation
def get_data(url):
	response = urllib2.urlopen(url)
	json_data = json.loads(response.read())
	return json_data

def parse(json_data):
	# for loop to go through length of the list of types

	for e in range(len(json_data["results"])):
		types = json_data["results"][e]["types"]
		for i in range(len(types)):
			if types[i] == "neighborhood":
				print types[i]

	return json_data["results"][0]["types"]

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
url = get_location(points)