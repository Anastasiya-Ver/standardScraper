from pymongo import MongoClient
import os

def get_database():
	CONNECTION_STRING = os.getenv("MONGODB_LINK")
	client = MongoClient(CONNECTION_STRING)

	return client['standards']

if __name__ == "__main__":
	dbname = get_database()