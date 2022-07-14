#Python
from typing import Optional
#Pydantinc
from pydantic import BaseModel
#FastAPI
from fastapi import FastAPI, Body, Query, Path

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
    name: Optional[str] = Query(None, min_length=1, max_length=50, title="nombre", description="nombre de la persona"),
    age: int = Query(..., ge=0, title="edad", description="edad de la persona")
):
    return {name: age}

# Path parameter
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(..., ge=1, title="person id", description="id de la persona"),
):
    return {person_id: True}