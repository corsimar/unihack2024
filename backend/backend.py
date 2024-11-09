import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
#from flask_restplus import Api, Resource

from openai_setup import genLesson 
from database import db, client, lessons_collection, stud_completed_less, users
from utils import convert_objectid
from bson import ObjectId

app = Flask(__name__)

# Define a simple route for "Hello" endpoint
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!"), 200

# Lesson enpoints
@app.route('/generate-lesson', methods=['GET'])
def getLesson():
    topic = request.args.get('topic', type=str)

    lesson = genLesson(topic)
    return jsonify(lesson), 200

@app.route('/add-lesson', methods=['POST'])
def addLesson():
    lesson = request.json
    lessons_collection.insert_one(lesson)
    return jsonify(message="Lesson added successfully"), 200

@app.route('/remove-lesson/<lesson_id>', methods=['DELETE'])
def removeLesson(lesson_id):
    result = lessons_collection.delete_one({'_id': ObjectId(lesson_id)})
    if result.deleted_count == 1:
        return jsonify(message="Lesson removed successfully"), 200
    else:
        return jsonify(message="Lesson not found"), 404


@app.route('/get-all-lessons', methods=['GET'])
def getAllLessons():
    lessons = list(lessons_collection.find())
    lessons = [convert_objectid(lesson) for lesson in lessons]

    print(lessons)
    return jsonify(lessons), 200

@app.route('/get-previous-lessons', methods=['GET'])
def getPreviousLessons():
    lessons = list(lessons_collection.find({}))
    lessons = [convert_objectid(lesson) for lesson in lessons]
    #get only the id and topic of the lesson
    lessons = [{'_id': lesson['_id'], 'title': lesson['title']} for lesson in lessons]

    return jsonify(lessons), 200

@app.route('/login', methods=['POST'])
def login():
    # get the user data
    user = request.json
    user_email = user['email']
    user_hashed_password = user['password']
    # check if the user exists
    user = users.find_one({'email': user_email})
    if user is None:
        return jsonify(message="User not found"), 404
    # check if the password is correct
    if user['password'] != user_hashed_password:
        return jsonify(message="Incorrect password"), 401
    user = convert_objectid(user)
    return jsonify(user), 200
    
    

# User endpoints (student)
@app.route('/complete-lesson', methods=['POST'])
def completeLesson():
    entry = request.json
    stud_completed_less.insert_one(entry)
    return jsonify(message="Lesson completed successfully"), 200

@app.route('/xp/<ammount>', methods=['POST'])
def xp():
    user = request.json
    user_id = user['_id']
    xp = user['xp'] + int(ammount)
    users.update_one({'_id': ObjectId(user_id)}, {'$set': {'xp': xp}})
    return jsonify(user['xp']), 200


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
