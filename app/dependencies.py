# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from app.auth_utils import SECRET_KEY, ALGORITHM

# # This is the URL where the frontend/backend requests the token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# def verify_token(token: str = Depends(oauth2_scheme)) -> str:
#     """
#     Validates the JWT token provided by the client.
#     Returns the username (subject) if valid, else raises HTTP 401.
#     """
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")

#         if username is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token: subject not found"
#             )

#         return username

#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token"
#         )
