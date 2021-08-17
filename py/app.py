import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import the dependencies that we need for Flask
from flask import Flask, jsonify

# set up our database engine for the Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Define name base 
Base = automap_base()

# reflect the database
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python
session = Session(engine)

# define our app for our Flask application
app = Flask(__name__)

# All of your routes should go after the app = Flask(__name__) line of code

# define the welcome route 
@app.route("/")

# Next, add the precipitation, stations, tobs, and temp routes that we'll need for this module into our return statement
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

 # next route we'll build is for the precipitation analysis
@app.route("/api/v1.0/precipitation")

 # create the precipitation() function
 # the line of code that calculates the date one year ago from the most recent date in the database
 # query to get the date and precipitation for the previous year
 # dictionary with the date as the key and the precipitation as the value. We'll use jsonify() to format our results into a JSON structured file
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


# the next route which is station
@app.route("/api/v1.0/stations")

# Create a function for it
# create a query that will allow us to get all of the stations in our database
# start by unraveling our results into a one-dimensional array
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create the temperature observations route
@app.route("/api/v1.0/tobs")

# create a function
# calculate the date one year ago from the last date in the database
# query the primary station for all the temperature observations from the previous year
# unravel the results into a one-dimensional array and convert that array into a list
# we want to jsonify our temps list, and then return it
# Add the return statement to the end of your code
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# the minimum, maximum, and average temperatures
# will have to provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats()
# add parameters to our stats()function: a start parameter and an end parameter
# create a query to select the minimum, average, and maximum temperatures from our SQLite database
# determine the starting and ending date, add an if-not statement to our code
# jsonify our results and return them
# he asterisk is used to indicate there will be multiple results for our query
# calculate the temperature minimum, average, and maximum with the start and end dates. We'll use the sel list,
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)