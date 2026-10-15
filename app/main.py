from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.database import Base, engine
from app.errors import register_error_handlers
from app.routers import productos, ai

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FIAshion API",
    version="1.0.0",
    description="REST API for the FIAshion clothing advisory system: product catalog "
                "(CRUD) and LLM-based recommendations.",
)
register_error_handlers(app)
app.include_router(productos.router)
app.include_router(ai.router)
