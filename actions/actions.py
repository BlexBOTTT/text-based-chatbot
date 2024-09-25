# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Fallback Policy
from rasa_sdk.events import UserUtteranceReverted
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

### Custom action for dynamic tuition prices

### Example tuition data
tuition_data = {
    "computer science": 2000,
    "education": 1500,
    "hospitality management": 1800,
    "business administration": 1600,
    "engineering": 2200,
    "psychology": 1700,
    "nursing": 1900,
}

class ActionAskTuition(Action):
    def name(self) -> Text:
        return "action_ask_tuition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course = tracker.get_slot("course").lower()
        tuition = tuition_data.get(course, "not available")
        
        if tuition != "not available":
            message = f"The tuition fee for {course.title()} is ${tuition}."
        else:
            message = f"I'm sorry, I don't have information on the tuition for {course.title()}."
        
        dispatcher.utter_message(text=message)
        return []



### Default fallback response for inputs with unrecognized intents (not trained)
# class ActionDefaultFallback(Action):
#     def name(self) -> str:
#         return "action_default_fallback"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):
#         dispatcher.utter_message(text="Sorry, I didn't understand that. Can you rephrase?")
#         return [UserUtteranceReverted()]