import jwt
from functools import wraps
from sanic import text
from settings import JWT_SECRET
import logging

logger = logging.getLogger(__name__)


def check_token(request):
    if not request.token:
        return False
    try:
        jwt.decode(request.token,
                   JWT_SECRET,
                   algorithms=["HS512"])
    except jwt.exceptions.InvalidTokenError:
        logger.warning(f"Invalid token {request.ip}")
        return False
    else:
        return True


def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated = check_token(request)
            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return text("User unauthorized", 401)
        return decorated_function
    return decorator(wrapped)
