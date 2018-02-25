# -*- coding: utf-8 -*-
import configparser
from flask import flash
import json
from project.models.user import User
from geopy.geocoders import Nominatim
from project.models.place import Place


import requests


class Travel:
    #Config = configparser.ConfigParser()
   # Config.read('../config/budget-travel.ini')
    amadeus_api_key ="BlGWrRe3OITosh4PSlzRAlZ4leqVcDBx"
    sabre_api_key = "T1RLAQLsP5dQOGPAzMdYySsn9hJaydxFXBDq57tdrzd/sZTzmi5gbRfCAADAo34GsJPXi/Dc7kJCArqfZb76MniUeGCJKQl/if2963wSXCUdP/sUPe3Z+rcGg9o32T1gZPI72SC0yZHsacsyFuyrrnYuOAJLCWXbV93s5aSTxGQpRxTtT4VCdL2RXtc4PYir2lYb6Izure28f/35YFhAhqsg9aDD3/shss8XV3ApicoO2nlZVL+KlAPfEAj+XhrgErQPsupE+8G5HaiO0cmeI46qcsJL205/DpW6R/JNHFMTx8li6F0v1QIVWoHi"
    zomato_api_key = "f52bbd60b69b3c43538a06bd0baa8092"
    dark_weather_api_key = "1dfe7f5d2677572e44cdaa05ab9f2bd4"
    iata_key = "a79b4c25-2e79-4c4b-8162-a60748437324"
    # amadeus_api_key = Config['Main']['amadeus_api_key']
    # sabre_api_key = Config['Main']['sabre_api_key']
    # zomato_api_key = Config['Main']['zomato_api_key']
    # dark_weather_api_key = Config['Main']['dark_weather_api_key']
    # iata_key = Config['Main']['iata_key']
    geolocator = Nominatim()

    def __init__(self,person):
        self__user = person;

    def get_local_location(self):
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        return lat, lon

    def get_top_destination(self,iata_code):
        url = "https://api.test.sabre.com/v1/lists/top/destinations?origin=" + iata_code + "&destinationtype=domestic&departuredate=" + str(User.start_date) + "&returndate=" + str(User.return_date) + "&topdestinations=6"
        data = {}
        response = requests.get(url, data=data,
                                headers={"Content-Type": "application/json", "Authorization": "Bearer " + self.sabre_api_key})
        city_list = []
        data_source = json.loads(response.text)
        for x in data_source["Destinations"]:
            if x['Destination']['Type'] == "City":
                city_list.append(x['Destination']['DestinationLocation'])
        return city_list

    def get_city_name_from_iata_code(self,iata_code):
        api_key = "ly2CUlEFKqpnoYUil71sAZmaQWTHt8bW"
        url = "https://api.sandbox.amadeus.com/v1.2/location/" + iata_code + "/?apikey=" + api_key
        data = {}
        response = requests.get(url, data=data, headers={"Content-Type": "application/json"})
        json_obj = json.loads(response.text)
        return json_obj['city']['name']

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


    def get_flights(self):
        check_in = str(User.start_date)
        check_out = str(User.return_date)
        latlong = self.get_lat_long(str(User.origin_city))
        iata_code = self.get_iata_code_city(latlong.latitude,latlong.longitude)
        budget = User.user_budget
        dates = str(check_in + "--" + check_out)
        url = "https://api.sandbox.amadeus.com/v1.2/flights/inspiration-search?origin=" + iata_code  + "&departure_date=" + str(User.start_date) + "&max_price=" + str(
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
        url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' + citycode + '&entity_type=city&establishment&count=5&type=101&sort=rating'
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

    def get_lat_long(self, city_name):
        return self.geolocator.geocode(city_name)

    def get_weatherdata(self, city_name):
        # date : YYYY-MM-DD
        latlong = self.get_lat_long(city_name)
        lat = latlong.latitude
        long = latlong.longitude
        date = User.start_date
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
        #weather_list.append(data_source["daily"]["data"][0]['precipType'])
        return weather_list


    def get_hotels(self):
        checkin = str(User.start_date)
        checkout = str(User.return_date)
        loc = self.get_local_location()
        airport_iata_code = self.get_iata_code_airport(loc[0], loc[1])
        url = "https://api.sandbox.amadeus.com/v1.2/hotels/search-airport?location=" + airport_iata_code + "&number_of_results=5&check_in=" + str(
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

    def travel_start(self):
        places=[]
        latlong = self.get_lat_long(User.origin_city)
        iata = self.get_iata_code_city(latlong.latitude,latlong.longitude)
        destination_list =  self.get_top_destination(iata)
        for destination_city in destination_list:
            place = Place(destination_city)
            city_name = self.get_city_name_from_iata_code(destination_city)
            place.destination=city_name
            place.attractions_list = self.get_attractions(city_name)
            place.flights = self.get_flights()
            place.hotels_list = self.get_hotels()
            place.weather = self.get_weatherdata(city_name)
            place.restaurants_list = self.get_restaurants(str(self.get_zomato_city_id(city_name)))
            places.append(place)
        
        return places


