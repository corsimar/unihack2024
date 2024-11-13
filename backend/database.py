from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
uri = os.getenv('MONGODB_URI')
    
client = MongoClient(uri)
db = client['RevoLearn']
lessons_collection = db['lessons']
stud_completed_less = db['stud_completed_less']
users = db['users']
experiments = db['experiments']
stud_completed_exp = db['stud_completed_exp']



