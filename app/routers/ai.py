from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Producto
from app.schemas import RecommendRequest, RecommendResponse, ErrorOut
from app.prompts import TECNICAS
from app.llm import llamar_gemini

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])


@router.post("/recommend", response_model=RecommendResponse,
             summary="Recommend clothes with an LLM",
             description=("Looks for available products that match the customer filters, "
                          "puts them in the prompt (basic RAG) and asks the LLM to pick "
                          "up to 3. The prompting technique can be zero_shot, few_shot or cot."),
             responses={429: {"model": ErrorOut, "description": "AI rate limit"},
                        502: {"model": ErrorOut, "description": "AI provider error"},
                        503: {"model": ErrorOut, "description": "AI not configured"},
                        504: {"model": ErrorOut, "description": "AI timeout"}})
def recomendar(datos: RecommendRequest, db: Session = Depends(get_db)):
    # 1. RETRIEVAL: solo prendas disponibles que cumplen los filtros
    consulta = select(Producto).where(
        Producto.disponible.is_(True),
        Producto.talla == datos.talla,
        Producto.genero.in_([datos.genero, "unisex"]),
        Producto.categoria == datos.categoria,
    )
    if datos.estilo:
        consulta = consulta.where(Producto.estilo == datos.estilo)
    productos = db.scalars(consulta.limit(20)).all()

    # Si no hay prendas, no gastamos una llamada al modelo.
    if not productos:
        return RecommendResponse(technique=datos.technique,
                                 recommendation="No available products match those filters.",
                                 products_considered=0, latency_ms=0)

    # 2. AUGMENTATION: armamos el prompt con las prendas reales
    prompt = TECNICAS[datos.technique](productos, datos.talla, datos.genero,
                                       datos.categoria, datos.estilo)

    # 3. GENERATION: llamamos al LLM
    res = llamar_gemini(prompt, datos.technique)
    return RecommendResponse(technique=datos.technique, recommendation=res["texto"],
                             products_considered=len(productos),
                             input_tokens=res["tok_in"], output_tokens=res["tok_out"],
                             latency_ms=res["ms"])
