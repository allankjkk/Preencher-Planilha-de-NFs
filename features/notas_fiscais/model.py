from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class NotaFiscal:
    numero: str
    chave: str | None
    fornecedor: str | None
    cnpj: str | None
    emissao: datetime | None
    valor: float | None
    obra: str
    materiais: list[str]