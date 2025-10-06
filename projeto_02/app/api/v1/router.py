# app/api/v1/router.py
from fastapi import APIRouter
from . import produtos, categoria, estoque 

api_router = APIRouter()
api_router.include_router(categoria.router)
api_router.include_router(produtos.router)
api_router.include_router(estoque.router) 