from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


#### custom action Start here:


# action_receive_name
# the chatbot will set the slot "name" to the text it received from user
class ActionReceiveName(Action):

    def name(self) -> Text:
        return "action_receive_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text_received = tracker.latest_message['text']          # use tracker to get the message history from user
        dispatcher.utter_message(text=f"{text_received}, hi nice to meet you")        # say something to user
        
        # return a list of event
        return [SlotSet("name", text_received)]                 # set the slot name

# action_receive_age
# the chatbot will set the slot "age" to the text it received from user
class ActionReceiveAge(Action):

    def name(self) -> Text:
        return "action_receive_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text_received = tracker.latest_message['text']          # use tracker to get the message history from user
        
        age = None
        try: 
           age = int(text_received)
        except ValueError:
            pass
        # return a list of event
        return [SlotSet("age", age)]                 

# action_receive_weight
class ActionReceiveWeight(Action):
    
    def name(self) -> Text:
        return "action_receive_weight"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text_received = tracker.latest_message['text']          # use tracker to get the message history from user
            
        weight = None
        try: 
            weight = float(text_received)
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
           
        height = None
        try: 
            height = float(text_received)
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
            if bmi is not None:     
                return []

            weight = tracker.get_slot("weight")         # get the value in slot "weight"
            height = tracker.get_slot("height")         # get the value in slot "height"
            
            # if weight or height is None, i.e. havent get user's weight or height
            if not weight or not height:
                dispatcher.utter_message(text="I dont have enough information for you BMI now. Sorry.")
            else:
                try:
                    bmi = weight / (height/100)**2
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

# the chatbot will say the name of user when user ask it to do so
class ActionSayAge(Action):

    def name(self) -> Text:
        return "action_say_age"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        age = tracker.get_slot("age")         # get the value in slot "age"
        
        # if age is None, i.e. havent get user's age
        if not age:
            dispatcher.utter_message(text="I dont have your age wor ")
        else:            
            dispatcher.utter_message(text=f"Your age is {age}!")        
        
        # return a list of event
        return []

class ActionSayWeight(Action):

    def name(self) -> Text:
        return "action_say_weight"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        weight = tracker.get_slot("weight")         # get the value in slot "weight"
        
        # if weight is None, i.e. havent get user's weight
        if not weight:
            dispatcher.utter_message(text="I dont have your weight wor ")
        else:            
            dispatcher.utter_message(text=f"Your weight is {weight}!")        
        
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
        
        # if bmi is None, i.e. havent get user's bmi
        if not bmi:
            dispatcher.utter_message(text="I dont have enough information for you BMI now. Sorry.")
        else:            
            dispatcher.utter_message(text=f"Your BMI is {bmi}!")        
        
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
