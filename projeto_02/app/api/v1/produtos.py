from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.db.deps import get_db
from app.schemas.produtos import ProdutoCreate, ProdutoSchema
from app.services import produtos as service_produtos
from app.repositories import estoque as repo_estoque 

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("", response_model=ProdutoSchema, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Cria um novo produto a partir dos dados fornecidos."""
    novo_produto = service_produtos.criar_produto(db, produto)
    return novo_produto

@router.get("", response_model=List[ProdutoSchema])
def listar_produtos(db: Session = Depends(get_db)):
    """Retorna uma lista com todos os produtos cadastrados."""
    return service_produtos.listar_produtos(db)

@router.get("/{produto_id}", response_model=ProdutoSchema)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Busca e retorna um produto pelo seu ID."""
    produto = service_produtos.obter_produto(db, produto_id)
    return produto

@router.get("/abaixo-minimo/", response_model=List[ProdutoSchema])
def produtos_abaixo_do_minimo(db: Session = Depends(get_db)):
    """Lista todos os produtos com saldo abaixo do mínimo estabelecido."""
    produtos = repo_estoque.get_produtos_abaixo_minimo(db)
    return produtos