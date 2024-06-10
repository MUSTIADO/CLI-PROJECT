import hashlib
import logging

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def log_event(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
