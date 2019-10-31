import numpy as np
import datetime as dt 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<p><strong>Available Routes:</strong></p>"
        f"<p>/api/v1.0/precipitation</p>"
        f"<p>/api/v1.0/stations</p>"
        f"<p>/api/v1.0/tobs</p>"
        f"<p>/api/v1.0/&#60;start&#62;</p>"
        f"<p><li>Example:  /api/v1.0/2016-08-23</li></p>"
        f"<p>/api/v1.0/&#60;start&#62;/&#60;end&#62;</p>"
        f"<p><li>Example:  /api/v1.0/2016-08-23/2017-08-23</li></p>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of station and precipitation data"""
    # Query all precip data
    results = session.query(Measurement.date, Measurement.station, Measurement.prcp).order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append
    all_precip = []
    for date, station, prcp in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['station'] = station
        precip_dict['prcp'] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict['station'] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""
    # Query all temperature data; the gitlab file said only the last year of data but that seemed like a pointless api call - it should have an input if it is limiting dates
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append
    all_temp = []
    for date, station, tobs in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['station'] = station
        temp_dict['tobs'] = tobs
        all_temp.append(temp_dict)

    return jsonify(all_temp)

@app.route("/api/v1.0/<start>")
def start_precip(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # check date string
    try:
        dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect start date format, should be YYYY-MM-DD")

    """Return a list of precipitation data after a supplied date"""
    # Query precipation data after specified date
    results = session.query(func.min(Measurement.prcp), func.max(Measurement.prcp), func.avg(Measurement.prcp)).filter(Measurement.date >= start).order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    start_precip = []
    for min_precip, max_precip, avg_precip in results:
        start_precip_dict = {}
        start_precip_dict['min_precip'] = min_precip
        start_precip_dict['max_precip'] = max_precip
        start_precip_dict['avg_precip'] = avg_precip
        start_precip.append(start_precip_dict)

    return jsonify(start_precip)


@app.route("/api/v1.0/<start>/<end>")
def dates_precip(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # check start date string
    try:
        dt.datetime.strptime(start, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect start date format, should be YYYY-MM-DD")

    # check end date string
    try:
        dt.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect end date format, should be YYYY-MM-DD")


    """Return a list of precipitation data between two date ranges"""
    # Query all precipitation data between two dates
    results = session.query(func.min(Measurement.prcp), func.max(Measurement.prcp), func.avg(Measurement.prcp)).filter(Measurement.date >= start).filter(Measurement.date <= end).order_by(Measurement.date.desc()).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation data
    dates_precip = []
    for min_precip, max_precip, avg_precip in results:
        dates_precip_dict = {}
        dates_precip_dict['min_precip'] = min_precip
        dates_precip_dict['max_precip'] = max_precip
        dates_precip_dict['avg_precip'] = avg_precip
        dates_precip.append(dates_precip_dict)

    return jsonify(dates_precip)


if __name__ == '__main__':
    app.run(debug=True)


# Note:  I do not understand the Hints section on gitlab - I can join the two tables together but I did not see anything specifying the need.