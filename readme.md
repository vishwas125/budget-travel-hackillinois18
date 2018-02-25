INTRODUCTION
	
        It's always been a hasty problem where to spend when you decide to travel some place, whether to spend more on food and compromise your stay or compromise your stay and get some delicious tasty food or drop both these and decide to stay some good place. Some time it becomes so hard to decide the location as well.
        The Budget Travel application will give you a perfect idea as what might be a good place to visit, which places are good to stay, and the city attractions completely based on your preferences of budget to want to spend for a particular domain such as food or travel or stay.
        We have used Amadeus’ Sandbox APIs, Zomato APIs, Dark Sky Weather API, Sabre API and IATA API. We  gather all the user data and the budget along with preferences such as food, travel or the stay and based on the preference we provide customer  recommendations and suggest the user, top places to visit or top restaurants the user must try, or the best flights based on the budget.
        Built using Flask Framework and Materialize.


REQUIREMENTS
    You will need a machine which has python-3.5+
    installed.
    requirements.txt will install all the required Python libraries.


ARCHITECTURE
    [-] Follows MVC architecture using Flask framework. UI built using Materialize css.


MODULES
    This is a brief description of the Python modules in the source.
    [-] data: 	Logic for fetching data using various APIs.
    [-] place:  Container for each destination being recommended.
    [-] user: 	Model for the user input.


API
	Amadeus API : https://sandbox.amadeus.com/api-catalog
	Dark-sky( weather API) : https://darksky.net/dev
	Sabre API : https://developer.sabre.com/docs/REST_APIs
	Zomato API : https://developers.zomato.com/documentation

