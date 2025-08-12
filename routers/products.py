from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Catalog
from models.products import Product
from schemas import ErrorResponse
from schemas.products import ProductCreate, ProductUpdate
from services.engine import get_session
from shared.exeptions import ProductNotFound, CatalogNotFound

products_router = APIRouter(tags=['Products'], prefix='/api/v1')


@products_router.get(
    '/products',
    response_model=list[Product] | None,
    summary="Get all products"
)
async def get_products(session: AsyncSession = Depends(get_session)):
    async with session as db:
        products = await Product.all(db)
    return products


@products_router.get(
    '/products/{product_id}',
    response_model=Product | None,
    summary="Get product by ID"
)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        product = await Product.get_by_id(db, product_id)
    return product


@products_router.post(
    '/products',
    response_model=Product,
    responses={404: {"model": ErrorResponse}},
    summary="Create a new product"
)
async def create_product(product: ProductCreate, session: AsyncSession = Depends(get_session)):
    async with session as db:
        catalog = await db.execute(select(Catalog).where(Catalog.catalog_id == product.catalog_id))
        catalog = catalog.scalars().first()
        if not catalog:
            raise CatalogNotFound()
        product = await Product.create(db, name=product.name, catalog_id=catalog.catalog_id)
        return product


@products_router.patch(
    '/products/{product_id}',
    response_model=Product,
    responses={404: {"model": ErrorResponse}},
    summary="Update a product"
)
async def update_product(product_id: int, product: ProductUpdate, session: AsyncSession = Depends(get_session)):
    async with session as db:
        existing_product = await Product.get_by_id(db, product_id)
        if not existing_product:
            raise ProductNotFound()
        if product.catalog_id is not None:
            catalog = await db.execute(select(Catalog).where(Catalog.catalog_id == product.catalog_id))
            catalog = catalog.scalars().first()
            if not catalog:
                raise CatalogNotFound()
        updated_product = await existing_product.update(db, **product.model_dump(exclude_unset=True))
        return updated_product


@products_router.delete(
    '/products/{product_id}',
    response_model=Product | None,
    responses={404: {"model": ErrorResponse}},
    summary="Delete a product"
)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        product = await Product.get_by_id(db, product_id)
        if not product:
            raise ProductNotFound()
        await product.delete(db)
        return product


@products_router.get(
    '/products/catalog/{catalog_id}',
    response_model=list[Product] | None,
    responses={404: {"model": ErrorResponse}},
    summary="Get products by catalog ID"
)
async def get_products_by_catalog(catalog_id: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        products = await Product.filter_by_catalog(db, catalog_id)
    return products
