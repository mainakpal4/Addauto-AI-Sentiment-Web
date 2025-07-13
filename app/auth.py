# from fastapi import APIRouter, HTTPException, Depends
# from passlib.context import CryptContext
# from pydantic import BaseModel
# from jose import jwt
# from datetime import datetime, timedelta
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Configuration
# SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # In-memory user store (for now)
# fake_user_db = {}

# # Bcrypt hasher
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# router = APIRouter()

# # Schemas
# class UserRegister(BaseModel):
#     username: str
#     password: str

# class UserLogin(BaseModel):
#     username: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# # Helpers
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)

# def verify_password(plain: str, hashed: str) -> bool:
#     return pwd_context.verify(plain, hashed)

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# # Routes
# @router.post("/register")
# def register(user: UserRegister):
#     if user.username in fake_user_db:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     fake_user_db[user.username] = hash_password(user.password)
#     return {"message": "User registered successfully"}

# from fastapi.security import OAuth2PasswordRequestForm

# @router.post("/token", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username
#     password = form_data.password
#     hashed = fake_user_db.get(username)

#     if not hashed or not verify_password(password, hashed):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token({"sub": username})
#     return {"access_token": token, "token_type": "bearer"}

