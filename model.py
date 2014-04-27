import config
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, Boolean

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref


engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class CurrentStation(Base):
	"""This table contains all information for the current bike share stations"""
	__tablename__ = "current_stations"
	id = Column(Integer, primary_key=True)
	station_name = Column(String(100), nullable=False)
	total_docks = Column(Integer, nullable=False)
	latitude = Column(Numeric(11,8), nullable=False)
	longitude = Column(Numeric(11,8), nullable=False)
	city = Column(String, nullable=False)


	def to_dict(self):
		output_dict = {}


		output_dict["id"] = self.id
		output_dict["latitude"] = float(self.latitude)
		output_dict["longitude"] = float(self.longitude)
		output_dict["city"] = self.city
		output_dict["stationName"] = self.station_name


		# # stations = session.query(CurrentStation).all()
		# ret = []
		# for s in stations:
		# 	d = {}
		# 	d["id"] = int(s.id)
		# 	d["latitude"] = float(s.latitude)
		# 	d["longitude"] = float(s.longitude)
		# 	d["city"] = s.city
		# 	d["stationName"] = s.station_name
		# 	ret.append(d)

		return output_dict


class CrowdSourced(Base):
	"""This table contains all the data scraped from the crowd sourced
	website: http://sfbikeshare.sfmta.com/. Additionally, it houses all
	the reasons for upvoting a location"""
	__tablename__ = "crowd_sourced"
	id = Column(Integer, primary_key=True)
	latitude = Column(Numeric(11,8), nullable=False)
	longitude = Column(Numeric(11,8), nullable=False)
	votes = Column(Integer, nullable=True)
	name = Column(String(150), nullable=True)
	elevation = Column(Numeric(11,7), nullable=True)
	crowd_sourced_reason = Column(Boolean, nullable=True)
	elevation_reason = Column(Boolean, nullable=True)
	grocery_reason = Column(Boolean, nullable=True)
	transportation_reason = Column(Boolean, nullable=True)
	food_reason = Column(Boolean, nullable=True)
	other_poi_reason = Column(Boolean, nullable=True)
	


	def to_dict(self):
		stations = session.query(CrowdSourced).all()
		ret = []
		for s in stations:
			d = {}
			d["id"] = int(s.id)
			d["latitude"] = float(s.latitude)
			d["longitude"] = float(s.longitude)
			d["votes"] = int(s.votes)
			if s.elevation:
				d["elevation"] = float(s.elevation)
			if s.elevation_reason:
				d["elevation_reason"] = s.elevation_reason
			if s.grocery_reason:
				d["grocery_reason"] = s.grocery_reason
			if s.transportation_reason:
				d["transportation_reason"] = s.transportation_reason
			if s.food_reason:
				d["food_reason"] = s.food_reason
			if s.other_poi_reason:
				d["other_poi_reason"] = s.other_poi_reason

			ret.append(d)

		return ret


	def get_elevation(self):
		stations = session.query(CrowdSourced).order_by(CrowdSourced.latitude, CrowdSourced.longitude).all()
		ret = []
		for s in stations:
			if s.elevation is not None:
				d = {}
				d["id"] = int(s.id)
				d["latitude"] = float(s.latitude)
				d["longitude"] = float(s.longitude)
				d["votes"] = int(s.votes)
				d["elevation"] = float(s.elevation)

				ret.append(d)

		return ret


class PossibleStation(Base):
	"""This table contains the optimized locations for each key
	based on the kmeans clustering algorithm."""
	__tablename__ = "possible_stations"
	id = Column(Integer, primary_key=True)
	latitude = Column(Numeric(11, 8), nullable=False)
	longitude = Column(Numeric(11, 8), nullable=False)
	name = Column(String(100), nullable=True)
	key = Column(String(100), nullable=True)
	cluster = Column(Integer, nullable=True)
	cluster_length = Column(Integer, nullable=True)
	cluster_rank = Column(Integer, nullable=True)

	def to_dict(self):
		stations = session.query(PossibleStation).all()
		ret = []
		for s in stations:
			d = {}
			d["id"] = int(s.id)
			d["latitude"] = float(s.latitude)
			d["longitude"] = float(s.longitude)
			d["key"] = s.key
			d["cluster"] = int(s.cluster)
			d["cluster_length"] = int(s.cluster_length)
			d["cluster_rank"] = int(s.cluster_rank)
			ret.append(d)

		return ret


def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
	create_tables()