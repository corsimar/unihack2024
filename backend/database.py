from pymongo.mongo_client import MongoClient

# Replace <username> with your actual MongoDB Atlas username
uri = "mongodb+srv://RevoLearn:UMHsBiClmSxemj0I@revolearn.fjzbs.mongodb.net/?retryWrites=true&w=majority&appName=RevoLearn"

    
client = MongoClient(uri)
db = client['RevoLearn']
lessons_collection = db['lessons']
stud_completed_less = db['stud_completed_less']
users = db['users']



