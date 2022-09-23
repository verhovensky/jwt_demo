import bcrypt
import jwt
from models.user import User
from sqlalchemy import select
from datetime import datetime, timedelta
from settings import JWT_SECRET
from sanic import json


async def insert_refresh_token(user_id: str,
                               token: str,
                               session) -> bool:

    """ Insert/Update token in user.token field (bcrypt) """

    async with session.begin():
        user = select(User).where(User.id == int(user_id))
        query = await session.execute(user)
        person = query.scalar()
        if person:
            person.token = token
            await session.commit()
            return True
        return False


async def make_payload(id: str,
                       delta: timedelta) -> dict:

    """ Make payload used as JWT claims """

    return {
        'user_id': id,
        'exp': datetime.utcnow() + delta,
        'iat': datetime.utcnow()}


async def crypt_token(token: str) -> str:
    token = token.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(token, salt)
    return hashed.decode("utf-8")


async def check_token(token: str,
                      user_id: str,
                      session) -> bool:
    async with session.begin():
        user = select(User).where(User.id == int(user_id))
        query = await session.execute(user)
        person = query.scalar()
        if person:
            hashed = person.token.encode("utf-8")
            token = token.encode("utf-8")
            if bcrypt.checkpw(token, hashed):
                return True
        return False


async def gen_token_pair(user_id: str) -> tuple:
    acs_payload = await make_payload(
        id=user_id,
        delta=timedelta(minutes=5))
    access_token = jwt.encode(acs_payload, JWT_SECRET,
                              algorithm="HS512")
    ref_payload = await make_payload(
        id=user_id,
        delta=timedelta(days=1))
    refresh_token = jwt.encode(ref_payload, JWT_SECRET,
                               algorithm="HS512")
    return access_token, refresh_token


async def set_refresh_token_cookie(response: json,
                                   token: str):
    response.cookies["refresh_token"] = token
    response.cookies["refresh_token"]["samesite"] = "Strict"
    response.cookies["refresh_token"]["httponly"] = True
    response.cookies["refresh_token"]["secure"] = True
    # response.cookies["refresh_token"]["expires"] = ...
    # response.cookies["refresh_token"]["path"] = ...
    return response
