from fastapi import HTTPException, APIRouter
from pydantic_schemas.user_login import UserLogin
from pydantic_schemas.user_create import UserCreate
from models.user import User
import bcrypt
import uuid
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
from fastapi import Depends, Header
import jwt

router = APIRouter()


@router.post("/signup", status_code=201)
# The request is sent auth/signup, then it checks the body of the request is a UserCreate object.
# If valid, it runs dependancy to get db. Once it yields the db, it runs the code inside function.
def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if user_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_db = User(
        id=str(uuid.uuid4()), name=user.name, email=user.email, password=hashed_password
    )
    db.add(user_db)
    db.commit()
    db.refresh(
        user_db
    )  # Refresh the user_db object to get the updated object, show the return object in postman
    return user_db


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(status_code=400, detail="Email does not exist")

    # Check if password is set and valid before checking
    if not user_db.password:
        raise HTTPException(status_code=400, detail="Email does not exist")

    try:
        if not bcrypt.checkpw(user.password.encode(), user_db.password):
            raise HTTPException(status_code=400, detail="Wrong password")
    except (ValueError, TypeError):
        # Handle case where password hash is invalid
        raise HTTPException(status_code=400, detail="Email does not exist")

    token = jwt.encode({"id": user_db.id}, "password_key")
    return {"token": token, "user": user_db}


@router.get("/")
def current_user_data(
    db: Session = Depends(get_db), user_dict=Depends(auth_middleware)
):
    user = db.query(User).filter(User.id == user_dict["uid"]).first()

    if not user:
        raise HTTPException(404, "User not found!")

    return user
