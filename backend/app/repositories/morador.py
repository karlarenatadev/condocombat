from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.morador import Morador


class MoradorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, morador: Morador) -> Morador:
        self.session.add(morador)
        await self.session.commit()
        await self.session.refresh(morador)
        return morador

    async def get_by_id(self, morador_id: int) -> Morador | None:
        result = await self.session.execute(
            select(Morador).where(Morador.id == morador_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Morador]:
        result = await self.session.execute(select(Morador))
        return list(result.scalars().all())

    async def get_by_cpf(self, cpf: str) -> Morador | None:
        result = await self.session.execute(select(Morador).where(Morador.cpf == cpf))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Morador | None:
        result = await self.session.execute(
            select(Morador).where(Morador.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_apartamento(self, apartamento_id: int) -> list[Morador]:
        result = await self.session.execute(
            select(Morador).where(Morador.apartamento_id == apartamento_id)
        )
        return list(result.scalars().all())

    async def update(self, morador_id: int, dados: dict) -> Morador | None:
        morador = await self.get_by_id(morador_id)
        if morador is None:
            return None
        for key, value in dados.items():
            setattr(morador, key, value)
        await self.session.commit()
        await self.session.refresh(morador)
        return morador

    async def delete(self, morador_id: int) -> bool:
        morador = await self.get_by_id(morador_id)
        if morador is None:
            return False
        await self.session.delete(morador)
        await self.session.commit()
        return True
