from datetime import datetime

import pandas as pd
from loguru import logger
from models import Catalog, Product


def parse_datetime(date_val):
    """
    Converts pandas Timestamp or string to datetime, returns None if invalid.
    """
    if pd.isna(date_val):
        return None
    if isinstance(date_val, pd.Timestamp):
        return date_val.to_pydatetime()
    try:
        return pd.to_datetime(date_val).to_pydatetime()
    except Exception as e:
        logger.warning(f"Invalid date format: {date_val}")
        return None


def load_catalogs(file, raise_on_error=False):
    file.seek(0)
    df = pd.read_csv(file, parse_dates=["created_at"])
    logger.info(f"Loaded {len(df)} rows from catalog file")
    success, skips = 0, 0
    catalogs = []
    for _, row in df.iterrows():
        name = row.get("name")
        created_at = parse_datetime(row.get("created_at"))

        if not (name and created_at):
            logger.warning(
                "Skipping row with missing or invalid 'name' or 'created_at'"
            )
            if raise_on_error:
                raise ValueError("Row must contain valid 'name' and 'created_at'")
            skips += 1
            continue
        catalogs.append(Catalog(name=name.strip(), created_at=created_at))
        logger.info(f"Loaded catalog: {name.strip()} created at: {created_at}")
        success += 1
    logger.info(f"Successfully loaded {success} catalogs, {skips} Skipped entries")
    return catalogs


cached_catalogs = {}


async def load_products(file, raise_on_error=False):
    file.seek(0)
    df = pd.read_csv(file, parse_dates=["created_at", "updated_at"])
    success, skips = 0, 0
    products = []
    for _, row in df.iterrows():
        name = row.get("name")
        price = row.get("price")
        catalog = row.get("catalog_id")
        created_at = parse_datetime(row.get("created_at"))
        updated_at = parse_datetime(row.get("updated_at"))

        if not name or pd.isna(price):
            logger.warning("Skipping row with missing 'name' or 'price'")
            if raise_on_error:
                raise ValueError("Row must contain 'name' and 'price'")
            skips += 1
            continue

        try:
            price = float(price)
        except ValueError:
            logger.warning(f"Invalid price format for row: {row.to_dict()}")
            if raise_on_error:
                raise ValueError(f"Invalid price format for row: {row.to_dict()}")
            skips += 1
            continue

        if not (created_at and updated_at):
            logger.warning("Skipping row with invalid 'created_at' or 'updated_at'")
            if raise_on_error:
                raise ValueError(f"Invalid date format for row: {row.to_dict()}")
            skips += 1
            continue

        products.append(
            Product(
                name=name.strip(),
                price=price,
                created_at=created_at,
                updated_at=updated_at,
                catalog_id=catalog,
            )
        )
        logger.info(
            f"Loaded product: {name.strip()} with price: {price} and catalog_id: {catalog}"
        )
        success += 1
    logger.info(f"Successfully loaded {success} products, {skips} Skipped entries")
    return products
