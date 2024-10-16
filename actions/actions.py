# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Fallback Policy
from rasa_sdk.events import UserUtteranceReverted

# DO NOT DELETE:For integration of mongodb, and fetching intent-responses back to the chatbot
from pymongo import MongoClient


### DO NOT DELETE: MAIN CODE FETCH SNIPPET FOR MONGODB RESPONSE, 
class ActionFetchDynamicResponse(Action):
    def name(self) -> Text:
        return "action_fetch_dynamic_response"

    def __init__(self):
        # Replace with your actual MongoDB URI
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['admission_chatbot']

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the intent from the user's latest message
        intent = tracker.latest_message['intent']['name']

        # Iterate over all collections in the database
        for collection_name in self.db.list_collection_names():
            collection = self.db[collection_name]

            # Try to find a document that matches the intent
            query = {
                "$or": [
                    {"process": {"$regex": intent, "$options": "i"}},
                    {"course": {"$regex": intent, "$options": "i"}},
                    {"synonyms": {"$regex": intent, "$options": "i"}},
                    {"details": {"$regex": intent, "$options": "i"}}
                ]
            }

            result = collection.find_one(query)

            if result:
                # Format the response based on the collection type
                if collection_name == "courses":
                    response = f"{result['course']} - Tuition: {result['tuition']}"
                elif collection_name == "admission":
                    response = f"Admission Process: {result.get('details', 'No details available.')}"
                
                dispatcher.utter_message(text=response)
                return []

        # If no response was found
        dispatcher.utter_message(text="I'm sorry, I couldn't find the information you're looking for.")
        return []
###




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

# RASA DEFAULT:
# This is a simple example for a custom action which utters "Hello World!"
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