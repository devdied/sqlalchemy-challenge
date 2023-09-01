# Import the dependencies.

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
M = Base.classes.measurement
S = Base.classes.station

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
        f"/api/v1.0/start: TMIN, TAVG, TMAX for all dates greater than or equal to the start date<br/>"
        f"/api/v1.0/start/end: TMIN, TAVG, TMAX for all dates from the start date to the end date, inclusive<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database.
    last_date = session.query(M.date).order_by(M.date.desc()).first().date
    query_date = dt.datetime.strptime(last_date, '%Y-%m-%d') -dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_data = session.query(M.date, M.prcp).filter(M.date >= query_date).filter(M.prcp != 'None').order_by(M.date).all()

    session.close()

    prcp_data = list(np.ravel(prcp_data))
    prcp_data = {prcp_data[i]: prcp_data[i+1] for i in range(0, len(prcp_data), 2)}

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stn_data = session.query(S.station,S.name,S.latitude,S.longitude,S.elevation).all()
    session.close()

    # Convert list of tuples into normal list
    stn_data = list(np.ravel(stn_data))

    return jsonify(stn_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database.
    last_date = session.query(M.date).order_by(M.date.desc()).first().date
    query_date = dt.datetime.strptime(last_date, '%Y-%m-%d') -dt.timedelta(days=365)
    best_stn = session.query(M.station, func.count(M.tobs)).group_by(M.station).order_by(func.count(M.tobs).desc()).all()

    tobs_data = session.query(M.date, M.tobs).filter(M.date >= query_date).filter(M.station == best_stn[0][0]).all()

    # Convert list of tuples into normal list
    tobs_data = list(np.ravel(tobs_data))

    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database.
    start_date = dt.datetime.strptime(start, '%Y-%m-%d') -dt.timedelta(days=365)

    tobsData = session.query(func.min(M.tobs),func.max(M.tobs),func.avg(M.tobs)).filter(M.date >= start_date).all()

    # Convert list of tuples into normal list
    tobsData = list(np.ravel(tobsData))
    tobsData = {'Tmin':tobsData[0],'Tmax':tobsData[1],'Tavg':tobsData[2]}
    return jsonify(tobsData)

@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database.
    start_date = dt.datetime.strptime(start, '%Y-%m-%d') -dt.timedelta(days=365)
    end_date = dt.datetime.strptime(end, '%Y-%m-%d') -dt.timedelta(days=365)
    tobsData = session.query(func.min(M.tobs),func.max(M.tobs),func.avg(M.tobs)).filter(M.date >= start_date).filter(M.date <= end_date).all()

    # Convert list of tuples into normal list
    tobsData = list(np.ravel(tobsData))
    tobsData = {'Tmin':tobsData[0],'Tmax':tobsData[1],'Tavg':tobsData[2]}
    return jsonify(tobsData)

if __name__ == '__main__':
    app.run(debug=True)

