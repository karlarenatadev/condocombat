from app.models.rivalidade import Rivalidade
from app.repositories.rivalidade import RivalidadeRepository

NIVEIS = ["leve", "moderado", "intenso", "belico"]


class RivalidadeNaoEncontrada(Exception):
    pass


class RivalidadeJaExiste(Exception):
    pass


class NivelInvalido(Exception):
    pass


class RivalidadeService:
    def __init__(self, repo: RivalidadeRepository) -> None:
        self.repo = repo

    async def criar(
        self,
        apartamento_a_id: int,
        apartamento_b_id: int,
        motivo: str | None = None,
        nivel: str = "moderado",
    ) -> Rivalidade:
        if apartamento_a_id == apartamento_b_id:
            raise RivalidadeJaExiste("Não é possível criar rivalidade consigo mesmo")

        existente = await self.repo.get_between(apartamento_a_id, apartamento_b_id)
        if existente is not None:
            raise RivalidadeJaExiste(
                f"Rivalidade entre {apartamento_a_id} e {apartamento_b_id} já existe"
            )

        if nivel not in NIVEIS:
            raise NivelInvalido(
                f"Nível '{nivel}' inválido. Válidos: {', '.join(NIVEIS)}"
            )

        rivalidade = Rivalidade(
            apartamento_a_id=apartamento_a_id,
            apartamento_b_id=apartamento_b_id,
            motivo=motivo,
            nivel=nivel,
        )
        return await self.repo.create(rivalidade)

    async def listar(self) -> list[Rivalidade]:
        return await self.repo.get_all()

    async def buscar(self, rivalidade_id: int) -> Rivalidade:
        rivalidade = await self.repo.get_by_id(rivalidade_id)
        if rivalidade is None:
            raise RivalidadeNaoEncontrada(f"Rivalidade {rivalidade_id} não encontrada")
        return rivalidade

    async def listar_por_apartamento(self, apartamento_id: int) -> list[Rivalidade]:
        return await self.repo.get_by_apartamento(apartamento_id)

    async def top_rivalidades(self, limite: int = 10) -> list[Rivalidade]:
        return await self.repo.top_rivalidades(limite)

    async def escalar(self, rivalidade_id: int) -> Rivalidade:
        rivalidade = await self.buscar(rivalidade_id)
        idx_atual = NIVEIS.index(rivalidade.nivel)
        if idx_atual >= len(NIVEIS) - 1:
            return rivalidade
        novo_nivel = NIVEIS[idx_atual + 1]
        return await self.repo.update(rivalidade_id, {"nivel": novo_nivel})

    async def atualizar(self, rivalidade_id: int, dados: dict) -> Rivalidade:
        await self.buscar(rivalidade_id)
        if "nivel" in dados and dados["nivel"] not in NIVEIS:
            raise NivelInvalido(f"Nível '{dados['nivel']}' inválido")
        atualizado = await self.repo.update(rivalidade_id, dados)
        if atualizado is None:
            raise RivalidadeNaoEncontrada(f"Rivalidade {rivalidade_id} não encontrada")
        return atualizado

    async def remover(self, rivalidade_id: int) -> None:
        removido = await self.repo.delete(rivalidade_id)
        if not removido:
            raise RivalidadeNaoEncontrada(f"Rivalidade {rivalidade_id} não encontrada")
