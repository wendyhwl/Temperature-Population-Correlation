"""
* CMPT353 Exercise 4.2: Cities: Temperatures and Density
* June 12, 2020
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# function that calculates the distance between one city and every station
# returns a dataframe of distances from one city to all stations
# Haversine formula from: https://stackoverflow.com/questions/1420045/how-to-find-distance-from-the-latitude-and-longitude-of-two-locations/1422562#1422562
def distance(city, stations):
    # applying the Haversine formula
    radius = 6371  # earth's mean radius = 6371km
    city_lat = city['latitude']          
    city_long = city['longitude']        
    station_lat = stations['latitude']   
    station_long = stations['longitude'] 
    dlat = np.radians(station_lat - city_lat)
    dlong = np.radians(station_long - city_long)
    
    a = (
        np.sin(dlat/2) ** 2 +
        np.cos(np.radians(city_lat)) * np.cos(np.radians(station_lat)) * (np.sin(dlong/2)**2)
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = radius * c
    
    # add distance column to stations
    stations['distance'] = d
    
    return stations

# returns the best value you can find for 'avg_tmax' for that one city from the list of all weather stations
def best_tmax(city, stations):
    # apply distance function, get the min distance index, return its avg_tmax
    df = distance(city, stations)
    closest_station_index = df['distance'].idxmin()
    tmax = df['avg_tmax'].loc[closest_station_index]
    return tmax

# command line takes 3 arg
station_file = sys.argv[1]
city_file = sys.argv[2]
output = sys.argv[3]

# read stations and city files
stations = pd.read_json(station_file, lines=True)
cities = pd.read_csv(city_file)

# divide 'avg_tmax' column by 10
stations['avg_tmax'] = stations['avg_tmax'] / 10

# remove rows with missing values
cities = cities.dropna()

# convert city area from m^2 to km^2, remove cities with area > 10000 km^2
cities['area'] = cities['area'] / 1000000
cities = cities[cities.area <= 10000]

# add population density column
cities['population density'] = cities['population'] / cities['area']

# apply best_tmax function to every row in cities
cities['best_tmax'] = cities.apply(best_tmax, stations=stations, axis=1)

# produce and save the plot
plt.plot(cities['best_tmax'],cities['population density'],'b.')
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)' )
plt.ylabel('Population Density (people/km\u00b2)')
# plt.show() # for testing
plt.savefig(output)