from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from gestao_atletas_api.centro_treinamento.schemas import (CentroTreinamentoIn, CentroTreinamentoOut)
from gestao_atletas_api.centro_treinamento.models import CentroTreinamentoModel

from gestao_atletas_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo Centro de treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency, 
    centro_treinamento_in: CentroTreinamentoIn
) -> CentroTreinamentoOut:
    
    centro_treinamento_model = CentroTreinamentoModel(
        **centro_treinamento_in.model_dump()
    )
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    await db_session.refresh(centro_treinamento_model)

    return CentroTreinamentoOut.model_validate(centro_treinamento_model)
    
    
@router.get(
    '/', 
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency):
    centros_treinamento = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    
    return [CentroTreinamentoOut.model_validate(ct)
        for ct in centros_treinamento
    ]


@router.get(
    '/{id}', 
    summary='Consulta um centro de treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: int, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(pk_id=id)
        )
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de treinamento não encontrado no id: {id}'
        )
    
    return CentroTreinamentoOut.model_validate(centro_treinamento)