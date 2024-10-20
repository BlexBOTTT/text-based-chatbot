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
from pymongo import MongoClient

### QUERY SEARCHER, DO NOT DELETE
def build_query(intent: str, collection_name: str) -> dict:
    # Define fields to search based on the collection type
    fields = {
        "admission": ["rasa_intent", "utter_admission"],
        "courses": ["rasa_intent", "course", "synonyms", "tuition"]
        
        # Add other collections and their respective fields as needed, MANUALLY!
    }

    # Construct the query dynamically
    if collection_name in fields:
        return {
            "$or": [
                {field: {"$regex": intent, "$options": "i"}} for field in fields[collection_name]
            ]
        }
    # Return an empty query if the collection name is not found
    return {}
### 

### DO NOT DELETE: MAIN CODE FETCH SNIPPET FOR MONGODB RESPONSE, 
class ActionFetchDynamicResponse(Action):
    def name(self) -> Text:
        return "action_fetch_dynamic_response"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client['admission_chatbot']

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message['intent']['name']
        
        for collection_name in self.db.list_collection_names():
            collection = self.db[collection_name]

            # only for complex ones like courses collection
            if collection_name == "courses" and intent == "ask_tuition":
                course_name = tracker.get_slot('course')  # Fetch the course slot value from the tuition.yml NLU

                 # Use the course_name in the query if it's available
                if course_name:
                    query = {
                        "course": {"$regex": course_name, "$options": "i"}
                    }
                else:
                    # If no course name is available, fallback to a broader query
                    query = build_query(intent, collection_name)
            else: # Use the helper function to build the query, fallback to a broader query
                query = build_query(intent, collection_name)

            # logging debugger START
            # CLI command: rasa run actions --debug
            # import logging
            # logger = logging.getLogger(__name__)

            # logger.debug(f"Searching for intent: {intent} in collection: {collection_name}")
            # logger.debug(f"Query used: {query}")

            result = collection.find_one(query)

            # if result:
            #     logger.debug(f"Document found: {result}")
            # else:
            #     logger.debug(f"No matching document found in collection: {collection_name}")
            # logging debugger END

            if result:
                if collection_name == "courses":
                    response = f"{result.get('course', 'No course available.')} - Tuition: {result.get('tuition', 'No tuition available.')}"
                elif collection_name == "admission":    
                    response = f"{result.get('utter_admission', 'No details available.')}"
                
                dispatcher.utter_message(text=response)
                return []

        dispatcher.utter_message(text="I'm sorry, I couldn't find the information you're looking for.")
        return []
###



### RASA DEFAULT:
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