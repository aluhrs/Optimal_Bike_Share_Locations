import model
import json

# should i set these as ints in here?

# load all of the current San Francisco bike share stations into the db
def load_current_stations(session):
	with open("./static/stations.json") as f:
		bike_stations = json.loads(f.read())
		for station in bike_stations:
			if station["city"] == "San Francisco":
				station_name = station["stationName"]
				total_docks = int(station["totalDocks"])
				latitude = float(station["latitude"])
				longitude = float(station["longitude"])
				city = station["city"]
				curr = model.Current_Station(station_name=station_name, total_docks=total_docks, 
												latitude=latitude, longitude=longitude, city=city)
				session.add(curr)
		session.commit()
		print "The current stations have been added to the database."

# load all of the votes within San Francisco into the db
def load_crowd_sourced_data(session):
	with open("./static/bikesharemetadata.txt") as f:
		crowd_sourced = json.loads(f.read())
		cleaned_data = clean_data(crowd_sourced)
		for location in cleaned_data:
			latitude = float(location["latitude"])
			longitude = float(location["longitude"])
			votes = int(location["votes"])
			name = location["name"]
			crowd = model.Crowd_Sourced(latitude=latitude, longitude=longitude, votes=votes, 
											name=name)
			session.add(crowd)
		session.commit()
		print "The crowd sourced data has been added to the database."

def load_possible_stations(session):
	with open("./static/hot_spots.txt") as f:
		hot_spots = json.loads(f.read())
		for spot in hot_spots:
			latitude = float(spot[0])
			longitude = float(spot[1])
			# add a name at some point
			hotspot = model.Possible_Station(latitude=latitude, longitude=longitude)
			session.add(hotspot)
		session.commit()
		print "The Possible Stations have been added to the database."


# ONLY get the lats and longs that fit inside the SF box
def clean_data(data):
	clean_data = []
	for i in data:
		lat = i["location"]["lat"]		
		lng = i["location"]["lng"]
		if i["submissions"] == []:
			vote = 1
		else:
			vote = i["submissions"][0]["length"]
		names = i["name"]

		upper_right_corner = lat < 37.81 and lng > -122.52
		lower_left_corner = lat > 37.72 and lng < -122.36

		if upper_right_corner:
			if lower_left_corner:
				clean_data.append({"latitude": lat, "longitude": lng, "votes": vote,
												"name": names})

	return clean_data


def main(session):
	# pass
	#load_current_stations(session)
	#load_crowd_sourced_data(session)
	load_possible_stations(session)

if __name__ == "__main__":
	s = model.session
	main(s)