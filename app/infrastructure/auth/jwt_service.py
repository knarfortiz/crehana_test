from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(username: str, user_id: str, expires_delta: timedelta):
    """
    Create an access token from a username and user_id.

    Args:
    - username (str): The username to encode in the token.
    - user_id (str): The user id to encode in the token.
    - expires_delta (timedelta): The time delta from now that the token will expire.

    Returns:
    - str: An access token with the username and user_id encoded.
    """
    encode = {"sub": username, "id": str(user_id)}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    """
    Decode an access token to retrieve its payload.

    Args:
    - token (str): The JWT access token to be decoded.

    Returns:
    - dict: The decoded payload if the token is valid.
    - None: If the token is invalid or decoding fails.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
