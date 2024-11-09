import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, request
#from flask_restplus import Api, Resource

from openai_setup import genLesson 
from database import db, client, lessons_collection, stud_completed_less, users, experiments
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

@app.route('/get-lessons-student/<student_id>', methods=['GET'])
def getLessonsStudent(student_id):
    student = users.find_one({'_id': ObjectId(student_id)})
    if student:
        lessons = list(lessons_collection.find({}))
        lessons = [convert_objectid(lesson) for lesson in lessons]
        #add an atribute to the lesson to indicate if it has been completed by the student
        for lesson in lessons:
            lesson['completed'] = False
            if stud_completed_less.find_one({'user_id': student_id, 'lesson_id': str(lesson['_id'])}): 
                lesson['completed'] = True 
        return jsonify(lessons), 200
    else:
        return jsonify(message="Student not found"), 404

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

@app.route('/get-completed-lessons/<student_id>', methods=['GET'])
def getCompletedLessons(student_id):
    completed_lessons = list(stud_completed_less.find({'user_id': student_id}))
    completed_lessons = [convert_objectid(lesson) for lesson in completed_lessons]

    return jsonify(completed_lessons), 200

#get locked lessons
@app.route('/get-locked-lessons/<student_id>', methods=['GET'])
def getLockedLessons(student_id):
    #a lesson should be locked if it has a previous_lesson_id and the previous_lesson_id is not in the completed lessons
    locked_lessons_ids = []
    completed_lessons = list(stud_completed_less.find({'user_id': student_id}))
    lessons = list(lessons_collection.find({}))
    
    for lesson in lessons:
        if lesson['previous_lesson_id']:
            if not stud_completed_less.find_one({'user_id': student_id, 'lesson_id': lesson['previous_lesson_id']}):
                locked_lessons_ids.append(str(lesson['_id']))
    locked_lessons = [convert_objectid(lesson) for lesson in lessons if str(lesson['_id']) in locked_lessons_ids]
    #return the locked lessons ids
    locked_lessons_ids = [lesson['_id'] for lesson in locked_lessons]
    
    return jsonify(locked_lessons_ids), 200


@app.route('/get-user-xp/<user_id>', methods=['GET'])
def xp(user_id):
    # user_id = user_id
    # user = users.find_one({'_id': ObjectId(user_id)})
    
    
    # return jsonify(user['xp']), 200
    #get user xp from completed lessons 
    completed_lessons = list(stud_completed_less.find({'user_id': user_id}))
    completed_lessons = [convert_objectid(lesson) for lesson in completed_lessons]
    xp = 0
    for lesson in completed_lessons:
        lesson = lessons_collection.find_one({'_id': ObjectId(lesson['lesson_id'])})
        xp += int(lesson['xp'])
    return jsonify(xp), 200

# Experiment endpoints
@app.route('/get-experiments', methods=['GET'])
def getExperiments():
    experiments_list = list(experiments.find())
    experiments_list = [convert_objectid(experiment) for experiment in experiments_list]

    return jsonify(experiments_list), 200

@app.route('/get-experiment/<experiment_id>', methods=['GET'])
def getExperiment(experiment_id):
    experiment = experiments.find_one({'_id': ObjectId(experiment_id)})
    if experiment:
        experiment = convert_objectid(experiment)
        return jsonify(experiment), 200
    else:
        return jsonify(message="Experiment not found"), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
