from sanic import Sanic
from sanic import response
from sqlalchemy import select
from sanic.response import json
from models.user import User
from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from settings import db_settings
from auth.auth import protected
from auth.login import login


_base_model_session_ctx = ContextVar("session")


app = Sanic(name='__app__')
app.config.update(db_settings)
app.blueprint(login)

bind = create_async_engine(
    f"postgresql+asyncpg://{app.config.DB_USER}:{app.config.DB_PASS}"
    f"@localhost:17080/{app.config.DB_NAME}",
    echo=True)


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = sessionmaker(bind,
                                       AsyncSession,
                                       expire_on_commit=False)()
    request.ctx.session_ctx_token = \
        _base_model_session_ctx.set(request.ctx.session)


@app.middleware("response")
async def close_session(request, response):
    if hasattr(request.ctx, "session_ctx_token"):
        _base_model_session_ctx.reset(
            request.ctx.session_ctx_token)
        await request.ctx.session.close()


@app.route("/")
async def index(request):
    return response.text("JWT Demo")


@app.get("/user/<pk:int>")
@protected
async def get_user(request, pk):
    session = request.ctx.session
    async with session.begin():
        stmt = select(User).where(User.id == pk)
        result = await session.execute(stmt)
        person = result.scalar()
    if not person:
        return json({})
    return json(person.to_dict(),
                headers={"content-type":
                         "application-json"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
