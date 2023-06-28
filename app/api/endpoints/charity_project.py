from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_closed_or_invested,
                                check_charity_project_exists,
                                check_charity_project_fully_invested,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_crud
from app.schemas.charity_project import (CharityProjectDB,
                                         CharityProjectUpdate,
                                         CreateCharityProject)
from app.services.investment import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_project(
        charity: CreateCharityProject,
        session: AsyncSession = Depends(get_async_session)
):
    """Создает благотворительный проект."""
    await check_name_duplicate(charity.name, session)
    new_project = await charity_crud.create(charity, session)
    return await investment_process(new_project, session)


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
):
    """Получает список всех проектов."""
    return await charity_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Редактирует проект."""
    await check_name_duplicate(obj_in.name, session)
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_fully_invested(project)
    if obj_in.full_amount is not None:
        if obj_in.full_amount < project.invested_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Требуемая сумма не может быть меньше внесенной!'
            )
    project = await charity_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session,
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаляет проект."""
    project = await check_charity_project_exists(project_id, session)
    await check_charity_project_closed_or_invested(project)
    project = await charity_crud.remove(
        project, session
    )
    return project
