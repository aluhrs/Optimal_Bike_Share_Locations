from sys import argv
import json

# allow the command line to take in arguments
script, filename = argv

# open the file
f = open(filename)
# read the file
data_string = f.read()
# close the file
f.close

# convert the data from json to python
bike_stations = json.loads(data_string)

# get a list of only the SF bike_stations
def SF_stations(stations):
	list_SF_stations = []

	for i in stations:
		lat = i["latitude"]
		lng = i["longitude"]
		if i["city"] == "San Francisco":
			list_SF_stations.append((lat, lng))

	return list_SF_stations


all_SF_stations = SF_stations(bike_stations)