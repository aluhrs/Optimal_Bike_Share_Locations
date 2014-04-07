from flask import Flask, render_template, redirect, request, g, session, url_for
import model
import config
import json
import math
import os
import parser

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def load_map():
	"""Load the map and pass the Google Map API Key to it"""
	return render_template("map.html", gkey=config.GOOGLE_API_KEY)

@app.route("/ajax/allcrowdsourced")
def all_crowdsourced():
	"""Pull all the source data from the crowd_sourced table"""
	the_app = model.Crowd_Sourced()
	ret = the_app.to_dict()


	return json.dumps(ret)

@app.route("/ajax/currentstations")
def current_stations():
	"""Pull all of the current bike share stations from the current_stations table"""
	the_app = model.Current_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

@app.route("/ajax/possiblestations")
def possible_stations():
	"""Pull all of the possible stations based solely on the crowd_sourced information
	from the possible_stations table"""
	the_app = model.Possible_Station()
	crowd_sourced_hs = the_app.to_dict()
	ret = []
	for i in crowd_sourced_hs:
		if i["key"] == "c":
			ret.append(i)

	return json.dumps(ret)

@app.route("/ajax/legend")
def toggle_checkboxes():
	"""Pull the possible stations from possible_stations table that's been flagged
	for the checkbox(es) that have been checked"""
	the_app = model.Possible_Station()
	db_data = the_app.to_dict()

	list_args = request.args.getlist("li[]")
	s_list_args = sorted(list_args)
	key = ''.join(s_list_args)

	ret = []
	query = model.session.query(model.Possible_Station).filter_by(key=key).all()
	for q in range(len(query)):
		d = {}
		d["latitude"] = float(query[q].latitude)
		d["longitude"] = float(query[q].longitude)
		d["key"] = query[q].key
		d["cluster"] = int(query[q].cluster)
		d["cluster_length"] = int(query[q].cluster_length)
		d["cluster_rank"] = int(query[q].cluster_rank)
		ret.append(d)
	
	return json.dumps(ret)


if __name__ == "__main__":
    app.run(debug=True)


