## Here is what I implemented based on provided task:

I divided project into modular structure with separate directories for routes, models, schemas and services.
This modular approach allows for better organization and maintainability of the codebase.

## Project Structure

- **Catalog Management**:
    - Retrieve a list of catalogs.
    - Create, update, and delete catalogs.

- **Product Management**:
    - Retrieve a list of products.
    - Create, update, and delete products.
    - Retrieve products by catalog and top products by price.

- **ETL Process**:
    - Load catalogs and products from CSV files and bulk-insert them into the database.

- **API Documentation**:
    - Automatically generated using FastAPI's built-in OpenAPI support.
    - Accessible at `/docs`.

## Used Technologies

- **uv**: Package manager for manage dependencies.
- **FastAPI**: For building the RESTful API.
- **SQLAlchemy**: For ORM functionality to interact with PostgreSQL.
- **SQLModel**: For defining database models and schemas.
- **asyncpg**: For asynchronous database operations with PostgreSQL.
- **Pydantic**: For data validation and serialization.
- **Docker**: For containerization of the application.
- **Docker Compose**: For managing multi-container applications, including the FastAPI app and PostgreSQL database.
- **alembic**: For database migrations.


## Features Implemented

### 1. Catalog Management (CRUD)

- **Retrieve All Catalogs**:
    - Endpoint: `GET /api/v1/catalogs`
    - Retrieves a paginated list of catalogs with product count.

- **Create a New Catalog**:
    - Endpoint: `POST /api/v1/catalogs`
    - Creates a new catalog.

- **Retrieve Catalog by ID**:
    - Endpoint: `GET /api/v1/catalogs/{catalog_id}`
    - Retrieves a specific catalog by its ID.

- **Update a Catalog**:
    - Endpoint: `PUT /api/v1/catalogs/{catalog_id}`
    - Updates an existing catalog by ID.

- **Delete a Catalog**:
    - Endpoint: `DELETE /api/v1/catalogs/{catalog_id}`
    - Deletes a catalog by ID.

### 2. Product Management (CRUD)

- **Retrieve All Products**:
    - Endpoint: `GET /api/v1/products`
    - Retrieves a paginated list of products.

- **Create a New Product**:
    - Endpoint: `POST /api/v1/products`
    - Creates a new product and associates it with an existing catalog.

- **Retrieve Products by Catalog ID**:
    - Endpoint: `GET /api/v1/products/catalog/{catalog_id}`
    - Retrieves products by their associated catalog ID.

- **Retrieve Top Products by Price**:
    - Endpoint: `GET /api/v1/products/top-products`
    - Retrieves top N products by price, with pagination support.

- **Retrieve Product by ID**:
    - Endpoint: `GET /api/v1/products/{product_id}`
    - Retrieves a specific product by its ID.

- **Update a Product**:
    - Endpoint: `PATCH /api/v1/products/{product_id}`
    - Updates an existing product by ID.

- **Delete a Product**:
    - Endpoint: `DELETE /api/v1/products/{product_id}`
    - Deletes a product by ID.

### 3. ETL Process

- **ETL for Catalogs**:
    - Endpoint: `POST /api/v1/etl/catalogs`
    - Allows the upload of a CSV file containing catalog data and performs an ETL process to insert the catalogs into
      the database.

- **ETL for Products**:
    - Endpoint: `POST /api/v1/etl/products`
    - Allows the upload of a CSV file containing product data and performs an ETL process to insert the products into
      the database.

## Database

- **Database Engine**: PostgreSQL
- **ORM**: SQLAlchemy + SQLModel
    - SQLAlchemy provides ORM functionality for interacting with PostgreSQL asynchronously.
    - SQLModel is used as an extension of SQLAlchemy to simplify database interactions and model definitions.

## Database Models

- **Catalog**: Represents product catalogs with fields such as `catalog_id`, `name`, and `created_at`.
- **Product**: Represents products with fields such as `product_id`, `name`, `price`, `created_at`, and `updated_at`.
  Each product is associated with a catalog using the `catalog_id`.

## Deployment

### Dockerfile

A `Dockerfile` is included to containerize the FastAPI application, allowing it to run in a consistent environment
across different systems. The application is packaged into a Docker image with the following steps:

1. Install dependencies from `pyproject.toml`.
2. Copy the application code into the container.
3. Expose port `8000` to run the FastAPI application.

### Docker Compose

Docker Compose is used to manage the application's services, including the FastAPI application and the PostgreSQL
database.

### Docker Compose Configuration

The **`docker-compose.yml`** file defines the two services: the FastAPI application and the PostgreSQL database.

```yaml
services:
  db:
    image: postgres:16-alpine
    container_name: db
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_INITDB_ARGS: "--data-checksums"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready -U ${DATABASE_USER}" ]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    env_file:
      - .env
    environment:
      DATABASE_URL: "postgresql+asyncpg://${DATABASE_USER}:${DATABASE_PASSWORD}@db:5432/${DATABASE_NAME}"
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```