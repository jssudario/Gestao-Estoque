from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.models import produtos as models_produto
from app.models import estoque_movimento as models_estoque

def get_saldo_produto(db: Session, produto_id: int) -> int:
    saldo = db.query(
        func.sum(
            case(
                (models_estoque.EstoqueMovimento.tipo == 'ENTRADA', models_estoque.EstoqueMovimento.quantidade),
                (models_estoque.EstoqueMovimento.tipo == 'SAIDA', -models_estoque.EstoqueMovimento.quantidade),
                else_=0
            )
        )
    ).filter(models_estoque.EstoqueMovimento.produto_id == produto_id).scalar()
    return saldo or 0

def create_movimento(db: Session, produto_id: int, quantidade: int, tipo: str, motivo: str = None) -> models_estoque.EstoqueMovimento:
    movimento_db = models_estoque.EstoqueMovimento(
        produto_id=produto_id,
        quantidade=quantidade,
        tipo=tipo.upper(),
        motivo=motivo
    )
    db.add(movimento_db)
    db.commit()
    db.refresh(movimento_db)
    return movimento_db

def get_movimentos_produto(db: Session, produto_id: int, skip: int = 0, limit: int = 100):
    return db.query(models_estoque.EstoqueMovimento)\
             .filter(models_estoque.EstoqueMovimento.produto_id == produto_id)\
             .order_by(models_estoque.EstoqueMovimento.criado_em.desc())\
             .offset(skip)\
             .limit(limit)\
             .all()

def get_resumo_estoque(db: Session):
    saldo_subquery = db.query(
        models_estoque.EstoqueMovimento.produto_id,
        func.sum(
            case(
                (models_estoque.EstoqueMovimento.tipo == 'ENTRADA', models_estoque.EstoqueMovimento.quantidade),
                (models_estoque.EstoqueMovimento.tipo == 'SAIDA', -models_estoque.EstoqueMovimento.quantidade)
            )
        ).label('saldo_atual')
    ).group_by(models_estoque.EstoqueMovimento.produto_id).subquery()
    resultado = db.query(
        models_produto.Produto.id,
        models_produto.Produto.nome,
        models_produto.Produto.estoque_minimo,
        func.coalesce(saldo_subquery.c.saldo_atual, 0).label('saldo')
    ).outerjoin(
        saldo_subquery, models_produto.Produto.id == saldo_subquery.c.produto_id
    ).order_by(models_produto.Produto.id).all()
    return resultado

def get_produtos_abaixo_minimo(db: Session):
    saldo_subquery = db.query(
        models_estoque.EstoqueMovimento.produto_id,
        func.sum(
            case(
                (models_estoque.EstoqueMovimento.tipo == 'ENTRADA', models_estoque.EstoqueMovimento.quantidade),
                (models_estoque.EstoqueMovimento.tipo == 'SAIDA', -models_estoque.EstoqueMovimento.quantidade)
            )
        ).label('saldo_atual')
    ).group_by(models_estoque.EstoqueMovimento.produto_id).subquery()
    resultado = db.query(models_produto.Produto)\
        .outerjoin(saldo_subquery, models_produto.Produto.id == saldo_subquery.c.produto_id)\
        .filter(func.coalesce(saldo_subquery.c.saldo_atual, 0) < models_produto.Produto.estoque_minimo)\
        .all()
    return resultado