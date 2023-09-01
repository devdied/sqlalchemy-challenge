# sqlalchemy-challenge
In this project, we perform a climate analysis about long holiday vacation in Honolulu, Hawaii. I used use Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Specifically, used SQLAlchemy ORM queries, Pandas, and Matplotlib for visualization.

* The starter code has precipitation and station analysis.
* App.py has the code for following available API rotes:
  - /api/v1.0/precipitation
  - /api/v1.0/stations
  - /api/v1.0/tobs
  - /api/v1.0/start: TMIN, TAVG, TMAX for all dates greater than or equal to the start date
  - /api/v1.0/start/end: TMIN, TAVG, TMAX for all dates from the start date to the end date, inclusive
