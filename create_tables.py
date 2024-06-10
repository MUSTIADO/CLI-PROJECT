from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine('sqlite:///ecommerce.db')  # Make sure this matches your database configuration

Base.metadata.create_all(engine)
