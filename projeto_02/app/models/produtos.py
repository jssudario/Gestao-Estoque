from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True, nullable=False)
    preco = Column(Float, nullable=False)
    estoque_minimo = Column(Integer, default=0, nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    categoria = relationship("Categoria", back_populates="produtos")

    movimentos = relationship("EstoqueMovimento", back_populates="produto", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('preco >= 0', name='check_preco_positive'),
        CheckConstraint('estoque_minimo >= 0', name='check_estoque_minimo_positive'),
    )