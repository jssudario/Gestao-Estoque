# app/services/produtos.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import produtos as repo
from app.schemas.produtos import ProdutoCreate
from app.models.produtos import Produto

def criar_produto(db: Session, payload: ProdutoCreate) -> Produto:
    # validações de negócio
    if payload.preco <= 0:
        raise ValueError("Preço deve ser maior que zero.")
    return repo.create(db, payload)

def listar_produtos(db: Session) -> list[Produto]:
    """Chama o repositório para listar todos os produtos."""
    return repo.list_(db)

def obter_produto(db: Session, produto_id: int) -> Produto:
    """Chama o repositório para obter um produto por ID."""
    produto = repo.get(db, produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Produto não encontrado"
        )
    return produto