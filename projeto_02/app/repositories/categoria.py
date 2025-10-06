from sqlalchemy.orm import Session
# tabela categoria
from app.models.categoria import Categoria
# contrato da API
from app.schemas.categoria import CategoriaCreate, CategoriaSchema

def create(db: Session, payload: CategoriaCreate) -> Categoria:
    # objeto = Produto(nome=payload.nome, preco=payload.preco,categoria_id=payload.categoria_id )
    objeto = Categoria(**payload.model_dump())
    db.add(objeto)
    db.commit()
    db.refresh(objeto)
    return objeto

def get(db: Session, categoria_id: int) -> Categoria | None:
    return db.get(Categoria, categoria_id)

def list_(db: Session) -> list[Categoria]:
    return db.query(Categoria).order_by(Categoria.id).all()