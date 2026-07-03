# main.py - OPEN THAN GO SYSTEM (STABLE ORCHESTRATOR)
# FastAPI backend ONLY (NO Flask)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random

app = FastAPI()

# ----------------------------
# CORS (Render / Frontend safe)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# SIMULADOR DE LUGARES (SALIR)
# ----------------------------
def generar_lugar(zip_code, estado, budget, stress=0):
    opciones = [
        {
            "name": "Parque tranquilo",
            "type": "nature",
            "reason": "Reduce estrés y sobrecarga mental"
        },
        {
            "name": "Cafetería silenciosa",
            "type": "calm",
            "reason": "Permite regulación emocional sin estímulos fuertes"
        },
        {
            "name": "Centro comercial ligero",
            "type": "neutral",
            "reason": "Distracción controlada sin aislamiento"
        },
        {
            "name": "Caminar 10 minutos en zona segura",
            "type": "movement",
            "reason": "Activa sistema nervioso y reduce ansiedad"
        }
    ]

    # lógica simple adaptativa (estable, sin sobreingeniería)
    if budget == "cero":
        return opciones[3]
    if stress and stress > 7:
        return opciones[0]

    return random.choice(opciones)

# ----------------------------
# MISIONES CASA (simplificado seguro)
# ----------------------------
def cargar_misiones_home():
    return [
        {
            "id": 1,
            "title": "Respiración guiada",
            "type": "breath",
            "duration": 120,
            "text": {
                "es": "Respira lento. Inhala calma. Exhala tensión.",
                "en": "Breathe slowly. Inhale calm. Exhale tension."
            }
        },
        {
            "id": 2,
            "title": "Reorden mental",
            "type": "reflection",
            "duration": 180,
            "text": {
                "es": "Piensa en una cosa que puedes controlar hoy.",
                "en": "Think of one thing you can control today."
            }
        },
        {
            "id": 3,
            "title": "Micro-acción",
            "type": "action",
            "duration": 120,
            "text": {
                "es": "Haz una acción pequeña que mejore tu bienestar ahora.",
                "en": "Do one small action that improves your wellbeing now."
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

        mode = data.get("decision", "salir")  # "salir" o "casa"
        lang = data.get("lang", "es")
        budget = data.get("budget_level", "cero")
        zip_code = data.get("zip_code", "")
        estado = data.get("estado", "")
        desahogo = data.get("desahogo", "")

        # -------------------------
        # MODO CASA (ENGINE.JS)
        # -------------------------
        if mode == "casa":

            return JSONResponse({
                "status": "success",
                "mode": "home",
                "duration": 600,  # 10 minutos
                "missions": cargar_misiones_home(),
                "breathing": {
                    "enabled": True,
                    "pattern": "4-4-6"
                },
                "voice": True
            })

        # -------------------------
        # MODO SALIR (MAIN LOGIC)
        # -------------------------
        stress_level = len(desahogo) % 10  # simulación ligera estable

        lugar = generar_lugar(zip_code, estado, budget, stress_level)

        return JSONResponse({
            "status": "success",
            "mode": "out",
            "duration": 60,  # 1 minuto máximo
            "place": lugar,
            "why": lugar["reason"],
            "psych_logic": {
                "es": "Este lugar fue seleccionado para regular tu estado emocional actual.",
                "en": "This place was selected to regulate your current emotional state."
            },
            "action": "go"
        })

    except Exception as e:

        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
def root():
    return {
        "status": "OPEN THAN GO ACTIVE",
        "backend": "stable",
        "modes": ["home", "out"]
    }
