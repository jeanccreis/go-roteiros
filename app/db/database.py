from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.db.models import Base

DATABASE_URL = "sqlite+aiosqlite:///./go_roteiros.db"


engine = create_async_engine(DATABASE_URL, echo=True)

# Criador de sessão assíncrona
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
