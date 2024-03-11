from pymongo import MongoClient
from bson.objectid import ObjectId 
import datetime

client = MongoClient("mongo")
db = client["cse312"]
questions = db["questions"]

def insert_question(username, question, answers, correct_answer):
    question_id = ObjectId()  
    question_document = {
        "_id": question_id,
        "username": username,
        "question": question,
        "answers": answers,
        "correct_answer": correct_answer,  # Store the index of the right answer
        "posted_at": datetime.datetime.utcnow()
    }
    questions.insert_one(question_document)
    return question_id
