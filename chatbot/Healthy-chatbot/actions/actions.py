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
            return [SlotSet("weight", None), SlotSet("duration", None)]            # set the slot be None
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
        return [SlotSet("weight", weight), SlotSet("duration", None)]
  
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
            return [SlotSet("height", None), SlotSet("duration", None)]            # set the slot be None
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
        return [SlotSet("height", height), SlotSet("duration", None)]


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

#----------------------------------------------------------------------------
#York's sport action
#Input sport, duration, unit then update activity level

sport_intensity = {
    'football': 8,
    'soccer' : 8,
    'cricket': 4,
    'field Hockey': 8,
    'tennis': 8,
    'volleyball': 6,
    'table Tennis': 4,
    'basketball': 8,
    'baseball': 4,
    'american Football': 8,
    'rugby': 8,
    'boxing': 10,
    'ice Hockey': 8,
    'swimming': 6, #[3,10], #depending on stroke and intensity
    'swim': 6, #[3,10], #depending on stroke and intensity
    'athletics': 6, #[3,10], #depending on event
    'gymnastics': 4,
    'golf': 4,
    'horse Racing': 6,
    'auto Racing': 2, #although it requires mental focus and quick reflexes
    'cycling': 6, #[3,10], #depending on intensity and terrain
    'badminton': 6
}

MIN = ["min", "mins", "m"]  #For determine the unit

heathylevel = 600  #Suggested activity level per week #activity level = intensity*mins

class AnalyisSport(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_analyis_sport"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        activitylevel = float(tracker.get_slot("activitylevel"))
        sport = next(tracker.get_latest_entity_values("sport"), None)
        if not sport:
            sport = tracker.get_slot("sport")
        duration = next(tracker.get_latest_entity_values("duration"), None)
        unit = next(tracker.get_latest_entity_values("unit"), None)

        #update durationInMin only when user provide both unit and duration
        #Get the duration slot if not
        #only unit do nothing
        if (unit and duration):
            try:
                durationInMin = float(duration)
                if unit.lower() not in MIN: #unit hour
                    durationInMin *= 60
            except:
                durationInMin = None

        if not duration:
            duration = tracker.get_slot("duration")
            try:
                durationInMin = float(duration)
            except:
                durationInMin = None

        #Find intensity
        if sport:
            sport = sport.lower()
            intensity = sport_intensity.get(sport, None)
        else:
            intensity = None

        
        if (intensity and durationInMin):
            activitylevel += durationInMin*intensity
            msg = f"Your activity level this week is {activitylevel} out of {heathylevel}"
            dispatcher.utter_message(text=msg)
            if activitylevel > heathylevel:
                msg = f"You have done enough exercise this week"
            else:
                msg = f"You should exercise more this week"
            dispatcher.utter_message(text=msg)
            #update activitylevel if requirment fulfiled and delete sport and duration slot
            return [SlotSet("activitylevel", activitylevel), SlotSet("sport", None), SlotSet("duration", None)]

        elif intensity: #Only sport
            msg = f"I like {sport} as well. It has an intensity level of {intensity} out of 10"
            dispatcher.utter_message(text=msg)
            msg = f"You play {sport} for how long?"
            dispatcher.utter_message(text=msg)
            return [SlotSet("sport", sport)]

        elif (durationInMin): #Only duration
            msg = f"What sport did you play?"
            dispatcher.utter_message(text=msg)
            return [SlotSet("duration", durationInMin)]

        else: #not intensity and not durationInMin
            msg = "I didn't recognize the sport. Are you sure it's spelled correctly?"
            dispatcher.utter_message(text=msg)
            return []

#Return activity level to user
class ActivityLevel(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_activitylevel"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        try:
            activitylevel = float(tracker.get_slot("activitylevel"))
        except:
            activitylevel = 0.0
        msg = f"Your activity level this week is {activitylevel} out of {heathylevel}"
        dispatcher.utter_message(text=msg)
        if activitylevel > heathylevel:
            msg = f"You have done enough exercise this week"
        else:
            msg = f"You need to do more exercise this week"
        dispatcher.utter_message(text=msg)
        return []

#end of York's sport action
#----------------------------------------------------------------------------