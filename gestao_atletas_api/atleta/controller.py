from fastapi import APIRouter, Body, HTTPException, status
from sqlalchemy import select

from gestao_atletas_api.atleta.schemas import (AtletaIn, AtletaOut, AtletaUpdate)
from gestao_atletas_api.categorias.models import CategoriaModel
from gestao_atletas_api.centro_treinamento.models import CentroTreinamentoModel
from gestao_atletas_api.contrib.dependencies import DatabaseDependency
from gestao_atletas_api.atleta.models import AtletaModel

router = APIRouter()


@router.post(
    '/', 
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn
):
    
    categoria = (
        await db_session.execute(
            select(CategoriaModel).filter_by(pk_id=atleta_in.categoria_id)
        )
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'A categoria {atleta_in.categoria_id} não foi encontrada.'
        )
    
    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(pk_id=atleta_in.centro_treinamento_id)
        )
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'O centro de treinamento {atleta_in.centro_treinamento_id} não foi encontrado.'
        )
    
    atleta_model = AtletaModel(**atleta_in.model_dump())


    db_session.add(atleta_model)
    await db_session.commit()
    await db_session.refresh(atleta_model)

    return AtletaOut.model_validate(atleta_model)


@router.get(
    '/', 
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency):
    atletas = (
        await db_session.execute(select(AtletaModel))
        ).scalars().all()
    
    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@router.get(
    '/{id}', 
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: int, db_session: DatabaseDependency):
    atleta = (
        await db_session.execute(
            select(AtletaModel).filter_by(pk_id=id)
        )
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    return AtletaOut.model_validate(atleta)


@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: int, atleta_up: AtletaUpdate,
    db_session: DatabaseDependency,
):
    atleta = (
        await db_session.execute(
            select(AtletaModel).filter_by(pk_id=id)
        )
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    allowed_fields = {'nome', 'idade', 'peso'}

    for key in allowed_fields & atleta_update.keys():
        setattr(atleta, key, atleta_update[key])

    await db_session.commit()
    await db_session.refresh(atleta)

    return AtletaOut.model_validate(atleta)


@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: int, db_session: DatabaseDependency) -> None:
    atleta = (
        await db_session.execute(
            select(AtletaModel).filter_by(pk_id=id)
        )
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()



