from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import re

#### custom action Start here:

# action_receive_weight
class ActionReceiveWeight(Action):
    
    def name(self) -> Text:
        return "action_receive_weight"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text_received = tracker.latest_message['text']          # use tracker to get the message history from user

        # use regex to extract the weight number from the text 
        res = re.search("(\d{2,3})\s?(kg|lb)?", text_received, re.IGNORECASE)
        weight = None        
        # if no matching
        if not res:
            return [SlotSet("weight", None)]            # set the slot be None
        else:
            # get if it is kg or lb
            unit = res.group(2)
            if not unit and unit == "lb":       # if unit is None or lb
                try:
                    weight = float(res.group(1)) * 0.45359237       # convert lb to kg
                except ValueError:
                    pass
            else:
                # we assume if no unit is given, it is kg here
                try:
                    weight = float(res.group(1))
                except ValueError:
                    pass
            
        # return a list of event
        return [SlotSet("weight", weight)]
  
# action_receive_height
class ActionReceiveHeight(Action):
        
    def name(self) -> Text:
        return "action_receive_height"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        text_received = tracker.latest_message['text']          # use tracker to get the message history from user
        # use regex to extract the weight number from the text 
        res = re.search("([12]\.?\d{2})\s?(m|cm)?", text_received, re.IGNORECASE)
        height = None
        if not res: # if no matching
            return [SlotSet("height", None)]            # set the slot be None
        else:
            # get if it is m or cm
            unit = res.group(2)
            if not unit and unit == "cm":       # if unit is None or cm
                try:
                    height = float(res.group(1)) * 0.01       # convert cm to m
                except ValueError:
                    pass
            else:
                try:
                    height = float(res.group(1))
                    # i guess no one can taller than 5m (?)
                    if height > 5:      # if height is greater 5, we assume the unit is cm here
                        height *= 0.01              # conver cm to m
                except ValueError:
                    pass

        # return a list of event
        return [SlotSet("height", height)]


