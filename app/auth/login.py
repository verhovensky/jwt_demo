from sanic import Blueprint, text, json
from auth.services import insert_refresh_token, \
    crypt_token, check_token, gen_token_pair, \
    set_refresh_token_cookie

login = Blueprint("login", url_prefix="/login")


@login.post("/")
async def do_login(request):
    try:
        user_id = request.json["id"]
    except KeyError:
        return text("Parameter 'id' in request "
                    "body required")
    # Gen token pair
    pair = await gen_token_pair(user_id)
    # Encrypt token as bcrypt
    enc = await crypt_token(pair[1])
    # Store refresh_token as bcrypt
    await insert_refresh_token(
        user_id=user_id,
        token=enc,
        session=request.ctx.session)
    response = json({'access_token': pair[0]})
    res = await set_refresh_token_cookie(response,
                                         token=pair[1])
    return res


@login.post("/refresh")
async def index(request):
    try:
        token = request.json["refresh_token"]
        user_id = request.json["id"]
    except KeyError:
        return text("Parameter 'refresh_token' "
                    "parameter 'id' "
                    "in request body required")
    checked = await check_token(token,
                                user_id,
                                request.ctx.session)
    if checked:
        new_pair = await gen_token_pair(user_id)
        enc = await crypt_token(new_pair[1])
        await insert_refresh_token(
            user_id=user_id,
            token=enc,
            session=request.ctx.session)
        response = json({'access_token': new_pair[0]})
        res = await set_refresh_token_cookie(response,
                                             token=new_pair[1])
        return res
    else:
        return text("Token is not valid")
