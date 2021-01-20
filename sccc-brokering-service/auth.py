import logging
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from psycopg2.errors import UniqueViolation

from config import AUTHENTICATION_SECRET_KEY
from models import User, BaseUser
from persistence import get_cursor


ALGORITHM = "HS256"
OAUTH_2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
LOGGER = logging.getLogger(__name__)

def get_user_by_username(username: str):
    with get_cursor() as cursor:
        cursor.execute("SELECT username, password, balance FROM users WHERE username = %s;", (username,))
        user = cursor.fetchone()
    return user

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Verify a plan password against a hashed password """
    return PWD_CONTEXT.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> BaseUser:
    """ Authenticate a user given a username and password from form_data """
    LOGGER.debug("Authenticating %s", username)
    
    if (user := get_user_by_username(username=username)) is None:
        LOGGER.debug("Username not found for %s", username)
        return None

    password_valid = verify_password(plain_password=password, hashed_password=user['password'])
    return BaseUser(**user) if password_valid else None

def create_new_user(user: User) -> bool:
    """ Create a new user. User object should contain a plain password.
        Returns the BaseUser model of the created user. Password excluded from
        model so safe to return via API.
    """
    user.password = PWD_CONTEXT.hash(user.password)
    try:
        with get_cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s) RETURNING (username)", (user.username, user.password))
            username = cursor.fetchone()
    except UniqueViolation:
        LOGGER.exception("Failed to create new user")
        return None
    return username


def create_token(username: str, token_expiry_minutes: int = 180) -> str:
    """ Function to create a JWT token for a given username with a specified expiry.
        User should be verified before using this function. This does NOT verify
        their credentials.
    """
    expiry = datetime.now() + timedelta(minutes=token_expiry_minutes)
    claims = {"exp": expiry, "uid": username}
    return jwt.encode(claims, AUTHENTICATION_SECRET_KEY, ALGORITHM)

def get_current_user(token: str = Depends(OAUTH_2_SCHEME)) -> User:
    """ Verify the given JWT token and get the relevant user if valid """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception

    try:
        # attempt to decode the JWT token against the secret key
        payload = jwt.decode(token, AUTHENTICATION_SECRET_KEY, algorithms=[ALGORITHM])
        # if valid, grab the username from the JWT token.
        if (username := payload.get("uid", None)) is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    return User(**get_user_by_username(username=username))