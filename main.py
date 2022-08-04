import os
#Python
from typing import Optional
#Pydantinc
from pydantic import BaseModel, BaseSettings
#FastAPI
from fastapi import FastAPI, Body, Query, Path, Depends
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
from config import Settings

app = FastAPI()
settings = Settings()
auth = Cognito(
    region=settings.REGION, 
    userPoolId=settings.USERPOOLID,
    client_id=settings.APPCLIENTID,
)

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    is_married: Optional[bool] = None

print(auth)
@app.get("/", dependencies=[Depends(auth.scope(["read"]))])
def home():
    return {"Hello": "World"}

# Request

class AccessUser(BaseModel):
    sub: str
    username: str
@app.get("/access/")
def secure_access(current_user: AccessUser = Depends(auth.claim(AccessUser))):
    # access token is valid and getting user info from access token
    return f"Hello", {current_user.sub}, {current_user.username}

get_current_user = CognitoCurrentUser(
    region=settings.REGION, 
    userPoolId=settings.USERPOOLID,
    client_id=settings.APPCLIENTID,
)


@app.get("/user/")
def secure_user(current_user: CognitoClaims = Depends(get_current_user)):
    # ID token is valid and getting user info from ID token
    return f"Hello, {current_user.username}"
