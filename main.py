from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from hash_password import verify_password, get_password_hash
from db import user_collection
from tokens import create_access_tokens, UserInfo


app = FastAPI()

class UserRegistration(BaseModel):
    name : str= Field(min_length=5, max_length=50)
    email: EmailStr
    password:str= Field(min_length=8)


class UserLogin(BaseModel):
    email:EmailStr
    password:str=Field(min_length=8)

@app.post("/register")
def register_user(user: UserRegistration):
    # Check if the user is in the database
    check_user_exists = user_collection.find_one(filter= {"email": user.email})
    if check_user_exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exists.")
    # Hash the password
    hashed_password = get_password_hash(user.password)
    # Create user object
    new_user = user_collection.insert_one(
        {"name": user.name,
        "email": user.email,
        "password": hashed_password}
    )
    # Return response
    return {"message": "User registered successfully"
            }


@app.post("/login")
def login_user(user: UserLogin):
    # Check if User email exist in Database
    db_user= user_collection.find_one(filter={"email" == user.email})
    if not db_user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid credentials!")
    #  Verify hashed password
    is_password_valid = verify_password(user.password, db_user["password"])
    if not is_password_valid:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Invalid credentials!")
    # return {"error":"Invalid email or password"}

    user_data= UserInfo(
        id=str(db_user["_id"]),
        email=db_user["email"],
        name=db_user["name"]
    )

    tokens = create_access_tokens(user_data)
    return {
        "message": "Login successful",
        "data": {
            "user": db_user,
            "token": tokens
        }
    }