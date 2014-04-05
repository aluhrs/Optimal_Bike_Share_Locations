import model
import json
import parser
import distancefromCS

def load_current_stations(session):
	"""Load all of the current San Francisco bike share stations into the database."""
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


def load_crowd_sourced_data(session):
	"""Load all of the votes within San Francisco into the database."""
	with open("./static/bikesharemetadata1.txt") as f:
		crowd_sourced = json.loads(f.read())
		cleaned_data = clean_data(crowd_sourced)
		for location in cleaned_data:
			latitude = float(location["latitude"])
			longitude = float(location["longitude"])
			votes = int(location["votes"])
			name = location["name"]
			crowd = model.Crowd_Sourced(latitude=latitude, longitude=longitude, votes=votes, 
											name=name, crowd_sourced_reason=True)
			session.add(crowd)
		session.commit()
		print "The crowd sourced data has been added to the database."


def load_possible_stations(session):
	"""Load the optimal bike share locations based on crowdsourced data."""
	#the_app = model.Crowd_Sourced()
	#all_data = the_app.to_dict()
	with open("./static/hot_spots.txt") as f:
		hot_spots = json.loads(f.read())
		for spot in hot_spots:
			#print spot
			#latitude = float(spot[0])
			#longitude = float(spot[1])
			latitude = float(spot["lat"])
			longitude = float(spot["lng"])
			cluster = int(spot["num_in_cluster"])
			key = 'c'
			hotspot = model.Possible_Station(latitude=latitude, longitude=longitude, key=key, num_in_clusters=cluster)
			session.add(hotspot)
		session.commit()
		print "The Possible Stations have been added to the database."


def clean_data(data):
	"""ONLY get the lats and longs that fit inside the SF box"""
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
		lower_left_corner = lat > 37.735 and lng < -122.388593
		#urc_cbs = lat < 37.794061 and lng < -122.408001
		#llc_cbs = lat > 37.774679 and lng < -122.388593
		if upper_right_corner:
			if lower_left_corner:
				# if urc_cbs:
				# 	if llc_cbs:
				clean_data.append({"latitude": lat, "longitude": lng, "votes": vote,
										"name": names})

	#print len(clean_data)
	return clean_data


def main(session):
	#pass
	load_current_stations(session)
	load_crowd_sourced_data(session)
	cs = distancefromCS.get_crowd_sourced_from_db()
	ps = distancefromCS.get_current_stations_from_db()
	distancefromCS.identify_points_near_curr_stations(cs, ps)
	points = model.session.query(model.Crowd_Sourced).all()
	parser.upvote(points)
	load_possible_stations(session)


if __name__ == "__main__":
	s = model.session
	main(s)