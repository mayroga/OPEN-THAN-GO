# OPEN THAN GO SYSTEM - Backend Engine v5 (NO FLASK / ASGI READY)
# Company: May Roga LLC

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
import json
import random
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MISSIONS_01 = os.path.join(BASE_DIR, "missions_01_07.json")
MISSIONS_08 = os.path.join(BASE_DIR, "missions_08_14.json")
MISSIONS_15 = os.path.join(BASE_DIR, "missions_15_21.json")


# ----------------------------
# SAFE JSON
# ----------------------------
def safe_json(path):
    try:
        if not os.path.exists(path):
            return {"missions": []}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"missions": []}


DATA_01 = safe_json(MISSIONS_01)
DATA_08 = safe_json(MISSIONS_08)
DATA_15 = safe_json(MISSIONS_15)


# ----------------------------
# FALLBACK
# ----------------------------
def fallback(es, en):
    return {
        "id": 0,
        "cat": "fallback",
        "b": [{"story": {"es": es, "en": en}}]
    }


# ----------------------------
# LOCATION ENGINE
# ----------------------------
def resolver(zip_code, region, estado):
    zip_code = (zip_code or "").strip()

    if zip_code:
        p = zip_code[:2]
        if p in ["33", "34"]:
            estado = "FL"
        elif p in ["75", "76", "77", "78", "79"]:
            estado = "TX"
        elif p in ["90", "91", "92", "93", "94", "95"]:
            estado = "CA"

    if not region:
        region = "General Area"

    return f"{region} {estado}".strip(), estado, region


# ----------------------------
# MISSION ENGINE (ORDER SAFE)
# ----------------------------
def get_mission(decision, pocket):
    try:
        if decision == "casa":
            pool = DATA_01.get("missions", [])
        else:
            pool = random.choice([DATA_08, DATA_15]).get("missions", [])

        if not pool:
            return fallback("Sistema sin misiones", "No missions available")

        filtered = [m for m in pool if pocket in (m.get("pocket_match") or [])]

        return random.choice(filtered) if filtered else random.choice(pool)

    except:
        return fallback("Error de sistema", "System error")


# ----------------------------
# FRONT PAGE
# ----------------------------
@app.get("/")
def home():
    file_path = os.path.join(BASE_DIR, "static/session.html")
    return FileResponse(file_path)


# ----------------------------
# API CORE
# ----------------------------
@app.post("/api/open-than-go")
async def open_than_go(request: Request):

    try:
        data = await request.json()

        decision = data.get("decision", "salir")
        pocket = data.get("budget_level", "cero")

        zip_code = data.get("zip_code", "")
        region = data.get("region", "")
        estado = data.get("estado", "FL")
        desahogo = (data.get("desahogo") or "").lower()

        onboarding = [
            "¿Qué emoción domina tu día?",
            "¿Energía baja, media o alta?",
            "¿Quieres calma o acción?",
            "¿Qué necesitas ahora?"
        ]

        # ---------------- CASA (10 MIN OBLIGATORIO) ----------------
        if decision == "casa":

            mission = get_mission("casa", pocket)

            return JSONResponse({
                "status": "success",
                "tipo": "Casa",
                "duration_sec": 600,
                "breathing": True,
                "voice": True,
                "onboarding": onboarding,
                "mision": mission
            })

        # ---------------- SALIR (1 MIN OBLIGATORIO) ----------------
        location, estado, region = resolver(zip_code, region, estado)

        if "stress" in desahogo or "ansiedad" in desahogo:
            place_type = "lugares tranquilos"
        else:
            place_type = {
                "cero": "parques",
                "minimo": "cafeterias",
                "moderado": "restaurantes",
                "libre": "lugares premium"
            }.get(pocket, "parques")

        gps = f"https://www.google.com/maps/search/{place_type}+en+{location}".replace(" ", "+")

        mission = get_mission("salir", pocket)

        return JSONResponse({
            "status": "success",
            "tipo": "Salida",
            "duration_sec": 60,
            "breathing": True,
            "voice": True,
            "lugar": {
                "name": place_type,
                "zona": location,
                "gps": gps
            },
            "onboarding": onboarding,
            "mision": mission
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)
