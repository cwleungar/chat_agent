from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher



#### custom action Start here:


# action_receive_name
# the chatbot will set the slot "name" to the text it received from user
class ActionReceiveFirstName(Action):

    def name(self) -> Text:
        return "action_receive_firstname"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        dispatcher.utter_message(text="Pleas give me your first name")        # say something to user
        text_received = tracker.latest_message['text']          # use tracker to get the message history from user

        # return a list of event
        return [SlotSet("first_name", text_received)]                 # set the slot first_name


class ActionReceiveLastName(Action):

    def name(self) -> Text:
        return "action_receive_lastname"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        dispatcher.utter_message(text="Pleas give me your last name")        # say something to user
        text_received = tracker.latest_message['text']                      # use tracker to get the message history from user


        # return a list of event
        return [SlotSet("last_name", text_received)]                 # set the slot last_name


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