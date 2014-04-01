from flask import Flask, render_template, redirect, request, g, session, url_for
import model
import config
import json
import math
import os
import parser
#import distance
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
	crowd_sourced_hs = the_app.to_dict()
	# go through a loop and only add the ones that have key = c
	ret = []
	for i in crowd_sourced_hs:
		if i["key"] == "c":
			ret.append(i)

	return json.dumps(ret)

@app.route("/ajax/legend")
def toggle_checkboxes():
	the_app = model.Possible_Station()
	db_data = the_app.to_dict()

	list_args = request.args.getlist("li[]")
	s_list_args = sorted(list_args)
	key = ''.join(s_list_args)
	print "key: ", key

	ret = []
	query = model.session.query(model.Possible_Station).filter_by(key=key).all()
	for q in range(len(query)):
		d = {}
		d["latitude"] = float(query[q].latitude)
		d["longitude"] = float(query[q].longitude)
		ret.append(d)
		#lat = query[q]["latitude"]
		#lng = query[q]["longitude"]
		#ret.append[lat, lng))
	
	return json.dumps(ret)


if __name__ == "__main__":
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run(debug=True)


