from fastapi import APIRouter
from gestao_atletas_api.atleta.controller import router as atleta_router
from gestao_atletas_api.categorias.controller import router as categorias_router
from gestao_atletas_api.centro_treinamento.controller import router as centro_router

api_router = APIRouter()

api_router.include_router(atleta_router, prefix='/atletas', tags=['Atletas'])
api_router.include_router(categorias_router, prefix='/categorias', tags=['Categorias'])
api_router.include_router(centro_router, prefix='/centros-treinamento', tags=['Centros de treinamento'])