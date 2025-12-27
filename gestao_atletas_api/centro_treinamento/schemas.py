"""
Schemas para o módulo de centro de treinamento.

Este módulo define os modelos de dados (schemas) utilizados para validação e documentação das operações relacionadas aos centros de treinamento.

Classes:
    CentroTreinamentoIn: Schema para entrada de dados de um centro de treinamento.
    CentroTreinamentoOut: Schema para saída de dados de um centro de treinamento, incluindo o identificador.
    CentroTreinamentoAtleta: Schema para exibir informações resumidas de um centro de treinamento associado a um atleta.
"""

from typing import Annotated
from pydantic import Field
from gestao_atletas_api.contrib.schemas import BaseSchema

class CentroTreinamentoBase(BaseSchema):
    nome: Annotated[str, Field(max_length=20)]

class CentroTreinamentoIn(CentroTreinamentoBase):
    endereco: Annotated[str, Field(max_length=60)]
    proprietario: Annotated[str, Field(max_length=30)]


class CentroTreinamentoOut(CentroTreinamentoBase):
    pk_id: int
    endereco: str
    proprietario: str

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', examples=['CT King'], max_length=20)]
