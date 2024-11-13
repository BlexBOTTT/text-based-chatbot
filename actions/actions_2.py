# actions_2.py
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from pymongo import MongoClient

class ActionIterateHelpfulCounter(Action):
    def name(self) -> str:
        return "action_iterate_helpful_counter"

    def __init__(self):
        # MongoDB connection setup
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["admission_chatbot"]
        self.collection = self.db["feedback"]

    def run(self, dispatcher, tracker, domain):
        # Get the user's intent from the latest message
        user_intent = tracker.latest_message['intent']['name']

        # Retrieve the counter document
        feedback_counter = self.collection.find_one({"_id": "helpful_counter"})

        if user_intent == "affirm":
            # Increment "yes_count" if the intent is "affirm"
            self.collection.update_one({"_id": "helpful_counter"}, {"$inc": {"yes_count": 1}})
            dispatcher.utter_message(text="Thank you for your feedback!")
        elif user_intent == "deny":
            # Increment "no_count" if the intent is "deny"
            self.collection.update_one({"_id": "helpful_counter"}, {"$inc": {"no_count": 1}})
            dispatcher.utter_message(text="Thank you for letting us know! We'll keep improving.")

        return []