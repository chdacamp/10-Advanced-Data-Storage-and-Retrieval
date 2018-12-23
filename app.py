import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import time
from datetime import date
from datetime import datetime

import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False}, echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date,Measurement.prcp).all()

    result_dict = dict(results)

    return jsonify(result_dict)


@app.route("/api/v1.0/stations")
def station():
    results = session.query(Station.station).all()

    result_list = list(results)

    return jsonify(result_list)

@app.route("/api/v1.0/tobs")

def tobs():
	
	today = date.today()
	results = session.query(Measurement.tobs)\
	.filter(func.date(Measurement.date) >= date(today.year-2, today.month, today.day))\
	.group_by(Measurement.date).all()
	
	result_list = list(results)

	return jsonify(result_list)
	
@app.route("/api/v1.0/<start>")
	
def starter(start):
	
	results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
	.filter(func.date(Measurement.date) >= func.date(start))\
	.group_by(Measurement.date).all()
	
	result_df = pd.DataFrame(results, columns = ['date','min','max','avg']).set_index('date')
	
	return jsonify(result_df.to_dict())

@app.route("/api/v1.0/<start>/<end>")

def start_end(start,end):
	
	results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs))\
	.filter(func.date(Measurement.date) >= func.date(start))\
	.filter(func.date(Measurement.date) <= func.date(end))\
	.group_by(Measurement.date).all()
	
	result_df = pd.DataFrame(results, columns = ['date','min','max','avg']).set_index('date')
	
	return jsonify(result_df.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
