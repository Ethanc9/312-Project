from pymongo import MongoClient

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]


def register(username, password):
    users.insert_one({"username": username, "password": password})