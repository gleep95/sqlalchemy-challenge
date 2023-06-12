# Import the dependencies.
from dateutil.relativedelta import relativedelta
import pandas as pd
import datetime as dt
import numpy as np
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
database1 = automap_base()
# reflect the tables
database1.prepare(engine, reflect=True)

# Save references to each table
HI_measurement = database1.classes.measurement
HI_station = database1.classes.station

# Create our session (link) from Python to the DB
session_link = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    session_link = Session(engine)
    prcp_data = session_link.query(HI_measurement.prcp, HI_measurement.date).all()
    session_link.close()
    prcp_list = []
    for prcp, date in prcp_data:
        prcp_dict = {}
        prcp_dict["precipitation"] = prcp
        prcp_dict["date"] = date
        prcp_list.append(prcp_data)
    return jsonify(prcp_list) 


@app.route("/api/v1.0/stations")
def stations():
    station_data = session_link.query(HI_station.station, HI_station.name).all()
    return jsonify(station_data)



past_year = '2017-08-23'
@app.route("/api/v1.0/tobs")
def tobs():
    temp_data = session_link.query(HI_measurement.date, HI_measurement.station, HI_measurement.tobs).filter(HI_measurement.date >= past_year).all()
    return jsonify(temp_data)



@app.route("/api/v1.0/<start>")
def start(date):
    temp_data1 = session_link.query(func.min(HI_measurement.tobs), func.avg(HI_measurement.tobs), func.max(HI_measurement.tobs)).filter(HI_measurement.date >= date).all()
    return jsonify(temp_data1)





@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    temp_data2 = session_link.query(func.min(HI_measurement.tobs), func.avg(HI_measurement.tobs), func.max(HI_measurement.tobs)).filter(HI_measurement.date >= start).filter(HI_measurement.date <= end).all()
    return jsonify(temp_data2)


if __name__ == "__main__":
    app.run(debug=True)