# calculate BMI based on weight and height slots
class ActionCalculateBmi(Action):
    
        def name(self) -> Text:
            return "action_calculate_bmi"
    
        def run(self, dispatcher: CollectingDispatcher,
                tracker: Tracker,
                domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    
            bmi = tracker.get_slot("bmi")         # get the value in slot "bmi"
            if bmi is not None:                 # if already has bmi, no need to calculate again   
                return []

            weight = tracker.get_slot("weight")         # get the value in slot "weight"
            height = tracker.get_slot("height")         # get the value in slot "height"
            
            # if weight or height is None, i.e. havent get user's weight or height
            if not weight or not height:
                dispatcher.utter_message(text="I dont have enough information for you BMI now. Sorry.")
            else:
                dispatcher.utter_message(text=f"Your weight is {weight} kg and your height is {height} m. Let me calculate your BMI...")
                try:
                    bmi = weight / height**2
                    dispatcher.utter_message(text=f"Your BMI is {bmi}!")        
                except:
                    dispatcher.utter_message(text="Error calculating your BMI. Sorry.")
                
            # return a list of event
            return [SlotSet("bmi", bmi)]


## Users asking the bot whether it know his/her some information
# action_say_name
# the chatbot will say the name of user when user ask it to do so
class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")         # get the value in slot "name"
        
        # if name is None, i.e. havent get user's name
        if not name:
            dispatcher.utter_message(text="I dont have your name wor ")
        else:            
            dispatcher.utter_message(text=f"Your name is {name}!")        
        
        # return a list of event
        return []

# action_say_weight
class ActionSayWeight(Action):

    def name(self) -> Text:
        return "action_say_weight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weight = tracker.get_slot("weight")         # get the value in slot "weight"
        
        # if weight is None, i.e. havent get user's weight
        if not weight:
            dispatcher.utter_message(text="Something went wrong to get your weight. Sorry")
        else:            
            dispatcher.utter_message(text=f"I remember your weight is {weight}kg!")        
        
        # return a list of event
        return []

# action_say_height
class ActionSayHeight(Action):

    def name(self) -> Text:
        return "action_say_height"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        height = tracker.get_slot("height")         # get the value in slot "height"
        
        # if height is None, i.e. havent get user's height
        if not height:
            dispatcher.utter_message(text="Something went wrong to get your height. Sorry")
        else:            
            dispatcher.utter_message(text=f"I remember your height is {height}m!")        
        
        # return a list of event
        return []

# action_say_bmi
class ActionSayBmi(Action):

    def name(self) -> Text:
        return "action_say_bmi"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bmi = tracker.get_slot("bmi")         # get the value in slot "bmi"
        
        bmi_health_range = {
                18.5: "You are unerweight. Please eat more!",
                24.9: "You are normal weight. Keep it up!",
                29.9: "You are overweight. Please exercise more!",
                34.9: "You are obese. Please exercise more!",
                39.9: "You are severely obese. Please exercise more!!!",
                40: "You are extremely fat. Get out of your room and exercise right now !!!!!"
        }

        # if bmi is None, i.e. havent get user's bmi
        if not bmi:
            dispatcher.utter_message(text="I dont have enough information for you BMI now. Sorry.")
        else:     
            dispatcher.utter_message(text=f"Your BMI is {bmi:.3g}!")        
            # say some comment to the user based on the bmi
            if bmi < 18.5:
                dispatcher.utter_message(text=bmi_health_range[18.5])
            elif bmi < 24.9:
                dispatcher.utter_message(text=bmi_health_range[24.9])
            elif bmi < 29.9:
                dispatcher.utter_message(text=bmi_health_range[29.9])
            elif bmi < 34.9:
                dispatcher.utter_message(text=bmi_health_range[34.9])
            elif bmi < 39.9:
                dispatcher.utter_message(text=bmi_health_range[39.9])
            else:
                dispatcher.utter_message(text=bmi_health_range[40])

        # return a list of event
        return []



# Ng Ho's API request
import requests
import json

class ActionCheckFood(Action):

    def name(self) -> Text:
        return "action_check_food"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        target_food = next(tracker.get_latest_entity_values("food"), None)

        if not target_food:
            msg = "The bot cannot detect what food you ate!"
            dispatcher.utter_message(text = msg)
            return []
        
        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"

        APP_ID = "9079dd12"
        APP_KEY = "d17f3427e78f76417e83f3f646219267"

        headers = { "x-app-id": APP_ID,
                    "x-app-key": APP_KEY
                    }
        
        body = {"query": f"100g of {target_food}"}

        data = requests.post(url, headers = headers, json = body)

        status = data.status_code

        nutritionValue = data.json()

        if status != 200:
            msg = f"Error code: {status}"
            dispatcher.utter_message(text = msg)
            return []

        msg = f"Here are the nutrition value of {target_food}:"

        listHolder = nutritionValue['foods']
        realDict = listHolder[0]

        msg += "\nCalories: " + str(realDict.get("nf_calories"))
        msg += "\nTotal fat: " + str(realDict.get("nf_total_fat"))
        msg += "\nSaturated fat: " + str(realDict.get("nf_saturated_fat"))
        msg += "\nCholesterol: " + str(realDict.get("nf_cholesterol"))
        msg += "\nSodium: " + str(realDict.get("nf_sodium"))
        msg += "\nCarbohydrates: " + str(realDict.get("nf_total_carbohydrate"))
        msg += "\nDietary fiber: " + str(realDict.get("nf_dietary_fiber"))
        msg += "\nSugars: " + str(realDict.get("nf_sugars"))
        msg += "\nProtein: " + str(realDict.get("nf_protein"))
        msg += "\nPotassium: " + str(realDict.get("nf_potassium"))

        dispatcher.utter_message(text = msg)
        return []
