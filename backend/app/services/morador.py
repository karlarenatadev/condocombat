from app.models.morador import Morador
from app.repositories.morador import MoradorRepository


class MoradorComCPFJaExiste(Exception):
    pass


class MoradorComEmailJaExiste(Exception):
    pass


class MoradorNaoEncontrado(Exception):
    pass


class MoradorService:
    def __init__(self, repo: MoradorRepository) -> None:
        self.repo = repo

    async def criar(
        self,
        nome: str,
        cpf: str,
        email: str,
        apartamento_id: int,
        telefone: str | None = None,
        tipo: str = "proprietario",
    ) -> Morador:
        existente_cpf = await self.repo.get_by_cpf(cpf)
        if existente_cpf is not None:
            raise MoradorComCPFJaExiste(f"CPF {cpf} já cadastrado")

        existente_email = await self.repo.get_by_email(email)
        if existente_email is not None:
            raise MoradorComEmailJaExiste(f"Email {email} já cadastrado")

        morador = Morador(
            nome=nome,
            cpf=cpf,
            email=email,
            telefone=telefone,
            tipo=tipo,
            apartamento_id=apartamento_id,
        )
        return await self.repo.create(morador)

    async def listar(self) -> list[Morador]:
        return await self.repo.get_all()

    async def buscar(self, morador_id: int) -> Morador:
        morador = await self.repo.get_by_id(morador_id)
        if morador is None:
            raise MoradorNaoEncontrado(f"Morador {morador_id} não encontrado")
        return morador

    async def listar_por_apartamento(self, apartamento_id: int) -> list[Morador]:
        return await self.repo.get_by_apartamento(apartamento_id)

    async def atualizar(self, morador_id: int, dados: dict) -> Morador:
        existente = await self.repo.get_by_id(morador_id)
        if existente is None:
            raise MoradorNaoEncontrado(f"Morador {morador_id} não encontrado")

        if "cpf" in dados and dados["cpf"] != existente.cpf:
            outro = await self.repo.get_by_cpf(dados["cpf"])
            if outro is not None:
                raise MoradorComCPFJaExiste(
                    f"CPF {dados['cpf']} já pertence a outro morador"
                )

        if "email" in dados and dados["email"] != existente.email:
            outro = await self.repo.get_by_email(dados["email"])
            if outro is not None:
                raise MoradorComEmailJaExiste(
                    f"Email {dados['email']} já pertence a outro morador"
                )

        atualizado = await self.repo.update(morador_id, dados)
        if atualizado is None:
            raise MoradorNaoEncontrado(f"Morador {morador_id} não encontrado")
        return atualizado

    async def remover(self, morador_id: int) -> None:
        removido = await self.repo.delete(morador_id)
        if not removido:
            raise MoradorNaoEncontrado(f"Morador {morador_id} não encontrado")
