from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class RivalidadeBase(BaseModel):
    apartamento_a_id: int
    apartamento_b_id: int
    motivo: str | None = None
    nivel: str = "moderado"
    status: str = "ativa"

    @field_validator("nivel")
    @classmethod
    def validate_nivel(cls, v: str) -> str:
        allowed = {"leve", "moderado", "intenso", "belico"}
        if v not in allowed:
            raise ValueError(f"nivel deve ser um de: {', '.join(sorted(allowed))}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"ativa", "congelada", "resolvida"}
        if v not in allowed:
            raise ValueError(f"status deve ser um de: {', '.join(sorted(allowed))}")
        return v


class RivalidadeCreate(RivalidadeBase):
    pass


class RivalidadeUpdate(BaseModel):
    motivo: str | None = None
    nivel: str | None = None
    status: str | None = None

    @field_validator("nivel")
    @classmethod
    def validate_nivel(cls, v: str | None) -> str | None:
        if v is not None:
            allowed = {"leve", "moderado", "intenso", "belico"}
            if v not in allowed:
                raise ValueError(f"nivel deve ser um de: {', '.join(sorted(allowed))}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None:
            allowed = {"ativa", "congelada", "resolvida"}
            if v not in allowed:
                raise ValueError(f"status deve ser um de: {', '.join(sorted(allowed))}")
        return v


class RivalidadeRead(RivalidadeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
