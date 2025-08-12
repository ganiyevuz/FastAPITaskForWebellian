from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import Catalog
from models.products import Product
from schemas import ErrorResponse
from schemas.products import ProductCreate, ProductUpdate
from services.engine import get_session
from services.pagination import PaginatedResponse
from shared.exeptions import ProductNotFound, CatalogNotFound
from shared.utils import load_products

products_router = APIRouter(tags=['Products'], prefix='/api/v1')


@products_router.get(
    '/products',
    response_model=PaginatedResponse[Product] | None,
    summary="Get all products"
)
async def get_products(limit: int = Query(100, ge=0), offset: int = Query(0, ge=0),
                       session: AsyncSession = Depends(get_session)):
    async with session as db:
        products = await Product.all(db, limit=limit, offset=offset)
    return PaginatedResponse(count=len(products), items=products)  # type: ignore


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


@products_router.get(
    '/products/catalog/{catalog_id}',
    response_model=list[Product] | None,
    responses={404: {"model": ErrorResponse}},
    summary="Get products by catalog ID"
)
async def get_products_by_catalog(catalog_id: int, session: AsyncSession = Depends(get_session)):
    """Get products by catalog ID."""
    async with session as db:
        products = await Product.filter_by_catalog(db, catalog_id)
    return products


@products_router.get('/products/top-products', response_model=PaginatedResponse[Product] | None)
async def get_top_products(
        top_n: int = Query(gt=0),
        offset: int = Query(0, ge=0),
        session: AsyncSession = Depends(get_session)
):
    """Get top N products by price."""
    async with session as db:
        products = await Product.get_top_products(db, top_n, offset=offset)
    return PaginatedResponse(count=len(products), items=products)  # type: ignore


@products_router.get(
    '/products/{product_id}',
    response_model=Product | None,
    summary="Get product by ID"
)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    async with session as db:
        product = await Product.get_by_id(db, product_id)
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


@products_router.post('/etl/products', summary="ETL Products")
async def etl_catalogs(file: UploadFile = File(...), session: AsyncSession = Depends(get_session)):
    if not file.content_type == 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")
    async with session as db:
        try:
            products = await load_products(file.file)
            if not products:
                raise HTTPException(status_code=400, detail="No valid products found in the file.")
            await Product.bulk_create(db, products)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        return {"message": "ETL process completed successfully"}
