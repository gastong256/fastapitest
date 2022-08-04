from pydantic import BaseSettings


class Settings(BaseSettings):
    REGION: str # default value if env variable does not exist
    USERPOOLID: str
    APPCLIENTID: str # default value if env variable does not exist

# specify .env file location as Config attribute
    class Config:
        env_file = ".env"