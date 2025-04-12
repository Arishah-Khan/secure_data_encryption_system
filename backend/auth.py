from pymongo import MongoClient
import hashlib
import os
import base64

client = MongoClient(os.getenv("MONGO_URI"))
db = client.secureshare

# Constants
SALT_SIZE = 16
ITERATIONS = 100_000
HASH_NAME = 'sha256'

def hash_pass(password: str) -> str:
    salt = os.urandom(SALT_SIZE)  
    key = hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATIONS)
    return base64.b64encode(salt + key).decode() 

def verify_pass(password: str, stored: str) -> bool:
    decoded = base64.b64decode(stored.encode())
    salt = decoded[:SALT_SIZE]
    stored_key = decoded[SALT_SIZE:]
    new_key = hashlib.pbkdf2_hmac(HASH_NAME, password.encode(), salt, ITERATIONS)
    return stored_key == new_key

def signup(email, password):
    try:
        # Check if email already exists
        if db.users.find_one({"email": email}):
            return "email_already_exists" 
        
        hashed = hash_pass(password)
        db.users.insert_one({"email": email, "password": hashed})
        return "signup_success"

    except Exception as e:
        print(f"Signup Error: {e}")
        return "signup_failed"
    
    
def login(email, password):
    try:
        user = db.users.find_one({"email": email})
        if not user:
            return "email_not_found"  

        if not verify_pass(password, user['password']):
            return "wrong_password"  

        return "login_success"  
    except Exception as e:
        print(f"Login Error: {e}")
        return "login_failed"

