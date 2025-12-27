from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from gestao_atletas_api.configs.database import get_db_session

DatabaseDependency = Annotated[AsyncSession, Depends(get_db_session)]