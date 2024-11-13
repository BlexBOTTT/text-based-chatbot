# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

#
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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
        # Add other collections and their respective fields as needed, MANUALLY!
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
        intent = tracker.latest_message['intent']['name']

        # debugger print on which intent is selected
        print("Detected intent:", intent)

        # Loop through all collections in the database
        for collection_name in self.db.list_collection_names():
            # Fetch the course name from the tracker slot
            collection = self.db[collection_name]

            # Special handling for the 'courses' collection when asking about tuition
            if collection_name == "tuition_prices" and intent == "ask_tuition_specific":
                # Fetch the course slot value from the data/nlu/tuition.yml
                course_name = tracker.get_slot('course')  
            
                print("detected course:", course_name)

                 # Use the course_name in the query if it's available
                if course_name:
                    query = {
                        "course": {"$regex": course_name, "$options": "i"}
                    }
                else:
                    # If no course name is available, fallback to a broader query
                    query = build_query(intent, collection_name)
            else: 
                # Use the helper function to build the query, fallback to a broader query
                query = build_query(intent, collection_name)

            try:
            # Execute the query on the current collection
                result = collection.find_one(query)

                # Check if a result was found
                if result:
                # Format response based on collection type

                    if collection_name == "admission":    
                        response = f"{result.get('utter_admission', 'No details available.')}"

                    elif collection_name == "courses":
                        response = f"{result.get('utter_course_list', 'No details available.')}"
                    
                    elif collection_name == "discounts":    
                        response = f"{result.get('utter_discounts', 'No details available.')}"

                    elif collection_name == "general":
                        if intent == "ask_school_location":
                            response = result.get('utter_school_location', 'Location details not available.')
                        elif intent == "ask_contact":
                            response = result.get('utter_ask_contact', 'Contact details not available.')
                        else:
                            response = result.get('No general details available.')  

                    elif collection_name == "tuition_prices":
                        response = result.get('utter_tuition_price_specific', 'No tuition available.')
                        if intent == "ask_tuition_general":
                            response = result.get('utter_tuition_price_general', 'No tuition available.')


                    # Send the response back to the user
                    dispatcher.utter_message(text=response)
                    return []
                
            except Exception as e:
                print(f"Error querying collection {collection_name}: {e}")
                continue

        # If no information was found in any collection in the DB, send an apology message
        dispatcher.utter_message(text="LAST I'm sorry, I couldn't find the information you're looking for.")
        return []
###

############################################################################################################################
############################################################################################################################

# action_feedback_counter is in actions_2.py

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