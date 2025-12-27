from fastapi import FastAPI
from gestao_atletas_api.router import api_router

app = FastAPI(title='Gestão de Atletas API')
app.include_router(api_router)
