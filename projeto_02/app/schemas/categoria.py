from pydantic import BaseModel, ConfigDict

class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaSchema(CategoriaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
