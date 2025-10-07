from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .categoria import CategoriaSchema

class ProdutoBase(BaseModel):
    nome: str
    preco: float

class ProdutoCreate(ProdutoBase):
    categoria_id: int
    estoque_minimo: Optional[int] = 0

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    estoque_minimo: Optional[int] = None

class ProdutoSchema(ProdutoBase):
    id: int
    estoque_minimo: int
    categoria: CategoriaSchema
    
    model_config = ConfigDict(from_attributes=True)

class CategoriaComProdutos(CategoriaSchema):
    produtos: List[ProdutoSchema] = []
