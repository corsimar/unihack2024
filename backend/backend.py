import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
from openai_setup import genLesson 
from database import lessons_collection, db, client
from utils import convert_objectid


app = Flask(__name__)

# Define a simple route for "Hello" endpoint
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Hello, World!"), 200

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

from bson import ObjectId

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


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
