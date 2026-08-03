from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class OcorrenciaBase(BaseModel):
    titulo: str
    descricao: str
    categoria: str
    gravidade: str = "media"
    status: str = "aberta"
    apartamento_id: int

    @field_validator("categoria")
    @classmethod
    def validate_categoria(cls, v: str) -> str:
        allowed = {"barulho", "briga", "festa", "obra", "animal", "outra"}
        if v not in allowed:
            raise ValueError(f"categoria deve ser um de: {', '.join(sorted(allowed))}")
        return v

    @field_validator("gravidade")
    @classmethod
    def validate_gravidade(cls, v: str) -> str:
        allowed = {"baixa", "media", "alta", "critica"}
        if v not in allowed:
            raise ValueError(f"gravidade deve ser um de: {', '.join(sorted(allowed))}")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"aberta", "investigando", "resolvida", "arquivada"}
        if v not in allowed:
            raise ValueError(f"status deve ser um de: {', '.join(sorted(allowed))}")
        return v


class OcorrenciaCreate(OcorrenciaBase):
    pass


class OcorrenciaUpdate(BaseModel):
    titulo: str | None = None
    descricao: str | None = None
    categoria: str | None = None
    gravidade: str | None = None
    status: str | None = None

    @field_validator("categoria")
    @classmethod
    def validate_categoria(cls, v: str | None) -> str | None:
        if v is not None:
            allowed = {"barulho", "briga", "festa", "obra", "animal", "outra"}
            if v not in allowed:
                raise ValueError(
                    f"categoria deve ser um de: {', '.join(sorted(allowed))}"
                )
        return v

    @field_validator("gravidade")
    @classmethod
    def validate_gravidade(cls, v: str | None) -> str | None:
        if v is not None:
            allowed = {"baixa", "media", "alta", "critica"}
            if v not in allowed:
                raise ValueError(
                    f"gravidade deve ser um de: {', '.join(sorted(allowed))}"
                )
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is not None:
            allowed = {"aberta", "investigando", "resolvida", "arquivada"}
            if v not in allowed:
                raise ValueError(f"status deve ser um de: {', '.join(sorted(allowed))}")
        return v


class OcorrenciaRead(OcorrenciaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
