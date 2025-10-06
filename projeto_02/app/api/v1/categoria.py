from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.deps import get_db
from app.schemas.categoria import CategoriaCreate, CategoriaSchema
from app.repositories import categoria as repo

router = APIRouter(prefix="/categoria", tags=["Categoria"])

@router.post("", response_model=CategoriaSchema, status_code=status.HTTP_201_CREATED)
def criar_categoria(payload: CategoriaCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria no banco de dados."""
    return repo.create(db, payload)

@router.get("", response_model=List[CategoriaSchema])
def listar_categorias(db: Session = Depends(get_db)):
    """Retorna uma lista com todas as categorias cadastradas."""
    return repo.list_(db)

@router.get("/{categoria_id}", response_model=CategoriaSchema)
def obter_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """Busca e retorna uma categoria pelo seu ID."""
    return repo.get(db, categoria_id)
