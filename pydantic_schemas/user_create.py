from pydantic import BaseModel


# These schemas are used to validate the user login data
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
