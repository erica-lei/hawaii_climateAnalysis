from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import Session
from sqlalchemy import func, create_engine
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.automap import automap_base

from flask import Flask, jsonify
import numpy as np
import datetime as dt

engine = create_engine('sqlite:///hawaii.sqlite') #to connect to my DB
session = Session(bind = engine)
Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()
session = Session(engine)
Stations = Base.classes.stations
Measurement = Base.classes.Measurement


app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precipitation():
    all_results=[]
    #Query all Measurement
    results = session.query(Measurement).filter(Measurement.date >= '2017-04-04').all()   
    #Create a dictionary from the row data and append to list    
    for data in results:
        results_dict={}
        results_dict["date"] = data.date
        results_dict["tobs"] = data.tobs
        all_results.append(results_dict)  
    return jsonify(all_results)

@app.route("/api/v1.0/stations")
def station():
    station = session.query(Measurement.station).group_by(Measurement.station).all()
   #station= session.query(Stations.station).all()
    hawaii_stations = list(np.ravel(station))   
    return jsonify(hawaii_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    tob_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2017-04-04').all()
    #use np.ravel to combine the tobs
    tobs_results = list(np.ravel(tob_query))
    return jsonify(tobs_results)
    

@app.route("/api/v1.0/2017-07-01/2017-07-15")
def two_dates():
    temp_query = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date.between("2017-07-01", "2017-07-07")).all()   
    temp_results = list(np.ravel(temp_query))
    return jsonify(temp_results)

@app.route("/api/v1.0/2017-07-11")
def start_temp():
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >='2017-07-11').all()
    start_date = list(np.ravel(results))
    return jsonify(start_date)


if __name__ == "__main__":
    app.run(debug=True)