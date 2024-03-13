from pymongo import MongoClient
from bson.objectid import ObjectId 
import datetime

client = MongoClient("mongo")
db = client["cse312"]
questions = db["questions"]
submissions = db["submissions"]

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

def output_questions():
    questions_list = list(questions.find({}))
    for question in questions_list:
        question['_id'] = str(question['_id'])
    print(questions_list)  # Convert ObjectId to string for JSON compatibility
    return questions_list


def validate_answer(username, question_id, answer_index):
    # Convert question_id from string to ObjectId
    question_id = ObjectId(question_id)
    
    # Find the question to ensure it exists and the answer index is valid
    question = questions.find_one({"_id": question_id})
    if question and 0 <= answer_index < len(question['answers']):
        is_correct = answer_index == question['correct_answer']
        message = "Correct!" if is_correct else "Incorrect."
        
        # Increment the answer count
        questions.update_one({"_id": question_id}, {"$inc": {"answer_count": 1}})
        
        # Save the user's submission
        submissions = db["submissions"]  # Assuming you have a submissions collection
        submissions.insert_one({
            "username": username,
            "questionId": str(question_id),  # Convert ObjectId to string for storage
            "chosenAnswer": answer_index,
            "submittedAt": datetime.datetime.utcnow()  # Optionally store the submission time
        })
        
        return {"message": message, "isCorrect": is_correct}
    else:
        return {"message": "Question or answer not found."}