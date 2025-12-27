from pydantic import Field
from gestao_atletas_api.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: str = Field(
        description='Nome da categoria', 
        examples=['Scale'], 
        max_length=10)


class CategoriaOut(CategoriaIn):
    pk_id: int = Field(
        description='Identificador da categoria',
        alias='pk_id')
