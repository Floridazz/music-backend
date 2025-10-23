from pydantic import BaseModel


# These schemas are used to validate the user login data
class UserLogin(BaseModel):
    email: str
    password: str
