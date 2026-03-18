from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import users, categories, products, meta

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRUD API",
    description="Generic CRUD API for dynamic admin panel",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(meta.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "CRUD API is running", "docs": "/docs", "meta": "/api/meta"}
