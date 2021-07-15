# Django_covidtracker

# COVIDTRACKER - COVID-19 Cases Daily Tracker  

## Web-Application built with Django as a backend to daily track COvid 19 cases across India.

## The daily data is provided by the api : `https://api.rootnet.in/`

## To reduce api calls everytime the page reloads, Implemented a function that lets you call the API only once in a day and update the database on a daily basis.  

## In order to clean start, implemnted python script to truncate all data from database and start fresh in case any changes or errors.

## Frameworks/Tools Used:  

1. Django (Backend), Django REST API.
2. HTML, CSS, Bootstrap (Frontend), JavaScript, Jquery (For executing search params)  
3. PostgreSQL Database (For storing all Covid Cases Statewise and District Wise.)

## Application is running live, deployed on Heroku. Link:- `https://sicmunduscovidtracker.herokuapp.com/`

## NOTE: Application best viewed in Desktop View (Currently)
