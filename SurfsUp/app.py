
# Import all dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify, session

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model

Base = automap_base()

# Reflect the tables

Base.prepare(engine, reflect=True)

# Add these references to the table

measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################

session = Session(engine)
app = Flask(__name__)

app.run()

#################################################
# Flask Routes
#################################################

# List all available api routes.

@app.route("/")
def welcome():
    return (
        f"Available Routes for Hawaii Weather Data:<br/><br>"
        f"-- Daily Precipitation Totals for Last Year: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"-- Active Weather Stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"-- Daily Temperature Observations for Station USC00519281 for Last Year: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"-- Min, Average & Max Temperatures for Date Range: /api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"NOTE: If no end-date is provided, the trip api calculates stats through 08/23/17<br>" 
    )

@app.route("/api/v1.0/precipitation")
def precipitation(): 

# Return a list of the total of the daily precipitation for specified time

    start_date = '2016-08-23'
    sel = [measurement.date,
       func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
    filter(measurement.date >= start_date).\
    group_by(measurement.date).\
    order_by(measurement.date).all()

    session.close()

# Convert the query results to a dictionary by using date as the key and prcp as the value.
    precipitation_dates = []
    precipitation_totals = []

    for date, dailytotal in precipitation:
        precipitation_dates.append(date)
        precipitation_totals.append(dailytotal)
        precipitation_dict = dict(zip(precipitation_dates, precipitation_totals))
    
    return jsonify(precipitation_dict)



# Do the same for stations

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [measurement.station]
    active_stations = session.query(*sel).\
    group_by(measurement.station).all()

    session.close()

#Return a list of stations from the dataset
    list_of_stations = list(np.ravel(active_stations))
    return jsonify(list_of_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
# Query the dates and temperature observations of the most-active station for the previous year of data.
    start_date = '2016-08-23'
    sel = [measurement.date,
       measurement.tobs]
    station_temps = session.query(*sel).\
        filter(measurement.date >= start_date, measurement.station == 'USC00519281').\
        group_by(measurement.date).\
        order_by(measurement.date).all()
     
    session.close()

# Create a dictionary with the date as the key the temperature as the value
    observation_dates = []
    temp_observations = []

    for date, observation in station_temps:
        observation_dates.append(date)
        temp_observations.append(observation)

    most_active_tobs_dict = dict(zip(observation_dates, temp_observations))
# Return a JSON list of the minimum temperature, the average temperature, 
# and the maximum temperature for a specified start or start-end range.
    return jsonify(most_active_tobs_dict)

@app.route("/api/v1.0/trip/<start_date>")
def trip1(start_date, end_date='2017-08-23'):
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
     
    trip_stats = []
    for min, avg, max in query_result:
        trip_dict = {}
        trip_dict["Min"] = min
        trip_dict["Average"] = avg
        trip_dict["Max"] = max
        trip_stats.append(trip_dict)

    # If the query returns non-null values return the results,
    # otherwise return an error message
    if trip_dict['Min']: 
        return jsonify(trip_stats)
    else:
        return jsonify({"error": f"Date {start_date} not found or not formatted as YYYY-MM-DD."}), 404
    

@app.route("/api/v1.0/trip/<start_date>/<end_date>")
def trip2(start_date, end_date='2017-08-23'):

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    trip_stats = []
    for min, avg, max in query_result:
        trip_dict = {}
        trip_dict["Min"] = min
        trip_dict["Average"] = avg
        trip_dict["Max"] = max
        trip_stats.append(trip_dict)

    # If the query returns non-null values return the results,
    # otherwise return an error message

    if trip_dict['Min']: 
        return jsonify(trip_stats)
    else:
        return jsonify({"error": f"Date(s) not found, invalid date range or dates not formatted correctly."}), 404