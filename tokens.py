import jwt
import os
from pydantic import BaseModel

class UserInfo(BaseModel):
    id: str
    email: str
    name:str

def sign_jwt(payload: dict):
    token= jwt.encode(
        payload, 
        os.getenv("JWT_SECRET_KEY"), 
        algorithm= os.getenv("JWT_ALGPRITHM"))
    return token


def decode_jwt(token:str):
    return jwt.decode(
        token,
        os.getenv("JWT_SECRET_KEY"),
        algorithms= [os.getenv("JWT_ALGPRITHM")]
    )

def create_access_tokens(data: UserInfo):
    access_token_expiration = 60 * 30 # 60 is secs and 30 is mins
    refresh_token_expiration = 60 * 60 * 24 * 7 #7 days

    access_payload = data.model_dump()
    access_payload["id"] = str(access_payload["id"])
    access_payload.update({
        "exp": access_token_expiration,
        "type": "access",
        })
    access_token = sign_jwt(access_payload)

    refresh_payload={
        "sub": data.id,
        "exp": refresh_token_expiration,
        "type": "refresh"
    }
    refresh_token=sign_jwt(refresh_payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

    # Access token is for 1 hour
    # Refresh token is for 7 days