"""Los 3 prompts que vamos a comparar. Misma tarea, distinta tecnica."""
from typing import List
from app.models import Producto


def _catalogo(productos: List[Producto]) -> str:
    return "\n".join(
        f"- id {p.id_producto}: {p.nombre} | {p.categoria} | talla {p.talla} | "
        f"estilo {p.estilo} | ${p.precio:,.0f}" for p in productos)


def _filtros(talla, genero, categoria, estilo) -> str:
    return (f"talla {talla}, genero {genero}, categoria {categoria}, "
            f"estilo {estilo or 'cualquiera'}")


def zero_shot(productos, talla, genero, categoria, estilo) -> str:
    return (
        "Eres el asesor de una tienda de ropa. Recomienda hasta 3 prendas "
        "de la lista que mejor encajen con el cliente. Usa SOLO prendas de la lista.\n\n"
        f"Cliente: {_filtros(talla, genero, categoria, estilo)}\n\n"
        f"Prendas disponibles:\n{_catalogo(productos)}")


def few_shot(productos, talla, genero, categoria, estilo) -> str:
    return (
        "Eres el asesor de una tienda de ropa. Recomienda hasta 3 prendas de la lista. "
        "Usa SOLO prendas de la lista y responde SIEMPRE con este formato: "
        "'id X - nombre - razon corta'.\n\n"
        "Ejemplo 1\n"
        "Cliente: talla S, genero mujer, categoria camisas, estilo casual\n"
        "Respuesta:\nid 4 - Camisa de lino - talla S y estilo casual\n\n"
        "Ejemplo 2\n"
        "Cliente: talla L, genero hombre, categoria pantalones, estilo formal\n"
        "Respuesta:\nid 9 - Pantalon sastre - talla L y estilo formal\n\n"
        "Ahora el cliente real\n"
        f"Cliente: {_filtros(talla, genero, categoria, estilo)}\n"
        f"Prendas disponibles:\n{_catalogo(productos)}\n"
        "Respuesta:")


def cot(productos, talla, genero, categoria, estilo) -> str:
    return (
        "Eres el asesor de una tienda de ropa. Piensa paso a paso. "
        "Primero revisa cada prenda y di si cumple talla, categoria y estilo. "
        "Despues da la recomendacion final (hasta 3 prendas, solo de la lista).\n\n"
        f"Cliente: {_filtros(talla, genero, categoria, estilo)}\n\n"
        f"Prendas disponibles:\n{_catalogo(productos)}")


TECNICAS = {"zero_shot": zero_shot, "few_shot": few_shot, "cot": cot}
