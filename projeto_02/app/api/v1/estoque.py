from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.deps import get_db
from app.schemas import estoque as schemas_estoque
from app.repositories import estoque as repo_estoque
from app.repositories import produtos as repo_produtos

router = APIRouter(prefix="/estoque", tags=["Estoque"])

# 1 e 2
@router.post("/movimentos", response_model=schemas_estoque.EstoqueMovSchema, status_code=status.HTTP_201_CREATED)
def criar_movimento(movimento: schemas_estoque.EstoqueMovCreate, db: Session = Depends(get_db)):
    """Cria uma movimentação manual de ENTRADA ou SAÍDA no estoque de um produto."""
    produto = repo_produtos.get(db, movimento.produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    if movimento.tipo.upper() not in ["ENTRADA", "SAIDA"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tipo de movimento inválido. Use 'ENTRADA' ou 'SAIDA'")

    if movimento.tipo.upper() == "SAIDA":
        saldo_atual = repo_estoque.get_saldo_produto(db, movimento.produto_id)
        if saldo_atual < movimento.quantidade:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para a saída")
    
    movimento_criado = repo_estoque.create_movimento(
        db=db,
        produto_id=movimento.produto_id,
        quantidade=movimento.quantidade,
        tipo=movimento.tipo.upper(),
        motivo=movimento.motivo
    )
    return movimento_criado

@router.get("/saldo/{produto_id}", response_model=schemas_estoque.SaldoSchema)
def obter_saldo(produto_id: int, db: Session = Depends(get_db)):
    """Calcula e retorna o saldo atual de um produto."""
    produto = repo_produtos.get(db, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    saldo = repo_estoque.get_saldo_produto(db, produto_id)
    return {"produto_id": produto_id, "nome_produto": produto.nome, "saldo_atual": saldo}

# 3
@router.post("/venda", response_model=schemas_estoque.EstoqueMovSchema, status_code=status.HTTP_201_CREATED)
def registrar_venda(venda: schemas_estoque.EstoqueOp, db: Session = Depends(get_db)):
    """Registra uma SAÍDA de estoque para simular uma operação de venda."""
    produto = repo_produtos.get(db, venda.produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    saldo_atual = repo_estoque.get_saldo_produto(db, venda.produto_id)
    if saldo_atual < venda.quantidade:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para a venda")
    
    motivo_venda = f"Venda - {venda.motivo}" if venda.motivo else "Venda"
    movimento_criado = repo_estoque.create_movimento(db, venda.produto_id, venda.quantidade, "SAIDA", motivo_venda)
    return movimento_criado

@router.post("/devolucao", response_model=schemas_estoque.EstoqueMovSchema, status_code=status.HTTP_201_CREATED)
def registrar_devolucao(devolucao: schemas_estoque.EstoqueOp, db: Session = Depends(get_db)):
    """Registra uma ENTRADA de estoque para simular a devolução de um produto."""
    produto = repo_produtos.get(db, devolucao.produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    motivo_devolucao = f"Devolução - {devolucao.motivo}" if devolucao.motivo else "Devolução"
    movimento_criado = repo_estoque.create_movimento(db, devolucao.produto_id, devolucao.quantidade, "ENTRADA", motivo_devolucao)
    return movimento_criado

@router.post("/ajuste", response_model=schemas_estoque.EstoqueMovSchema, status_code=status.HTTP_201_CREATED)
def registrar_ajuste(ajuste: schemas_estoque.EstoqueAjuste, db: Session = Depends(get_db)):
    """Registra um ajuste de ENTRADA (quantidade > 0) ou SAÍDA (quantidade < 0) no estoque. Ex: Retirada por produto danificado / Entrada de brinde de um fornecedor."""
    produto = repo_produtos.get(db, ajuste.produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

    tipo_movimento = "ENTRADA" if ajuste.quantidade > 0 else "SAIDA"
    quantidade_ajuste = abs(ajuste.quantidade)

    if tipo_movimento == "SAIDA":
        saldo_atual = repo_estoque.get_saldo_produto(db, ajuste.produto_id)
        if saldo_atual < quantidade_ajuste:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Saldo insuficiente para o ajuste de saída")
    
    motivo_ajuste = f"Ajuste - {ajuste.motivo}"
    movimento_criado = repo_estoque.create_movimento(db, ajuste.produto_id, quantidade_ajuste, tipo_movimento, motivo_ajuste)
    return movimento_criado

# 4
@router.get("/extrato/{produto_id}", response_model=List[schemas_estoque.EstoqueMovSchema])
def obter_extrato(produto_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Retorna o extrato de movimentações de um produto."""
    produto = repo_produtos.get(db, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    movimentos = repo_estoque.get_movimentos_produto(db, produto_id, skip, limit)
    return movimentos

@router.get("/resumo", response_model=List[schemas_estoque.ResEstoqueSchema])
def obter_resumo(db: Session = Depends(get_db)):
    """Gera um relatório com o resumo de saldo de todos os produtos cadastrados."""
    resumo_db = repo_estoque.get_resumo_estoque(db)
    
    resumo_final = []
    for item in resumo_db:
        saldo = item.saldo
        minimo = item.estoque_minimo
        resumo_final.append({
            "produto_id": item.id,
            "nome_produto": item.nome,
            "saldo_atual": saldo,
            "estoque_minimo": minimo,
            "situacao": "ABAIXO DO MÍNIMO" if saldo < minimo else "OK"
        })
    return resumo_final