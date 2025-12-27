from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gestao_atletas_api.atleta.models import AtletaModel

from gestao_atletas_api.contrib.models import BaseModel


class CentroTreinamentoModel(BaseModel):
    __tablename__ = 'centros_treinamento'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    endereco: Mapped[str] = mapped_column(String(60), nullable=False)
    proprietario: Mapped[str] = mapped_column(String(30), nullable=False)

    atletas: Mapped[list["AtletaModel"]] = relationship(
        back_populates="centro_treinamento", 
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<CentroTreinamento(nome={self.nome})>"