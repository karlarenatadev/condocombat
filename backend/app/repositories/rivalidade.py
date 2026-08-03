from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rivalidade import Rivalidade


class RivalidadeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, rivalidade: Rivalidade) -> Rivalidade:
        self.session.add(rivalidade)
        await self.session.commit()
        await self.session.refresh(rivalidade)
        return rivalidade

    async def get_by_id(self, rivalidade_id: int) -> Rivalidade | None:
        result = await self.session.execute(
            select(Rivalidade).where(Rivalidade.id == rivalidade_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Rivalidade]:
        result = await self.session.execute(select(Rivalidade))
        return list(result.scalars().all())

    async def get_by_apartamento(self, apartamento_id: int) -> list[Rivalidade]:
        result = await self.session.execute(
            select(Rivalidade).where(
                or_(
                    Rivalidade.apartamento_a_id == apartamento_id,
                    Rivalidade.apartamento_b_id == apartamento_id,
                )
            )
        )
        return list(result.scalars().all())

    async def get_between(self, apto_a: int, apto_b: int) -> Rivalidade | None:
        result = await self.session.execute(
            select(Rivalidade).where(
                or_(
                    (Rivalidade.apartamento_a_id == apto_a)
                    & (Rivalidade.apartamento_b_id == apto_b),
                    (Rivalidade.apartamento_a_id == apto_b)
                    & (Rivalidade.apartamento_b_id == apto_a),
                )
            )
        )
        return result.scalar_one_or_none()

    async def top_rivalidades(self, limite: int = 10) -> list[Rivalidade]:
        ordem = ["belico", "intenso", "moderado", "leve"]
        result = await self.session.execute(select(Rivalidade))
        todas = list(result.scalars().all())
        todas.sort(key=lambda r: ordem.index(r.nivel) if r.nivel in ordem else 99)
        return todas[:limite]

    async def update(self, rivalidade_id: int, dados: dict) -> Rivalidade | None:
        rivalidade = await self.get_by_id(rivalidade_id)
        if rivalidade is None:
            return None
        for key, value in dados.items():
            setattr(rivalidade, key, value)
        await self.session.commit()
        await self.session.refresh(rivalidade)
        return rivalidade

    async def delete(self, rivalidade_id: int) -> bool:
        rivalidade = await self.get_by_id(rivalidade_id)
        if rivalidade is None:
            return False
        await self.session.delete(rivalidade)
        await self.session.commit()
        return True
