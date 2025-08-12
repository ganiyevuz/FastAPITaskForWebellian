from contextlib import asynccontextmanager

from fastapi import FastAPI

from routers import products_router, catalogs_router
from services.engine import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: Shadows name 'app' from outer scope
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, docs_url="/")
app.include_router(catalogs_router)
app.include_router(products_router)
