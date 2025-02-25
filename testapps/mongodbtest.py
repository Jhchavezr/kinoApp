from pymongo import MongoClient

try:
    client = MongoClient("mongodb://admin_user:Cic40MX@52.15.210.68:27017/admin")
    client.admin.command("ping")  # Simple command to check the connection
    print("Connection successful!")
except Exception as e:
    print("Failed to connect to MongoDB:", e)
