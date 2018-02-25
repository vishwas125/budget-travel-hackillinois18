

from project.models.data import Travel


class User:
    user_budget = input()
    travel_preference = False
    stay_preference = False
    food_preference = False
    if travel_preference and stay_preference and food_preference:
        travel_budget = user_budget/3
        food_budget = user_budget/3
        stay_budget = user_budget/3
    if travel_preference and stay_preference and (not food_preference):
        travel_budget = user_budget*.40
        stay_preference = user_budget*.40
        food_preference = user_budget*.20
    if travel_preference and (not stay_preference) and food_preference:
        travel_budget = user_budget*.40
        food_budget = user_budget*.20
        stay_budget = user_budget*.40
    if travel_preference and (not stay_preference) and not(food_preference):
        travel_budget = user_budget*.40
        stay_preference = user_budget*.30
        food_preference = user_budget*.30
    if (not travel_preference) and stay_preference and food_preference:
        travel_budget = user_budget*.20
        food_budget = user_budget*.40
        stay_budget = user_budget*.40
    if (not travel_preference) and stay_preference and (not food_preference):
        travel_budget = user_budget*.30
        stay_preference = user_budget*.60
        food_preference = user_budget*.30
    if travel_preference and not(stay_preference) and food_preference:
        travel_budget = user_budget*.40
        food_budget = user_budget*.20
        stay_budget = user_budget*.40
    if (not travel_preference) and (not stay_preference) and (not food_preference):
        travel_budget = user_budget/3
        stay_preference = user_budget/3
        food_preference = user_budget/3


    user1 = Travel.amadeus_api_key
