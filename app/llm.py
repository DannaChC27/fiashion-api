"""Llamada a Gemini por REST. Aqui se manejan timeout, rate limit y fallas."""
import os
import time
import csv
import httpx
from fastapi import HTTPException

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
TIMEOUT_SECONDS = 15.0
LOG_PATH = os.getenv("LLM_LOG_PATH", "llm_calls.csv")


def _guardar_en_log(tecnica, prompt, respuesta, tok_in, tok_out, ms):
    """Cada llamada real queda en un CSV: sirve de evidencia y para calcular costos."""
    nuevo = not os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuevo:
            w.writerow(["technique", "prompt", "response", "input_tokens",
                        "output_tokens", "latency_ms"])
        w.writerow([tecnica, prompt, respuesta, tok_in, tok_out, ms])


def llamar_gemini(prompt: str, tecnica: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")
    if not api_key or not model:
        raise HTTPException(503, "AI service is not configured")

    inicio = time.perf_counter()
    try:
        r = httpx.post(
            API_URL.format(model=model),
            headers={"x-goog-api-key": api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=TIMEOUT_SECONDS,
        )
    except httpx.TimeoutException:
        raise HTTPException(504, "The AI provider took too long to answer")
    except httpx.HTTPError:
        raise HTTPException(502, "Could not reach the AI provider")

    if r.status_code == 429:
        raise HTTPException(429, "AI rate limit reached, try again later")
    if r.status_code in (401, 403):
        raise HTTPException(502, "AI provider rejected the API key")
    if r.status_code >= 400:
        raise HTTPException(502, "AI provider returned an error")

    datos = r.json()
    try:
        texto = datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise HTTPException(502, "AI provider returned an empty answer")

    uso = datos.get("usageMetadata", {})
    ms = int((time.perf_counter() - inicio) * 1000)
    tok_in = uso.get("promptTokenCount")
    tok_out = uso.get("candidatesTokenCount")
    _guardar_en_log(tecnica, prompt, texto, tok_in, tok_out, ms)
    return {"texto": texto, "tok_in": tok_in, "tok_out": tok_out, "ms": ms}
