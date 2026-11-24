from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.product_routes import router as product_router
from app.routes.customer_routes import router as customer_router
from app.routes.sale_routes import router as sale_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Inventory API (MVC)",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(product_router)
app.include_router(customer_router)
app.include_router(sale_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)