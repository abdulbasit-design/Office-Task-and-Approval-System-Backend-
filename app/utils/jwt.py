import os

from datetime import (
    datetime,
    timedelta,
    timezone
)

import jwt

from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ALGORITHM = "HS256"


if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY is not configured"
    )


def create_access_token(
    user_id: int
):
    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=15)
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def create_refresh_token(
    user_id: int
):
    expire = (
        datetime.now(timezone.utc)
        + timedelta(days=7)
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    return payload