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

def output_questions():
    return_list = ''
    question_list = list(questions.find({}))
    index = 1
    print(question_list)
    for i in question_list:
        print(i['answers'])
        return_list += '<br/>' + 'Question ' + str(index) + ': ' + i['question'] + '<br/>'
        answer_num = 1
        for j in i['answers']:
            j = j[:-1]
            return_list += str(answer_num) + ': ' + j + '<br/>'
            answer_num += 1
        index += 1
    print(return_list)
    return return_list
