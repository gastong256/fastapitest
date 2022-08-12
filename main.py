#Pydantinc
from pydantic import BaseModel,validator
#FastAPI
from fastapi import FastAPI, Depends
#fastapi_cloudauth
from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser, CognitoClaims
#config
from config import Settings

app = FastAPI()
settings = Settings()
auth = Cognito(
    region=settings.REGION, 
    userPoolId=settings.USERPOOLID,
    client_id=settings.APPCLIENTID,
)

# Models
class AccessUser(BaseModel):
    sub: str
    username: str
    scope: str
    @validator('scope')
    def allowed_scopes(cls, v):
        if 'email' not in v:
            raise ValueError('Scope not allowed')
        return v

@app.get("/") 
def home(current_user: AccessUser = Depends(auth.claim(AccessUser))):
    return {"Hello": current_user.username}

# Request

@app.get("/access/")
def secure_access(current_user: AccessUser = Depends(auth.claim(AccessUser))):
    # access token is valid and getting user info from access token
    return {"sub":current_user.sub, "username":current_user.username, "scope":current_user.scope}

get_current_user = CognitoCurrentUser(
    region=settings.REGION, 
    userPoolId=settings.USERPOOLID,
    client_id=settings.APPCLIENTID,
)

@app.get("/user/")
def secure_user(current_user: CognitoClaims = Depends(get_current_user)):
    # ID token is valid and getting user info from ID token
    return f"Hello, {current_user}"

# use 'scope' mothod to validate cognito groups, in this example we are validating that the current jwt is in the group 'app1'
# by default it validates that it belongs to all the groups in the list. 
@app.get("/test/", dependencies=[Depends(auth.scope(["email"]))])
def secure(current_user: AccessUser = Depends(auth.claim(AccessUser))):
    # access token is valid
    return f"Hello, {current_user.username}"