from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["smart_drive_ai"]
collection = db["alerts"]

def save_alert(message, label):
    collection.insert_one({
        "message": message,
        "label": label,
        "timestamp": datetime.now()
    })
