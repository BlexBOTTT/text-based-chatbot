# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import EventType

# DO NOT DELETE:For integration of mongodb, and fetching intent-responses back to the chatbot
from pymongo import MongoClient, errors
import os

############################################################################################################################
############################################################################################################################
### QUERY SEARCHER FUNCTION, DO NOT DELETE
def build_query(intent: str, collection_name: str) -> dict:
    # Define fields to search based on the collection type
    fields = {
        "admission": ["rasa_intent"],
        "courses": ["rasa_intent"],
        "discounts": ["rasa_intent"],
        "general": ["rasa_intent"],
        "tuition_prices": ["rasa_intent", "course", "synonyms"],
        # Add other collections and their respective fields as needed!
    }

    # Construct the query dynamically based on the provided collection name
    if collection_name in fields:
        return {
            "$or": [
                {field: {"$regex": intent, "$options": "i"}} for field in fields[collection_name]
            ]
        }
    # Return an empty query if the collection name is not found
    return {}
### 

### DO NOT DELETE: MAIN ACTION CLASS CODE FETCH RESPONSES FROM MONGODB,
class ActionFetchDynamicResponse(Action):
    def name(self) -> Text:
        # Name of the action used in the Rasa domain
        return "action_fetch_dynamic_response"

    def __init__(self):
        # Initialize MongoDB client and connect to the admission_chatbot database
        try:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
            self.client = MongoClient(mongo_uri)
            self.db = self.client['admission_chatbot']
        except errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            self.db = None  # Gracefully handle failure to connect
            
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if self.db is None:
            dispatcher.utter_message(text="I'm sorry, there was an error connecting to the database.")
            return []

        # Get the latest intent from the user's message
        rasa_intent = tracker.latest_message['intent']['name']

        # debugger print on which intent is selected
        print("Action: AFDR Detected intent:", rasa_intent)

        # Loop through all collections in the database
        for collection_name in self.db.list_collection_names():
            # Fetch the course name from the tracker slot
            collection = self.db[collection_name]

            # Default response if no response fetched from monbodb due to undetected intent
            response = "I'm sorry, I couldn't find the information you're looking for."  

            # Special handling for the 'courses' collection when asking about tuition
            if collection_name == "tuition_prices" and rasa_intent == "ask_tuition_price_specific":
                course_name = tracker.get_slot('course')
                print("Detected course:", course_name)

                # Ensure that the course_name slot is used when available
                if course_name:
                    query = {
                        "course": {"$regex": course_name, "$options": "i"}
                    }
                else:
                    # Fallback to general tuition query if no course name is available
                    query = build_query(rasa_intent, collection_name)

            else: 
                # Use the helper function to build the query, fallback to a broader query
                query = build_query(rasa_intent, collection_name)

            try:
            # Execute the query on the current collection
                result = collection.find_one(query)

                # Check if a result was found
                if result:
                     # Format response based on collection type
                        # then match detected rasa intent
                            # then spits the according utterance to the user
                    if collection_name == "admission":    
                        if rasa_intent == "ask_admission_process":
                            response = result.get('utter_admission_process', 'Admission process not details  available.')
                        if rasa_intent == "ask_admission_requirements":
                            response = result.get('utter_admission_requirements', 'Admission requirements details not available.')
                        if rasa_intent == "ask_admission_online_registration":
                            response = result.get('utter_admission_online_registration', 'Admission online registration details  not available.')
                        if rasa_intent == "ask_admission_transferee_enrollment":
                            response = result.get('utter_admission_transferee_enrollment', 'Admission transferee enrollment details  not available.')
                        if rasa_intent == "ask_admission_working_student":
                            response = result.get('utter_admission_working_student', 'Admission working student details not available.')

                    elif collection_name == "courses":
                        if rasa_intent == "ask_courses_list":
                            response = result.get('utter_course_list', 'Course list details not available.')
                    
                    elif collection_name == "discounts":    
                        if rasa_intent == "ask_available_discounts":
                            response = result.get('utter_discounts', 'Discount details not available.')

                    elif collection_name == "general":
                        if rasa_intent == "ask_school_location":
                            response = result.get('utter_school_location', 'School location not available.')
                        elif rasa_intent == "ask_school_contact":
                            response = result.get('utter_ask_contact', 'School contact details not available.')
                        elif rasa_intent == "ask_chatbot_coverage":
                            response = result.get('utter_chatbot_coverage', 'Chatbot coverage details not available.')
                        elif rasa_intent == "ask_speak_to_staff":
                            response = result.get('utter_speak_to_staff', 'Speak-to-staff details not available.')
                        elif rasa_intent == "ask_why_should_i_enroll":
                            response = result.get('utter_why_should_i_enroll', 'Why-enroll details not available.')
                        else:
                            response = result.get('No general details available.')  
                
                    elif collection_name == "tuition_prices":
                        if rasa_intent == "ask_tuition_price_specific":
                            response = result.get('utter_tuition_price_specific', 'Specific course tuition price not available.')
                        if rasa_intent == "ask_tuition_price_general":
                            response = result.get('utter_tuition_price_general', 'General tuition price not available.')

                    # Send the response back to the user
                    dispatcher.utter_message(text=response)
                    return []
                
            except Exception as e:
                print(f"Error querying collection {collection_name}: {e}")
                continue

        # If no information was found in any collection in the DB, send an apology message
        dispatcher.utter_message(text=response)
        return []
###

############################################################################################################################
############################################################################################################################

# class ActionIterateHelpfulCounter(Action):
#     def name(self) -> str:
#         return "action_iterate_helpful_counter"

#     def __init__(self):
#         # MongoDB connection setup
#         self.client = MongoClient("mongodb://localhost:27017/")
#         self.db = self.client["admission_chatbot"]
#         self.collection = self.db["feedback"]

#         # Triggers if there is no helpful_counter ID in the collection feedback
#         if not self.collection.find_one({"_id": "helpful_counter"}):
#             self.collection.insert_one({"_id": "helpful_counter", "yes_count": 0, "no_count": 0})

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list[EventType]:
#         # Get the user's intent from the latest message
#         user_intent = tracker.latest_message['intent']['name']

#         print("Action: AIHC Detected intent:", user_intent) # debugging line

#         try:
#             # Update counter based on user intent
#             if user_intent == "affirm":
#                 result = self.collection.update_one({"_id": "helpful_counter"}, {"$inc": {"yes_count": 1}})
#                 # print(f"Update result: {result.modified_count}")  # Debugging line
#                 dispatcher.utter_message(text="Thank you for your feedback! Please do continue asking inquiries!")

#             elif user_intent == "deny":
#                 result = self.collection.update_one({"_id": "helpful_counter"}, {"$inc": {"no_count": 1}})
#                 # print(f"Update result: {result.modified_count}")  # Debugging line
#                 dispatcher.utter_message(text="Thank you for letting us know! We'll keep improving.")

#             else:
#                 response = 'no affirm-deny response detected.'

#             # # DEBUG: Fetch the updated document to confirm the count
#             # feedback_counter = self.collection.find_one({"_id": "helpful_counter"})
#             # print(f"Updated document: {feedback_counter}")  # Debugging line

#         except Exception as e:
#             dispatcher.utter_message(text=response)
#             print(f"Error updating feedback counter: {e}")

#         return []

############################################################################################################################
############################################################################################################################
### RASA DEFAULT, do not open:
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