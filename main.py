# main.py - OPEN THAN GO SYSTEM (FINAL STABLE DEPLOY)
# FastAPI + Static + API + Render Ready

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import random

app = FastAPI()

# ----------------------------
# STATIC FILES (ESTO ARREGLA EL 404)
# ----------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------
# ROOT -> ABRE FRONTEND
# ----------------------------
@app.get("/")
def root():
    return FileResponse("static/session.html")

# ----------------------------
# LUGAR SIMULADO (SALIR)
# ----------------------------
def generar_lugar(zip_code, estado, budget, stress=0):

    opciones = [
        {
            "name": "Parque tranquilo",
            "reason": "Reduce estrés y ayuda a estabilizar tu mente",
            "gps_link": "https://maps.google.com"
        },
        {
            "name": "Cafetería silenciosa",
            "reason": "Ambiente seguro para regular emociones",
            "gps_link": "https://maps.google.com"
        },
        {
            "name": "Caminar zona segura",
            "reason": "Movimiento físico regula ansiedad y pensamiento",
            "gps_link": "https://maps.google.com"
        }
    ]

    if budget == "cero":
        return opciones[2]

    if stress > 7:
        return opciones[0]

    return random.choice(opciones)

# ----------------------------
# MISIONES CASA
# ----------------------------
def misiones_casa():

    return [
        {
            "id": 1,
            "type": "breath",
            "duration": 120,
            "text": {
                "es": "Respira lento. Inhala calma. Exhala tensión.",
                "en": "Breathe slowly. Inhale calm. Exhale tension."
            }
        },
        {
            "id": 2,
            "type": "reflection",
            "duration": 180,
            "text": {
                "es": "Observa qué puedes controlar hoy.",
                "en": "Notice what you can control today."
            }
        },
        {
            "id": 3,
            "type": "action",
            "duration": 120,
            "text": {
                "es": "Haz una pequeña acción para mejorar tu estado.",
                "en": "Take a small action to improve your state."
            }
        }
    ]

# ----------------------------
# API PRINCIPAL
# ----------------------------
@app.post("/api/open-than-go")
async def open_than_go(request: Request):

    try:
        data = await request.json()

        mode = data.get("decision", "salir")
        lang = data.get("lang", "es")
        budget = data.get("budget_level", "cero")
        zip_code = data.get("zip_code", "")
        estado = data.get("estado", "")
        desahogo = data.get("desahogo", "")

        # ---------------- CASA ----------------
        if mode == "casa":

            return JSONResponse({
                "status": "success",
                "mode": "home",
                "duration": 600,
                "missions": misiones_casa()
            })

        # ---------------- SALIR ----------------
        stress = min(len(desahogo or "") % 10, 10)

        lugar = generar_lugar(zip_code, estado, budget, stress)

        return JSONResponse({
            "status": "success",
            "mode": "out",
            "duration": 60,
            "place": lugar,
            "why": lugar["reason"],
            "action": "go"
        })

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)
