# -*- coding: utf-8 -*-
from flask import flash
import urllib.request
import requests
from datetime import datetime
import random
import json
import configparser


class Travel:
    Config = configparser.ConfigParser()
    Config.read('../config/budget-travel.ini')
    amadeus_api_key = Config['Main']['amadeus_api_key']
    sabre_api_key = Config['Main']['sabre_api_key']
    zomato_api_key = Config['Main']['zomato_api_key']
    dark_weather_api_key = Config['Main']['dark_weather_api_key']
    iata_key = Config['Main']['iata_key']

    def __init__(self, origin_city, start_date, return_date):
        self.origin_city = origin_city
        self.start_date = start_date
        self.return_date = return_date


    def get_local_location(self):
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        return lat, lon

    def get_top_destination(self, origin_city, departure_date, return_date):
        url = "https://api.test.sabre.com/v1/lists/top/destinations?origin=" + origin_city + "&destinationtype=domestic&departuredate=" + departure_date + "&returndate=" + return_date + "&topdestinations=6"
        data = {}
        response = requests.get(url, data=data,
                                headers={"Content-Type": "application/json", "Authorization": "Bearer " + self.sabre_api_key})
        city_list = []
        data_source = json.loads(response.text)
        for x in data_source["Destinations"]:
            if x['Destination']['Type'] == "City":
                city_list.append(x['Destination']['DestinationLocation'])
        return city_list

    def get_iata_code_city(self, lat, lon):
        url = "https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?latitude=" + str(lat) + "&longitude=" + str(
            lon) + "&apikey=" + self.amadeus_api_key
        req = requests.get(url)
        if req.status_code == 200:
            # rawData = req.json()
            print('Success')
        else:
            print(req.status_code)
            print("Fail")
        return req.json()[0]['city']

    def get_iata_code_airport(self, lat, lon):
        url = "https://api.sandbox.amadeus.com/v1.2/airports/nearest-relevant?latitude=" + str(lat) + "&longitude=" + str(
            lon) + "&apikey=" + self.amadeus_api_key
        req = requests.get(url)
        if req.status_code == 200:
            # rawData = req.json()
            print('Success')
        else:
            print(req.status_code)
            print("Fail")
        return req.json()[0]['airport']


    def get_flights(self, budget, check_in, check_out, city):
        dates = str(check_in + "--" + check_out)
        url = "https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin=" + city + "&departure_date=" + dates + "&max_price=" + str(
            budget) + "&apikey=" + self.amadeus_api_key
        req = requests.get(url)
        result = (req.json())
        with open("req.json", "w", encoding="utf-8") as sam:
            json.dump(result, sam)
        data = json.load(open('req.json'))
        finalTopFive = []
        destData = data['results']
        topFiveDest = ['MSP']
        for itm in destData:
            for key, value in itm.items():
                if value in topFiveDest:
                    finalTopFive.append(itm)
        # print(finalTopFive)
        if req.status_code == 200:
            # rawData = req.json()
            print('Success')
        else:
            print(req.status_code)
            print("Fail")
        return finalTopFive

    def get_zomato_city_id(self, city_name):
        url = 'https://developers.zomato.com/api/v2.1/cities?q=' + city_name
        data = '{"id": "id","name": "name","country_id": "country_id","country_name": "country_name","is_state": "","state_id": "","state_name": "","state_code": ""}'
        response = requests.get(url, data=data, headers={"Content-Type": "application/json",
                                                         "user-key": self.zomato_api_key})
        if response.status_code == 200:
            print('Success')
        else:
            print(response.status_code)
            print("Fail")
        data_source = json.loads(response.text)
        return data_source['location_suggestions'][0]['id']


    def get_restaurants(self, citycode):
        url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' + citycode + '&entity_type=city&establishment_type=101&sort=rating'
        data = {}
        restaurant_list = []
        response = requests.get(url, data=data, headers={"Content-Type": "application/json",
                                                         "user-key": self.zomato_api_key})

        data_source = json.loads(response.text)
        if response.status_code == 200:
            print('Success')
        else:
            print(response.status_code)
            print("Fail")
        for x in data_source['restaurants']:
            restaurant_list.append(x['restaurant']['name'])
            restaurant_list.append(x['restaurant']['location']['address'])
            restaurant_list.append(x['restaurant']['user_rating']['aggregate_rating'])
            restaurant_list.append(x['restaurant']['featured_image'])
        return restaurant_list

    def get_weatherdata(self, date, lat, long):
        # date : YYYY-MM-DD
        year = date[:4]
        month = date[5:7]
        year = int(year) - 1
        day = date[8:10]
        if int(day) < 15:
            day = "01"
        else:
            day = "15"
        date = str(year) + "-" + month + "-" + day
        url = "https://api.darksky.net/forecast/" + self.dark_weather_api_key + "/" + str(lat) + "," + str(
            long) + "," + date + "T12:30:00"
        data = {}
        weather_list = []
        response = requests.get(url, data=data, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            print('Success')
        else:
            print(response.status_code)
            print("Fail")
        data_source = json.loads(response.text)
        weather_list.append(data_source["daily"]["data"][0]['temperatureHigh'])
        weather_list.append(data_source["daily"]["data"][0]['temperatureLow'])
        weather_list.append(data_source["daily"]["data"][0]['humidity'])
        weather_list.append(data_source["daily"]["data"][0]['precipType'])
        return weather_list


    def get_hotels(self, checkin, checkout):
        loc = self.get_local_location()
        airport_iata_code = self.get_iata_code_airport(loc[0], loc[1])
        url = "https://api.sandbox.amadeus.com/v1.2/hotels/search-airport?location=" + airport_iata_code + "&check_in=" + str(
            checkin) + "&check_out=" + str(checkout) + "&apikey=" + self.amadeus_api_key
        req = requests.get(url)
        result = (req.json())
        with open("hotel_data.json", "w", encoding="utf-8") as hotel:
            json.dump(result, hotel)
        data = json.load(open('hotel_data.json'))
        hotel_details = []
        for x in data["results"]:
            hotel_details.append(x["property_name"])
            hotel_details.append(x["address"])
            hotel_details.append(x["total_price"]["amount"])
        return hotel_details
        if req.status_code == 200:
            # rawData = req.json()
            print('Success')
        else:
            print(req.status_code)
            print("Fail")


    def get_attractions(self, city):
        url = "https://api.sandbox.amadeus.com/v1.2/points-of-interest/yapq-search-text?city_name=" + city + "&apikey=" + self.amadeus_api_key
        data = {}
        response = requests.get(url, data=data, headers={"Content-Type": "application/json"})
        attractions_list = []
        json_obj = json.loads(response.text)
        for x in json_obj['points_of_interest']:
            attractions_list.append(x['title'])

        if response.status_code == 200:
            print('Success')
        else:
            print(response.status_code)
            print("Fail")
        return attractions_list

travel = Travel("Chicago","2018-03-23", "2018-03-30");
travel.get_flights("500","2018-03-23", "2018-03-30", "CHI")
#travel.get_attractions("Chicago")