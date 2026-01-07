from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL= os.getenv("DATABASE_URL")
engine= create_engine(
)

sessionLocal= sessionmaker(bind=engine, autoflush=False , autocommit=False)

Base= declarative_base()

def get_db():
    db= sessionLocal()
    try:
        yield db
    finally:
        db.close()
    