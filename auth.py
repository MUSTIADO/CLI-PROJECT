import hashlib
from models import User

def create_user(session, username, password, role):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = User(username=username, password=hashed_password, role=role)
    session.add(user)
    session.commit()

def authenticate_user(session, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user = session.query(User).filter_by(username=username, password=hashed_password).first()
    return user

def get_user_role(session, user_id):
    user = session.query(User).get(user_id)
    return user.role if user else None
