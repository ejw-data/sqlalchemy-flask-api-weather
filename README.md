# sqlalchemy-flask-api-weather  

Author:  Erin James Wills, ejw.data@gmail.com 

![Weather API](./images/weather-api.png)
<cite>Photo by [NASA](https://unsplash.com/@nasa?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/weather?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)</cite>  

<br>

## Overview  
<hr>

This repo uses data contained in an SQLite file and SQLAlchemy to obtain data for 1) an analysis of Hawaii weather (Jupyter Notebook) and 2) Flask api that provides the weather data via 5 different routes.

<br>

## Technologies
* Python
* Pandas
* SQLAlchemy

<br>

## Data Source
Dataset generated by Trilogy Education Services. Origins beyond this is unknown. 

<br>

## Setup and Installation  
1. Environment needs the following:  
    * Python 3.6+
    * pandas
    * flask
    * sqlalchemy.ext.automap
    * sqlalchemy.orm
    * datetime
    * numpy
1. Activate your environment
1. Clone the repo to your local machine
1. Start Jupyter Notebook within the environment from the repo
1. Run `climate_analysis.ipynb` to test connections and queries
1. To run the flask app:
    *  In terminal, navigate to the top-level repo folder
    *  Activate your environment
    *  In terminal run:  `python app.py`
    *  The routes that can be used are listed on the page.

<br>
