from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient

# uri = "mongodb+srv://shahazeer3:medscribe@cluster0.12pmea0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # Create a new client and connect to the server
# client = MongoClient(uri)

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

database_url = "mongodb://localhost:27017"
client = MongoClient(database_url)
database_name = "MedScribe"              
collection_name = "CaseStudies"     
db = client[database_name]
collection = db[collection_name]       

class ActionGetCaseStudies(Action):
    def name(self) -> Text:
        return "action_get_case_studies"
    
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        patient_id = next(tracker.get_latest_entity_values("patient_id"), None)

        document = collection.find_one({"patient_id": patient_id})
        if document:
            # info = "<br><br>".join(textwrap.fill(p, width=80) for p in document["patient"].split("<br><br>"))
            age = document.get("age", [])[0][0] if document.get("age") else None
            response_text = "Patient ID : {} <br>Patient User ID : {} <br>PMID : {} <br>Patient Age : {} <br>Gender : {} <br>Title : {}. <br>-------------------------------------------------------------------------------------------------------------------------------------- <br>Patient: <br>{}".format(patient_id, document["patient_uid"],document["PMID"],age,document['gender'],document["title"], document["patient"])
        else:
            print("No document found for patient ID:", patient_id)
            response_text = "I'm sorry, I couldn't find that patient ID in my database."

        dispatcher.utter_message(text=response_text)
        return []
    

class ActionSearchCaseStudies(Action):
    def name(self) -> Text:
        return "action_search_case_studies"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        search_string = next(tracker.get_latest_entity_values("search_string"), None)

        # documents = collection.find({"title": {"$regex": search_string, "$options": "i"}}).limit(5)
        documents = collection.aggregate([
            {"$match": {"title": {"$regex": search_string, "$options": "i"}}},
            {"$sample": {"size": 5}}
        ])

        documents = list(documents)

        if documents:
            response_text = "Here are some case studies related to '{}':<br><br>".format(search_string)
            for document in documents:
                response_text += "<br>Title: {}<br>Patient-ID: {}<br>Patient User ID: {}<br>PMID: {}<br>--------------------------------------------------------------------------------------------------------------------------------------<br>".format(document["title"], document["patient_id"], document["patient_uid"], document["PMID"])
        else:
            print("No documents found containing:", search_string)
            response_text = "I'm sorry, I couldn't find any case studies related to '{}'.".format(search_string)

        dispatcher.utter_message(text=response_text)
        return []

class ActionCheckBP(Action):
    def name(self) -> Text:
        return "action_check_hypertension"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bp_reading = next(tracker.get_latest_entity_values("blood_pressure"), None)

        if bp_reading:
            try:
                systolic, diastolic = map(int, bp_reading.split('/'))
            except ValueError:
                dispatcher.utter_message("Please provide a valid blood pressure reading.")
                return []

            # Check if the user has hypertension based on the blood pressure reading
            if systolic >= 140 or diastolic >= 90:
                dispatcher.utter_message("Based on your blood pressure reading, you may have hypertension.<br> If you have exercised before checking your blood pressure, try taking two readings, with a minimum of 15 to 30 minutes interval between each reading. If the readings are the same, it is advisable to visit a doctor for further evaluation. ")
            else:
                dispatcher.utter_message("Based on your blood pressure reading, you may not have hypertension.")
        else:
            dispatcher.utter_message("I couldn't find a blood pressure reading in your message.")

        return []
    

class ActionCheckTemperature(Action):
    def name(self) -> Text:
        return "action_check_temperature"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        temperature = next(tracker.get_latest_entity_values("body_temp"), None)
        if temperature and float(temperature) > 37.0:
            # User has a fever
            dispatcher.utter_message("You have a fever.<br>")
        else:
            # User does not have a fever
            dispatcher.utter_message("You do not have a fever.")
        
        return []
    

class ActionSearchDoctors(Action):
    def name(self) -> Text:
        return "action_seach_doctors"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doctor_type = next(tracker.get_latest_entity_values("doctor"), None)
        
        collection_Doctor = db["Doctors"]
        
        # Search for doctors based on the provided type
        doctors = collection_Doctor.find({"specialization": doctor_type})
        doctor_list = [doctor["name"] for doctor in doctors]
        
        # Close the MongoDB connection
        client.close()
        
        if doctor_list:
            message = f"Here are some {doctor_type} doctors you can consider: {', '.join(doctor_list)}"
        else:
            message = f"Sorry, we couldn't find any {doctor_type} doctors at the moment."
        
        dispatcher.utter_message(message)
        
        return []