#Python
from typing import Optional
#Pydantinc
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI, Body

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"Hello": "World"}

# Testing

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person
