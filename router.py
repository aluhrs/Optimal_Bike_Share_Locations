from flask import Flask, render_template, redirect, request, g, session, url_for
import model
import config
import json

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def load_map():
	# load from the db and pass them to jinja
	return render_template("map.html")

@app.route("/ajax/currentstations")
def current_stations():
	#stations = model.session.query(model.Current_Station).all()

	# ret = []
	# # loop through and add to list
	# for s in stations:
	# 	lat = s.latitude
	# 	lng = s.longitude
	# 	city = s.city
	# 	name = s.station_name
	# 	ret.append((city, name))

	# return json.dumps(ret)
	the_app = model.Current_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

@app.route("/ajax/possiblestations")
def possible_stations():
	the_app = model.Possible_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True)