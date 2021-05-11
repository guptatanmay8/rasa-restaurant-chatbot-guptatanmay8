# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
#
#
class ResturantForm(Action):

    def name(self) -> Text:
        return "resturant_form"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict) -> List[EventType]:
        required_slots = ["number","section","time"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                return [SlotSet("requested_slot",slot_name)]
        
        return[SlotSet("requested_slot",None)]

        return []

class Validate_resturant_form(FormValidationAction):

    def name(self) -> Text:
        return "validate_resturant_form"

    def validate_number(self,slot_value: Any , dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict) -> Dict[Text, Any]:

        if type(slot_value) == type(5):
            return {"number": slot_value}
        else:
            dispatcher.utter_message(text="Please enter valid number of seats")
            return {"number":None}


    def validate_section(self,slot_value: Any , dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict) -> Dict[Text, Any]:
        list = ["AC","NON-AC"]
        if slot_value.upper() not in list:
            dispatcher.utter_message(text="Please put a valid section")
            return{"section":None}
        
        else:
            return{"section":slot_value}

    def validate_time(self,slot_value: Any , dispatcher: CollectingDispatcher, tracker: Tracker, domain:Dict) -> Dict[Text, Any]:
        
        hour = int(slot_value[11:13])
        minutes = int(slot_value[14:16])

        if hour>=19 and hour<22:
            final_time = str(hour-12) + ':'
            if minutes>=30:
                final_time+= "30 pm"
            else:
                # minutes=0
                final_time+= "00 pm"
            return{"time":final_time}
        
        else:
            dispatcher.utter_message(text="We are not open at that time. We are only open from 7pm to 10pm")
            return{"time":None}


class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"
    
    def run(self,dispatcher,tracker: Tracker, domain: "DomainDict",) -> List[EventType]:
        dispatcher.utter_message(template="utter_final_details",Num_seats=tracker.get_slot("number"),Section = tracker.get_slot("section"),Time = tracker.get_slot("time"))
        
        
