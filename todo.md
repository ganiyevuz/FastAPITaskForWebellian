## Python Technical Task

**🛠️ Task Description:**  
Develop a Python **FastAPI** application for managing shop inventory.  

### 📦 Catalog Management
- Retrieve a list of catalogs.
- Add, update, or delete catalogs.

### 🛒 Product Management
- Retrieve a list of products within a specific catalog.
- Create, update, or delete products.
- Assign or remove a product from a catalog.

### 📑 API Documentation and Testing
- Provide API documentation using Swagger (OpenAPI), built-in with FastAPI.
- Ensure the application can be tested effectively via Swagger UI at `/docs`.

---

**🗄️ Database:**  
Use one of:
- In-memory DB (e.g., SQLite with `:memory:`)
- Persistent DB (e.g., SQLite, PostgreSQL) with ORM like SQLAlchemy or Tortoise ORM.

---

**✅ Expectations:**
- Strong understanding of Python backend best practices.
- Modular architecture (routers, services, models, schemas).
- Clean, maintainable, scalable code.
- API docs & error handling.
- Simple but extensible design.

**📂 Bonus:**
- Dependency injection with `Depends`.
- Unit tests (pytest, httpx).
- Dockerfile or run instructions.

---

## Data Engineer Technical Task

**🛠️ Task Description:**  
Build a **data pipeline** application to ingest, transform, and serve shop inventory data (mini ETL).

### 📦 Data Ingestion
- Read from CSV/JSON (mock or generate data).
- Fields:
  - Catalog: `catalog_id`, `name`, `created_at`
  - Product: `product_id`, `name`, `price`, `catalog_id`, `updated_at`

### 🔄 Data Transformation
- Convert dates to consistent format/timezone.
- Normalize product names (case, whitespace).
- Validate schema and clean bad entries.

### 🗄️ Data Storage
- Store cleaned data in DB (PostgreSQL, SQLite, Parquet, DuckDB).
- Use proper schema with relationships.

### 🔍 Data Serving & Querying
- Query products by catalog.
- Get top N products by price.
- Get product counts per catalog.

### 🧪 Testing & Validation
- Data quality checks (nulls, count mismatches).
- Logging & error handling.

---

**🧰 Suggested Stack:**
- Python
- pandas
- SQLAlchemy
- FastAPI / Typer
- pydantic
- pytest
- Optional: Airflow, Dagster, Prefect

---

**✅ Expectations:**
- Understanding ETL, data modeling, integrity.
- Clean modular code.
- Practical DB interaction.
- Documentation & validation.

**📂 Bonus:**
- Dockerized setup.
- Data versioning/partitioning.
- Pipeline orchestration.
- Unit/integration tests.

---
