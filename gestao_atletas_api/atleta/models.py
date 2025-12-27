from datetime import datetime
from decimal import Decimal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gestao_atletas_api.categorias.models import CategoriaModel
    from gestao_atletas_api.centro_treinamento.models import CentroTreinamentoModel


from sqlalchemy import (Integer, String, DateTime, ForeignKey, Enum, Numeric)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy.sql import func
from gestao_atletas_api.contrib.models import BaseModel

from sqlalchemy import Enum as SAEnum
from gestao_atletas_api.atleta.enums import SexoEnum


class AtletaModel(BaseModel):
    __tablename__ = 'atletas'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)

    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    
    peso: Mapped[Decimal] = mapped_column(Numeric(5, 2),nullable=False,)
    altura: Mapped[Decimal] = mapped_column(Numeric(3, 2),nullable=False,)

    sexo: Mapped[SexoEnum] = mapped_column(SAEnum(SexoEnum, name="sexo"),nullable=False,)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False,
    )
    
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.pk_id", ondelete="CASCADE"),
        index=True, 
        nullable=False,
    )
    
    centro_treinamento_id: Mapped[int] = mapped_column(
        ForeignKey("centros_treinamento.pk_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    categoria: Mapped["CategoriaModel"] = relationship(
        back_populates="atletas", 
        lazy="selectin",
    )
    
    centro_treinamento: Mapped["CentroTreinamentoModel"] = relationship(
        back_populates="atletas",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Atleta(nome={self.nome}, cpf={self.cpf})>"