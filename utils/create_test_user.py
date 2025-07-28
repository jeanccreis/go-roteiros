import asyncio
from app.db.database import async_session  # CORRETO AGORA
from app.db.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user():
    async with async_session() as session:  # CORRETO AQUI TAMBÉM
        user = User(
            email="johndoe@example.com",
            full_name="John Doe",
            hashed_password=pwd_context.hash("123456"),
            disabled=False
        )
        session.add(user)
        await session.commit()
        print("Usuário de teste criado com sucesso.")

if __name__ == "__main__":
    asyncio.run(create_user())
