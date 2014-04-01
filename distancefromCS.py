"""This script deletes the points that are within a couple of blocks from a current station."""

import model

def get_crowd_sourced_from_db():
	the_app = model.Crowd_Sourced()
	crowd_sourced_points = the_app.to_dict()
	cs = list_lat_lngs(crowd_sourced_points)
	return cs



def get_possible_stations_from_db():
	the_app = model.Current_Station()
	curr_stations = the_app.to_dict()
	ps = list_lat_lngs(curr_stations)
	return ps


def list_lat_lngs(data):

	lat_lng = []

	for i in range(len(data)):
		#print data[i]
		id = data[i]["id"]
		lat = data[i]["latitude"]
		lng = data[i]["longitude"]
		lat_lng.append((id,lat,lng))

	return lat_lng


def identify_points_near_curr_stations(cs, ps):

	to_delete = []
	for i in cs:
		lat_i = i[1]
		high_lat_i = lat_i + .002
		low_lat_i = lat_i - .002
		lng_i = i[2]
		high_lng_i = lng_i + .002
		low_lng_i = lng_i - .002
		for j in ps:
			lat_j = j[1]
			lng_j = j[2]
			if lat_j < high_lat_i and lat_j > low_lat_i and lng_j < high_lng_i and lng_j > low_lng_i:
				#either downvote or delete from DB
				#query db
				to_be_del = model.session.query(model.Crowd_Sourced).filter_by(id=i[0]).one()
				model.session.delete(to_be_del)
				to_delete.append(i)

	model.session.commit()
	print len(to_delete)
	print "The points have been removed from the database."


if __name__ == "__main__":
	cs = get_crowd_sourced_from_db()
	ps = get_possible_stations_from_db()
	identify_points_near_curr_stations(cs, ps)