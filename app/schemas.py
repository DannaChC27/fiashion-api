from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100,
                        description="Product name", examples=["Oversize denim jacket"])
    descripcion: str = Field("", max_length=300,
                             description="Short description", examples=["Blue denim jacket, unisex fit"])
    precio: float = Field(..., gt=0, description="Price in COP", examples=[129900])
    talla: str = Field("M", description="Size (XS, S, M, L, XL)", examples=["M"])
    genero: str = Field("unisex", description="Target gender", examples=["mujer"])
    categoria: str = Field("general", description="Category", examples=["chaquetas"])
    estilo: str = Field("casual", description="Style", examples=["urbano"])
    disponible: bool = Field(True, description="Is it in stock?", examples=[True])


class ProductoCreate(ProductoBase):
    pass


class ProductoOut(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id_producto: int = Field(..., examples=[1])


class ErrorOut(BaseModel):
    status: int = Field(..., examples=[404])
    message: str = Field(..., examples=["Product not found"])
    timestamp: str = Field(..., examples=["2026-10-14T22:55:56+00:00"])


class ValidationErrorOut(BaseModel):
    status: int = Field(..., examples=[422])
    message: str = Field(..., examples=["Invalid data"])
    timestamp: str = Field(..., examples=["2026-10-14T22:55:56+00:00"])
    details: list[dict] = Field(..., examples=[[{"field": "body.precio",
                                                  "problem": "Input should be greater than 0"}]])


class RecommendRequest(BaseModel):
    talla: str = Field(..., description="Customer size", examples=["M"])
    genero: str = Field(..., description="Gender / age group", examples=["mujer"])
    categoria: str = Field(..., description="Wanted category", examples=["chaquetas"])
    estilo: Optional[str] = Field(None, description="Wanted style", examples=["urbano"])
    technique: Literal["zero_shot", "few_shot", "cot"] = Field(
        "zero_shot", description="Prompting technique to use")


class RecommendResponse(BaseModel):
    technique: str
    recommendation: str
    products_considered: int
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    latency_ms: int
