import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# set up our database engine for the Flask application 
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database 
session = Session(engine)

# define our app for our Flask application.
app = Flask(__name__)

# define the welcome route
@app.route("/")

#create a function welcome() with a return statement for our routes using f-strings
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

#create route for precipitation
@app.route("/api/v1.0/precipitation")

# create the precipitation() function 
# using line of code that calculates the date one year ago from the most recent date in the database
# write a query to get the date and precipitation for the previous year
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# create route for stations
@app.route("/api/v1.0/stations")

#create a new function called stations()
#create a query that will allow us to get all of the stations in our database
#start by unraveling our results into a one-dimensional array
#convert our unraveled results into a list
#return as JSON
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create route for temperature
@app.route("/api/v1.0/tobs")

# create a new fucntion called temp_monthly()
# calculate the date one year ago from the last date in the database
# next step is to query the primary station for all the temperature observations from the previous year
# unravel the results into a one-dimensional array and convert that array into a list
# jsonify our temps list, and then return it
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# create route for summary statistics (min, max, average) report
#provide both a starting and ending date
# switching out <start> and <end dates> with actual dates will give correct results online
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")


# create a new function, stats()
# add a start parameter and an end parameter. For now, set them both to None
#create a query to select the minimum, average, and maximum temperatures from our SQLite database. 
# start by just creating a list called "*sel" (* indicates there will be multiple results)
  # calculate the temperature minimum, average, and maximum with the start and end dates
# add an if-not statment (for starting and end date retrieval)
  #query our database using the list that we just made
  #unravel the results into a one-dimensional array and convert them to a list
  #jsonify our results and return them
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps) 
