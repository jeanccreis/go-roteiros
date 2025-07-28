import asyncio
from app.db.database import engine
from app.db.models import Base

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    asyncio.run(init_db())
