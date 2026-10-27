from pymongo import MongoClient


# Local MongoDB connection
MONGO_URL = "mongodb://localhost:27017"

# Create MongoDB client
client = MongoClient(MONGO_URL)

# Select database
db = client["skillpath_ai"]

# Collections
students_collection = db["students"]
analysis_collection = db["analysis"]


def get_database():
    return db


def get_students_collection():
    return students_collection


def get_analysis_collection():
    return analysis_collection


if __name__ == "__main__":
    try:
        # Test MongoDB connection
        client.admin.command("ping")

        print("MongoDB connection successful! ✅")
        print("Database: skillpath_ai")
        print("Collections:")
        print("- students")
        print("- analysis")

    except Exception as error:
        print("MongoDB connection failed! ❌")
        print(error)

        