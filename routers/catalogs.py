from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import Catalog
from schemas import ErrorResponse
from schemas.catalogs import CatalogCreate
from services.engine import get_session
from shared.exeptions import CatalogNotFound

catalogs_router = APIRouter(tags=['Catalogs'], prefix='/api/v1')


@catalogs_router.get('/catalogs', response_model=list[Catalog] | None, summary="Get all catalogs")
async def get_catalogs(session: AsyncSession = Depends(get_session)):
    async with session as db:
        catalogs = await Catalog.all(db)
    return catalogs


@catalogs_router.get(
    '/catalogs/{catalog_id}',
    response_model=Catalog | None,
    responses={404: {"model": ErrorResponse}},
    summary="Get catalog by ID"
)
async def get_catalog(catalog_id: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        catalog = await Catalog.get_by_id(db, catalog_id)
        if not catalog:
            raise CatalogNotFound()
    return catalog


@catalogs_router.post('/catalogs', response_model=Catalog, summary="Create a new catalog")
async def create_catalog(catalog: CatalogCreate, session: AsyncSession = Depends(get_session)):
    async with session as db:
        catalog = await Catalog.create(db, name=catalog.name)
        return catalog


@catalogs_router.put(
    '/catalogs/{catalog_id}',
    response_model=Catalog,
    responses={404: {"model": ErrorResponse}},
    summary="Update a catalog"
)
async def update_catalog(catalog_id: int, catalog: CatalogCreate, session: AsyncSession = Depends(get_session)):
    async with session as db:
        existing_catalog = await Catalog.get_by_id(db, catalog_id)
        if not existing_catalog:
            raise CatalogNotFound()
        updated_catalog = await existing_catalog.update(db, **catalog.model_dump(exclude_unset=True))
        return updated_catalog


@catalogs_router.delete(
    '/catalogs/{catalog_id}',
    response_model=Catalog | None,
    responses={404: {"model": ErrorResponse}},
    summary="Delete a catalog")
async def delete_catalog(catalog_id: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        catalog = await Catalog.get_by_id(db, catalog_id)
        if not catalog:
            raise CatalogNotFound()
        await catalog.delete(db)
        return catalog
