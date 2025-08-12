import csv
from datetime import datetime
from loguru import logger

from models import Catalog

CATALOGS_FILE = '../data/catalogs.csv'
PRODUCTS_FILE = '../data/products.csv'


def parse_datetime(date_str):
    """
    Parse a datetime string in the format 'YYYY-MM-DD HH:MM:SS'.
    Returns a datetime object or None if parsing fails.
    """
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}")
        return None


def load_catalogs(raise_on_error=False):
    with open(CATALOGS_FILE, encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        catalogs = []
        for row in csv_reader:
            created_at = row.get('created_at', None)
            name = row.get('name', None)
            if not any((name, created_at)):
                logger.warning("Skipping row with missing 'name' or 'created_at'")
                if raise_on_error:
                    raise ValueError("Row must contain 'name' or 'created_at'")
                else:
                    continue
            created_at = parse_datetime(created_at)
            if created_at is None:
                if raise_on_error:
                    raise ValueError(f"Invalid date format for row: {row}")
                else:
                    logger.warning(f"Invalid date format for row: {row}")
                    continue
            catalogs.append(Catalog(name=name, created_at=created_at))
    return catalogs


def load_products(raise_on_error=False):
    from models import Product
    with open(PRODUCTS_FILE, encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        products = []
        for row in csv_reader:
            name = row.get('name', None)
            price = row.get('price', None)
            catalog = row.get('catalog', None)
            created_at = row.get('created_at', None)
            updated_at = row.get('updated_at', None)
            if not name or not price:
                logger.warning("Skipping row with missing 'name' or 'price'")
                if raise_on_error:
                    raise ValueError("Row must contain 'name' and 'price'")
                else:
                    continue
            try:
                price = float(price)
            except ValueError:
                if raise_on_error:
                    raise logger.warning(f"Invalid price format for row: {row}")
                else:
                    logger.warning(f"Invalid price format for row: {row}")
                    continue
            created_at = parse_datetime(created_at)
            updated_at = parse_datetime(updated_at)

            if not any((created_at, updated_at)):
                logger.warning("Skipping row with invalid 'created_at' or 'updated_at'")
                if raise_on_error:
                    raise ValueError(f"Invalid date format for row: {row}")
                else:
                    logger.warning(f"Invalid date format for row: {row}")
                    continue
            name = name.strip()
            products.append(Product(name=name, price=price))
    return products
