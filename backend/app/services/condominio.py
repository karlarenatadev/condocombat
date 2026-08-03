"""Service layer for Condominio business rules."""

from collections.abc import Sequence

from app.models.condominio import Condominio
from app.repositories.condominio import CondominioRepository
from app.schemas.condominio import CondominioCreate, CondominioUpdate


class CondominioJaExiste(Exception):
    """CNPJ já cadastrado para outro condomínio."""


class CondominioNaoEncontrado(Exception):
    """Condomínio não encontrado."""


class CondominioService:
    """Regras de negócio para gestão de condomínios."""

    def __init__(self, repository: CondominioRepository) -> None:
        self.repository = repository

    async def criar(self, data: CondominioCreate) -> Condominio:
        if data.cnpj:
            existente = await self.repository.get_by_cnpj(data.cnpj)
            if existente is not None:
                raise CondominioJaExiste(
                    f"CNPJ {data.cnpj} já cadastrado para '{existente.nome}'"
                )
        return await self.repository.create(data)

    async def listar(self) -> Sequence[Condominio]:
        return await self.repository.get_all()

    async def buscar(self, condominio_id: int) -> Condominio:
        condominio = await self.repository.get_by_id(condominio_id)
        if condominio is None:
            raise CondominioNaoEncontrado(f"Condomínio {condominio_id} não encontrado")
        return condominio

    async def atualizar(self, condominio_id: int, data: CondominioUpdate) -> Condominio:
        if data.cnpj:
            existente = await self.repository.get_by_cnpj(data.cnpj)
            if existente is not None and existente.id != condominio_id:
                raise CondominioJaExiste(
                    f"CNPJ {data.cnpj} já cadastrado para '{existente.nome}'"
                )
        condominio = await self.repository.update(condominio_id, data)
        if condominio is None:
            raise CondominioNaoEncontrado(f"Condomínio {condominio_id} não encontrado")
        return condominio

    async def remover(self, condominio_id: int) -> None:
        removido = await self.repository.delete(condominio_id)
        if not removido:
            raise CondominioNaoEncontrado(f"Condomínio {condominio_id} não encontrado")
