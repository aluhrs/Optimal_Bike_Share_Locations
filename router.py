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

	crowd_sourced_stations = model.session.query(model.CrowdSourced).all()

	station_dicts = []
	for cs in crowd_sourced_stations:
		station_dicts.append(cs.to_dict())

	return json.dumps(station_dicts)


@app.route("/ajax/currentstations")
def current_stations():
	"""Pull all of the current bike share stations from the current_stations table"""

	curr_stations = model.session.query(model.CurrentStation).all()

	station_dicts = []
	for curr in curr_stations:
		station_dicts.append(curr.to_dict())

	return json.dumps(station_dicts)


@app.route("/ajax/possiblestations")
def possible_stations():
	"""Pull all of the possible stations based solely on the crowd_sourced information
	from the possible_stations table"""

	poss_stations = model.session.query(model.PossibleStation).filter_by(key='c').all()

	station_dicts = []
	for poss in poss_stations:
		station_dicts.append(poss.to_dict())

	return json.dumps(station_dicts)


@app.route("/ajax/legend")
def toggle_checkboxes():
	"""Pull the possible stations from possible_stations table that has been flagged
	with the key that matches the checkbox(es) that have been checked"""

	checked_boxes = sorted(request.args.getlist("li[]"))
	key = ''.join(checked_boxes)

	poss_stations = model.session.query(model.PossibleStation).filter_by(key=key).all()

	station_dicts = []
	for poss in poss_stations:
		station_dicts.append(poss.to_dict())

	return json.dumps(station_dicts)


if __name__ == "__main__":
    app.run(debug=True)


