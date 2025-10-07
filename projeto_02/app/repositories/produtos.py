from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.produtos import Produto
from app.schemas.produtos import ProdutoCreate, ProdutoUpdate, ProdutoSchema
from app.models.categoria import Categoria

def create(db: Session, payload: ProdutoCreate) -> Produto:
    # objeto = Produto(nome=payload.nome, preco=payload.preco,Produto_id=payload.Produto_id )
    categoria = db.get(Categoria, payload.categoria_id)
    if not categoria:
        raise HTTPException(
            status_code = 400,
            detail="Categoria não encontrada"
        )
    objeto = Produto(**payload.model_dump())
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, produto_id: int) -> Produto | None:
    return db.get(Produto, produto_id)

def list_(db: Session) -> list[Produto]:
    return db.query(Produto).order_by(Produto.id).all()
