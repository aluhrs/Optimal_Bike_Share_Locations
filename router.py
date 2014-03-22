from flask import Flask, render_template, redirect, request, g, session, url_for
import model
import config
import json
#import elevation

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
def load_map():
	# load from the db and pass them to jinja
	return render_template("map.html")

@app.route("/ajax/currentstations")
def current_stations():
	the_app = model.Current_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

@app.route("/ajax/possiblestations")
def possible_stations():
	the_app = model.Possible_Station()
	ret = the_app.to_dict()
	return json.dumps(ret)

@app.route("/getelevation")
def get_elevation():
	pass
	#ret = elevation.url
	# for i in ret:
	# 	print type(ret[0])
	# loop through lats and longs
	# add it to the https request
	# https://maps.googleapis.com/maps/api/elevation/json?locations=latitude,longitude&sensor=false&key=AIzaSyC5k5lbiAeixFr-jxt4Oay-IAc0TgSp_To

	#return json.dumps(ret)
	#return json.dumps(ret)

if __name__ == "__main__":
    app.run(debug=True)