#Python
from typing import Optional
#Pydantinc
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI, Body, Query

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

# Request

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations query
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...)
):
    return {name: age}