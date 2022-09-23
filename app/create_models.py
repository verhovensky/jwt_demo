import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from settings import db_settings
from models.user import User

settings = list(map(
    str, [v for k, v in db_settings.items()]))


async def main():
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings[3]}:{settings[2]}"
        f"@{settings[0]}:17080/{settings[1]}",
        echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)
        await conn.run_sync(User.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            user = User(name='Mike')
            session.add(user)
            await session.commit()
    print(f"User with id={user.id} created")

asyncio.run(main())
