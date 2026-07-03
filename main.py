# OPEN THAN GO SYSTEM - MAIN BACKEND v6 (ASGI STABLE)
# Company: May Roga LLC

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import random

app = FastAPI()

# ------------------------------
# PATHS
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# ------------------------------
# STATIC FILES (CRÍTICO)
# ------------------------------
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ------------------------------
# INDEX
# ------------------------------
@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "session.html"))

# ------------------------------
# SAFE MISSION LOADER (MINIMAL)
# ------------------------------
def safe_mission(decision: str, pocket: str):
    if decision == "casa":
        return {
            "b": [
                {"tx": {"es": "Respira lento y profundo", "en": "Breathe slow and deep"}},
                {"t": "breath_auto", "d": 10},
                {"tx": {"es": "Suelta tensión corporal", "en": "Release body tension"}}
            ]
        }

    return {
        "b": [
            {"tx": {"es": "Observa tu entorno con calma", "en": "Observe your environment calmly"}},
            {"t": "breath_auto", "d": 8},
            {"tx": {"es": "Elige un lugar seguro cercano", "en": "Choose a safe nearby place"}}
        ]
    }

# ------------------------------
# LOCATION SIMPLE ENGINE
# ------------------------------
def build_location(zip_code: str, estado: str):

    prefix = (zip_code or "")[:2]

    if prefix in ["33", "34"]:
        estado = "FL"
    elif prefix in ["10", "11", "12", "13"]:
        estado = "NY"

    query_map = {
        "FL": "parks miami",
        "NY": "parks new york",
        "TX": "parks texas"
    }

    query = query_map.get(estado, "parks near me")

    return {
        "name": "Exploración local",
        "estado": estado,
        "gps_link": f"https://www.google.com/maps/search/?api=1&query={query}"
    }

# ------------------------------
# API MAIN
# ------------------------------
@app.post("/api/open-than-go")
async def open_than_go(payload: dict):

    try:
        decision = payload.get("decision", "salir")
        budget = payload.get("budget_level", "cero")
        zip_code = payload.get("zip_code", "")
        estado = payload.get("estado", "FL")

        mision = safe_mission(decision, budget)

        if decision == "casa":

            return JSONResponse({
                "status": "success",
                "tipo": "Casa",
                "mision": mision,
                "lugar": None
            })

        lugar = build_location(zip_code, estado)

        return JSONResponse({
            "status": "success",
            "tipo": "Salida",
            "mision": mision,
            "lugar": lugar
        })

    except Exception as e:

        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

# ------------------------------
# HEALTH CHECK
# ------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
