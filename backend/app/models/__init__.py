from importlib import import_module
from typing import TYPE_CHECKING

from app.database import Base

__all__ = [
    "Apartamento",
    "Base",
    "Condominio",
    "Morador",
    "Ocorrencia",
    "Rivalidade",
]

if TYPE_CHECKING:
    # imports apenas para type checkers / linters, não executados em runtime
    from app.models.apartamento import Apartamento
    from app.models.condominio import Condominio
    from app.models.morador import Morador
    from app.models.ocorrencia import Ocorrencia
    from app.models.rivalidade import Rivalidade


def __getattr__(name: str):
    """Lazy-load and return model classes when accessed as attributes of app.models."""
    if name in __all__:
        module = import_module(f"{__name__}.{name.lower()}")
        return getattr(module, name)
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    return sorted(list(globals().keys()) + __all__)
