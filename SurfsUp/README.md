# # sqlalchemy-challenge
## # Climate analysis in Honolulu
# Challenge details
# References
# Part 1 - climate_starter.ipynb
# Part 2 - app.py

In this two-part challenge I use Python and SQLAlchemy to do a basic climate analysis and data exploration of  climate database for weather in Honolulu Hawaii using
- SQL ALchemy
- Pandas
- Matplotlib

In the second part of this challenge I create a Flask API with the ability to query data sourced in part 1 using the API SQLite connection.

# # acknowledgements_and_references

<!-- The following resource https://stackoverflow.com/questions/16728904/sqlalchemy-count-of-distinct-over-multiple-columns was used to assist in creating the following code snippet
'
'
'session.query(func.count(distinct(Measurement.station))).all()
'
'
The above assisted to correct incorrect syntax for func.count(distinct(variable)) request.

<!-- The following resource https://www.geeksforgeeks.org/python-datetime-strptime-function/ was used to assist in creating the following code snippet
'
'station_temps = session.query(*sel).\
'filter(func.strftime(Measurement.date) >= start_date, Measurement.station == 'USC00519281').\
'
'
The above assisted to correct my original code with no strftime originally. 

<!-- The following resource: ChatGPT was used to assist in creating the following code snippet
'
' precipitation_dates = []
' precipitation_totals = []
'
'    for date, dailytotal in precipitation:
'        precipitation_dates.append(date)
'        precipitation_totals.append(dailytotal)
'
'    precipitation_dict = dict(zip(precipitation_dates, precipitation_totals))
'
'   return jsonify(precipitation_dict)
'
'
'
The above assisted to  correct syntax, add in 'zip' and asist to create a dictionary.