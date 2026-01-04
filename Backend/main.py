from fastapi import FastAPI
from database import Base, engine
Base.metadata.create_all(bind=engine)
app=FastAPI()
@app.get("/")
def greet():
    return "Hello"
