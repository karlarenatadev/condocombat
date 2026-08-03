from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

from app.models.apartamento import Apartamento

class Morador(Base):
    __tablename__ = "moradores"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tipo: Mapped[str] = mapped_column(
        String(20), default="proprietario", nullable=False
    )
    apartamento_id: Mapped[int] = mapped_column(
        ForeignKey("apartamentos.id"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    apartamento: Mapped["Apartamento"] = relationship(
        "Apartamento", back_populates="moradores"
    )