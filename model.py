import config
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text

from sqlalchemy.orm import backref, sessionmaker, scoped_session, relationship


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
		"""Adds all of the CurrentStation columns to a dictionary, so the data
		can be easily formatted in the router.py"""

		output_dict = {}

		output_dict["id"] = self.id
		output_dict["latitude"] = float(self.latitude)
		output_dict["longitude"] = float(self.longitude)
		output_dict["city"] = self.city
		output_dict["stationName"] = self.station_name

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
		"""Adds all of the CrowdSourced columns to a dictionary, so the data
		can be easily formatted in the router.py"""

		output_dict = {}

		output_dict["id"] = self.id
		output_dict["latitude"] = float(self.latitude)
		output_dict["longitude"] = float(self.longitude)
		output_dict["votes"] = int(self.votes)
		if self.elevation:
				output_dict["elevation"] = float(self.elevation)
		if self.elevation_reason:
			output_dict["elevation_reason"] = self.elevation_reason
		if self.grocery_reason:
			output_dict["grocery_reason"] = self.grocery_reason
		if self.transportation_reason:
			output_dict["transportation_reason"] = self.transportation_reason
		if self.food_reason:
			output_dict["food_reason"] = self.food_reason
		if self.other_poi_reason:
			output_dict["other_poi_reason"] = self.other_poi_reason

		return output_dict


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
		"""Adds all of the PossibleStation columns to a dictionary, so the data
		can be easily formatted in the router.py"""

		output_dict = {}

		output_dict["id"] = self.id
		output_dict["latitude"] = float(self.latitude)
		output_dict["longitude"] = float(self.longitude)
		output_dict["key"] = self.key
		output_dict["cluster"] = int(self.cluster)
		output_dict["cluster_length"] = int(self.cluster_length)
		output_dict["cluster_rank"] = int(self.cluster_rank)

		return output_dict


def create_tables():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
	create_tables()