"""This script deletes the points that are within a couple of blocks from a current station."""

import model

def get_crowd_sourced_from_db():
	"""query database for the crowd_sourced data"""
	#the_app = model.CrowdSourced()
	#crowd_sourced_points = the_app.to_dict()
	crowd_sourced_points = model.session.query(model.CrowdSourced).all()
	cs = list_lat_lngs(crowd_sourced_points)
	return cs



def get_current_stations_from_db():
	"""query database for possible_stations data"""
	curr_stations = model.session.query(model.CurrentStation).all()
	#the_app = model.CurrentStation()
	#curr_stations = the_app.to_dict()
	ps = list_lat_lngs(curr_stations)
	return ps


def list_lat_lngs(data):
	"""parse data and add relevant data to a list"""
	lat_lng = []

	for i in range(len(data)):
		id = data[i].id
		lat = float(data[i].latitude)
		lng = float(data[i].longitude)
		lat_lng.append((id,lat,lng))

	return lat_lng


def identify_points_near_curr_stations(cs, ps):
	"""remove points that are near current stations"""
	to_delete = []
	for i in cs:
		lat_i = i[1]
		high_lat_i = lat_i + .005
		low_lat_i = lat_i - .005
		lng_i = i[2]
		high_lng_i = lng_i + .005
		low_lng_i = lng_i - .005
		for j in ps:
			lat_j = j[1]
			lng_j = j[2]
			if lat_j < high_lat_i and lat_j > low_lat_i and lng_j < high_lng_i and lng_j > low_lng_i:
				to_be_del = model.session.query(model.CrowdSourced).filter_by(id=i[0]).one()
				model.session.delete(to_be_del)
				to_delete.append(i)

	model.session.commit()
	print "This is the amount of points that are being deleted: %r" % len(to_delete)
	print "The points have been removed from the database."


if __name__ == "__main__":
	cs = get_crowd_sourced_from_db()
	ps = get_current_stations_from_db()
	#identify_points_near_curr_stations(cs, ps)