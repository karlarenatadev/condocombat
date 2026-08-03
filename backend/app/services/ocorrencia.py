from app.models.ocorrencia import Ocorrencia
from app.repositories.ocorrencia import OcorrenciaRepository

STATUS_VALIDAS: dict[str, set[str]] = {
    "aberta": {"investigando", "arquivada"},
    "investigando": {"resolvida", "aberta", "arquivada"},
    "resolvida": {"arquivada"},
    "arquivada": set(),
}


class OcorrenciaNaoEncontrada(Exception):
    pass


class TransicaoStatusInvalida(Exception):
    pass


class OcorrenciaService:
    EXCEPCOES = (OcorrenciaNaoEncontrada, TransicaoStatusInvalida)

    def __init__(self, repo: OcorrenciaRepository) -> None:
        self.repo = repo

    async def criar(
        self,
        titulo: str,
        descricao: str,
        categoria: str,
        apartamento_id: int,
        gravidade: str = "media",
        status: str = "aberta",
    ) -> Ocorrencia:
        ocorrencia = Ocorrencia(
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            gravidade=gravidade,
            status=status,
            apartamento_id=apartamento_id,
        )
        return await self.repo.create(ocorrencia)

    async def listar(
        self,
        categoria: str | None = None,
        status: str | None = None,
        gravidade: str | None = None,
        apartamento_id: int | None = None,
    ) -> list[Ocorrencia]:
        return await self.repo.get_all(categoria, status, gravidade, apartamento_id)

    async def buscar(self, ocorrencia_id: int) -> Ocorrencia:
        ocorrencia = await self.repo.get_by_id(ocorrencia_id)
        if ocorrencia is None:
            raise OcorrenciaNaoEncontrada(f"Ocorrência {ocorrencia_id} não encontrada")
        return ocorrencia

    async def listar_recentes(self) -> list[Ocorrencia]:
        return await self.repo.list_recentes()

    async def atualizar_status(
        self, ocorrencia_id: int, novo_status: str
    ) -> Ocorrencia:
        ocorrencia = await self.buscar(ocorrencia_id)
        transicoes = STATUS_VALIDAS.get(ocorrencia.status, set())
        if novo_status not in transicoes:
            raise TransicaoStatusInvalida(
                f"Não é permitido mudar de '{ocorrencia.status}' para '{novo_status}'"
            )
        return await self.repo.update(ocorrencia_id, {"status": novo_status})

    async def atualizar(self, ocorrencia_id: int, dados: dict) -> Ocorrencia:
        await self.buscar(ocorrencia_id)
        if "status" in dados:
            return await self.atualizar_status(ocorrencia_id, dados["status"])
        atualizado = await self.repo.update(ocorrencia_id, dados)
        if atualizado is None:
            raise OcorrenciaNaoEncontrada(f"Ocorrência {ocorrencia_id} não encontrada")
        return atualizado

    async def remover(self, ocorrencia_id: int) -> None:
        removido = await self.repo.delete(ocorrencia_id)
        if not removido:
            raise OcorrenciaNaoEncontrada(f"Ocorrência {ocorrencia_id} não encontrada")
