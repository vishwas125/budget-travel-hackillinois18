# -*- coding: utf-8 -*-
from flask import flash
import urllib.request
import requests
from datetime import datetime
import random
import json
import ssl
from iata_codes import IATACodesClient

if hasattr(ssl, '_create_unverified_context'):
      ssl._create_default_https_context = ssl._create_unverified_context


amadeus_key="a1nd6o3QzlTCjQTtmEDUt4TBKoeGSm55"
iata_key="a79b4c25-2e79-4c4b-8162-a60748437324"

def get_local_location():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat,lon



def get_iata_code_city(lat,lon):
    url="https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?latitude="+str(lat)+"&longitude="+str(lon)+"&apikey="+amadeus_key
    req = requests.get(url)
    return req.json()[0]['city']

def get_iata_code_airport(lat,lon):
    url="https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?latitude="+str(lat)+"&longitude="+str(lon)+"&apikey="+amadeus_key
    req = requests.get(url)
    return req.json()[0]['airport']



def get_flights(budget):

    loc=get_local_location()
    city=get_iata_code_city(loc[0],loc[1])
    url="https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin="+city+"&max_price="+str(budget)+"&apikey="+amadeus_key
    req = requests.get(url)
    
    if req.status_code == 200:    
        #rawData = req.json()
        print('Success')
        
                
    else:
        print(req.status_code)
        print("Fail")


def get_hotels(checkin,checkout):

    loc=get_local_location()
    airport_iata_code=get_iata_code_airport(loc[0],loc[1])
    url="https://api.sandbox.amadeus.com/v1.2/hotels/search-airport?location="+airport_iata_code+"&check_in="+str(checkin)+"&check_out="+str(checkout)+"&apikey="+amadeus_key
    req = requests.get(url)
    
    if req.status_code == 200:    
        #rawData = req.json()
        print('Success')
        
                
    else:
        print(req.status_code)
        print("Fail")


#get_flights(500)

#get_hotels("2018-02-25","2018-02-28")