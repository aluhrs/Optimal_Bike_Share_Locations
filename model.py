import config
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,
									  autocommit = False,
									  autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

class Current_Station(Base):
	__tablename__ = "current_stations"
	id = Column(Integer, primary_key=True)
	station_name = Column(String(100), nullable=False)
	total_docks = Column(Integer, nullable=False)
	latitude = Column(Numeric(11,8), nullable=False)
	longitude = Column(Numeric(11,8), nullable=False)
	city = Column(String, nullable=False)


	def to_dict(self):
		# query the database
		stations = session.query(Current_Station).all()
		ret = []
		for s in stations:
			d = {}
			d["latitude"] = float(s.latitude)
			d["longitude"] = float(s.longitude)
			d["city"] = s.city
			d["stationName"] = s.station_name
			ret.append(d)

		return ret


class Crowd_Sourced(Base):
	__tablename__ = "crowd_sourced"
	id = Column(Integer, primary_key=True)
	latitude = Column(Numeric(11,8), nullable=False)
	longitude = Column(Numeric(11,8), nullable=False)
	votes = Column(Integer, nullable=True)
	name = Column(String(100), nullable=True)
	elevation = Column(Numeric(11,7), nullable=True)

	def to_dict(self):
		# query the database
		stations = session.query(Crowd_Sourced).all()
		ret = []
		for s in stations:
			latitude = float(s.latitude)
			longitude = float(s.longitude)
			ret.append((latitude, longitude))

		return ret

class Possible_Station(Base):
	# TODO: reseed the database with __tablename__ = "possible_stations"
	__tablename__ = "possible_station"
	id = Column(Integer, primary_key=True)
	latitude = Column(Numeric(11, 8), nullable=False)
	longitude = Column(Numeric(11, 8), nullable=False)
	name = Column(String(100), nullable=True)

	def to_dict(self):
		# query the database
		stations = session.query(Possible_Station).all()
		ret = []
		for s in stations:
			d = {}
			d["latitude"] = float(s.latitude)
			d["longitude"] = float(s.longitude)
			ret.append(d)

		return ret

def create_tables():
    Base.metadata.create_all(engine)

	# create nullable fields for elevation, population, etc
	# send a hundred coordinates from crowdsourced data, 
	# get elevation data then populate data

#class Hot_Spots(Base):
	#__tablename__ = "hot_spots"
	# id, lat, long, station name(intersection), 
	# amount of crowdsourced votes - use this to filter out insignificant spots
	# find grocery stores/other things

if __name__ == "__main__":
	create_tables()