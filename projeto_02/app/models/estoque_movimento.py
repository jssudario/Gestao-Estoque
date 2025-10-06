from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class EstoqueMovimento(Base):
    """ Modelo que registra cada entrada ou saída de estoque de um produto. """
    __tablename__ = "estoque_movimentos"

    id = Column(Integer, primary_key=True)
    
    # "ENTRADA" ou "SAIDA"
    tipo = Column(String(50), nullable=False)
    
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String(255), index=True, nullable=True)

    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    produto = relationship("Produto", back_populates="movimentos")

    criado_em = Column(DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint('quantidade > 0', name='check_quantidade_positive'),
    )