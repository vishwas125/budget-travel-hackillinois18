
class User:
    user_budget = ""
    travel_budget, food_budget, stay_budget = 500, 100, 400
    travel_preference = False
    stay_preference = False
    food_preference = False
    origin_city = ""
    start_date = ""
    return_date = ""

    def __init__(self, origin_city, start_date, return_date, user_budget):
        self.origin_city = origin_city
        self.start_date = start_date
        self.return_date = return_date
        self.user_budget = user_budget
        #self.travel_preference=travel_preference
        #self.categorize_budget(user_budget,travel_preference, stay_preference, food_preferenc)

    def categorize_budget(self, user_budget, travel_preference, stay_preference, food_preference):
        if travel_preference and stay_preference and food_preference:
            self.travel_budget = user_budget/3
            self.food_budget = user_budget/3
            self. stay_budget = user_budget/3
        if travel_preference and stay_preference and (not food_preference):
            self.travel_budget = user_budget*.40
            self.stay_budget = user_budget*.40
            self.food_budget = user_budget*.20
        if travel_preference and (not stay_preference) and food_preference:
            self.travel_budget = user_budget*.40
            self.food_budget = user_budget*.20
            self.stay_budget = user_budget*.40
        if travel_preference and (not stay_preference) and not food_preference:
            self.travel_budget = user_budget*.40
            self.stay_budget = user_budget*.30
            self.food_budget = user_budget*.30
        if (not travel_preference) and stay_preference and food_preference:
            self.travel_budget = user_budget*.20
            self.food_budget = user_budget*.40
            self.stay_budget = user_budget*.40
        if (not travel_preference) and stay_preference and (not food_preference):
            self.travel_budget = user_budget*.30
            self.stay_budget = user_budget*.60
            self.food_budget = user_budget*.30
        if travel_preference and not stay_preference and food_preference:
            self.travel_budget = user_budget*.40
            self.food_budget = user_budget*.20
            self.stay_budget = user_budget*.40
        if (not travel_preference) and (not stay_preference) and (not food_preference):
            self.travel_budget =  user_budget/3
            self.stay_budget = user_budget/3
            self.food_budget = user_budget/3

        return self.user_budget

