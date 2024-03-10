from pymongo import MongoClient
from bson.objectid import ObjectId  # For generating unique IDs
import datetime

client = MongoClient("mongo")
db = client["cse312"]
questions = db["questions"]

def insert_question(username, question, answers):
    question_id = ObjectId()  # Generates a unique ID for the question
    question_document = {
        "_id": question_id,
        "username": username,
        "question": question,
        "answers": answers,
        "posted_at": datetime.datetime.utcnow()
    }
    questions.insert_one(question_document)
    return question_id
