from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class EstoqueMov(BaseModel):
    produto_id: int
    quantidade: int

class EstoqueMovCreate(EstoqueMov):
    tipo: str # "ENTRADA" ou "SAIDA"
    motivo: Optional[str] = None

class EstoqueOp(EstoqueMov):
    motivo: Optional[str] = None

class EstoqueAjuste(EstoqueMov):
    motivo: str

class EstoqueMovSchema(EstoqueMov):
    id: int
    tipo: str
    motivo: Optional[str] = None
    criado_em: datetime
    
    model_config = ConfigDict(from_attributes=True)

class SaldoSchema(BaseModel):
    produto_id: int
    nome_produto: str
    saldo_atual: int

class ResEstoqueSchema(BaseModel):
    produto_id: int
    nome_produto: str
    saldo_atual: int
    estoque_minimo: int
    situacao: str # OK, ABAIXO DO MÍNIMO