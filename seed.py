"""Mete prendas de ejemplo para probar la IA. Uso: python seed.py"""
from app.database import Base, engine, SessionLocal
from app.models import Producto

Base.metadata.create_all(bind=engine)
datos = [
    ("Chaqueta de jean oversize", 129900, "M", "mujer", "chaquetas", "urbano"),
    ("Chaqueta bomber negra", 159900, "M", "mujer", "chaquetas", "urbano"),
    ("Chaqueta impermeable", 189900, "M", "unisex", "chaquetas", "deportivo"),
    ("Chaqueta de cuero sintetico", 210000, "M", "mujer", "chaquetas", "urbano"),
    ("Camisa de lino", 89900, "S", "mujer", "camisas", "casual"),
    ("Pantalon cargo", 119900, "L", "hombre", "pantalones", "urbano"),
]
with SessionLocal() as db:
    if not db.query(Producto).count():
        for n, p, t, g, c, e in datos:
            db.add(Producto(nombre=n, precio=p, talla=t, genero=g, categoria=c, estilo=e))
        db.commit()
print("Listo")
