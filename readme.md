INTRO
	
The budget is the most important factor while planning or taking any trip. How much money we're going to spend on things like food, accomodation, travel, recreation etc are major factors our budget is going to depend on. To address the priorities and utilize the existing data and services, we bring to you the budget travel buddy application. 

Built at hackillinois 2018, this application uses data from various sources: mainly Amadeus’ Sandbox APIs, Zomato APIs, Dark Sky Weather API, Sabre API and IATA API.

 The user enters his source and budget along with priorities for food/accomodation/travel and the application gets the best possible results for various places the user can go to, along with customized suggestions for restaurants, hotels and flights/trains, fulfilling user's priorities.     


REQUIREMENTS

You will need a machine which has python-3.5+ installed.
The requirements.txt will install all the required Python libraries.
    


ARCHITECTURE

Follows MVC architecture using Flask framework. UI built using Materialize css.
     


MODULES

 This is a brief description of the Python modules in the source.
    [-] data: 	Logic for fetching data using various APIs.
    [-] place:  Container for each destination being recommended.
    [-] user: 	Model for the user input.   


APIs

Amadeus API : https://sandbox.amadeus.com/api-catalog
Dark-sky( weather API) : https://darksky.net/dev
Sabre API : https://developer.sabre.com/docs/REST_APIs
Zomato API : https://developers.zomato.com/documentation
IATA Codes: http://iatacodes.org/


