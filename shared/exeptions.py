from fastapi import HTTPException


class ProductNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Product not found")


class CatalogNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Catalog not found")
